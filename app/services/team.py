from typing import Any

from app.services.history_service import (
    HistoryService
)

from app.services.response_validator import (
    ResponseValidator
)


class AITeam:

    MAX_FIX_ATTEMPTS = 3
    MAX_JSON_FIX_ATTEMPTS = 3

    def __init__(
        self,
        planner,
        architect,
        developer,
        qa
    ):

        self.planner = planner
        self.architect = architect
        self.developer = developer
        self.qa = qa

    @staticmethod
    def compress(
        text: str,
        limit: int = 500
    ) -> str:

        return str(
            text or ""
        )[:limit]

    @staticmethod
    def extract_content(
        response
    ) -> str:

        if response is None:
            return ""

        if hasattr(
            response,
            "content"
        ):

            return str(
                response.content
            )

        if isinstance(
            response,
            dict
        ):

            return str(
                response.get(
                    "content",
                    ""
                )
            )

        return str(
            response
        )

    @staticmethod
    def repair_json(
        text: str
    ) -> str:

        if not text:
            return ""

        text = str(text)

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        start = text.find("{")
        end = text.rfind("}")

        if (
            start == -1
            or
            end == -1
        ):
            return ""

        return text[
            start:end + 1
        ]

    @staticmethod
    def is_empty_response(
        text: str
    ) -> bool:

        return (
            not text
            or
            not str(text).strip()
        )

    def get_rules(self) -> str:

        return """
ОБЯЗАТЕЛЬНО:

Создай простой FastAPI проект.

Используй:

- FastAPI
- logging
- uvicorn

Структура:

1) app/main.py
2) requirements.txt

main.py должен:

- создать FastAPI()
- иметь endpoint "/"
- вернуть:

{
    "status":"ok"
}

requirements.txt:

fastapi>=0.136
uvicorn>=0.35

Правила:

- только два файла
- только app/main.py
- только requirements.txt
- content всегда строка
- никаких БД
- никаких selenium
- никаких parser
- никаких settings
- никаких postgres
- никаких dotenv
- никаких дополнительных файлов
- без markdown
- без пояснений

Вернуть только JSON:

{
    "files":[
        {
            "path":"app/main.py",
            "content":"..."
        },
        {
            "path":"requirements.txt",
            "content":"..."
        }
    ]
}
"""

    def run(
        self,
        task: str
    ):

        state: dict[str, Any] = {

            "task": task,
            "plan": "",
            "architecture": "",
            "code": "",
            "review": "",
            "runtime_errors": []

        }

        team_errors = (
            HistoryService.get_known_errors()
        )

        success_patterns = (
            HistoryService.get_success_patterns()
        )

        print(
            "\n=== ПЛАНИРОВЩИК ===\n"
        )

        state["plan"] = self.compress(
            self.extract_content(
                self.planner.run(
                    task
                )
            ),
            400
        )

        print(
            "\n=== АРХИТЕКТОР ===\n"
        )

        state["architecture"] = self.compress(
            self.extract_content(
                self.architect.run(
                    state["plan"]
                )
            )
        )

        print(
            "\n=== РАЗРАБОТЧИК ===\n"
        )

        rules = self.get_rules()

        state["code"] = self.repair_json(
            self.extract_content(
                self.developer.run(
                    f"""
Задача:

{task}

Известные ошибки:

{team_errors}

Успешные решения:

{success_patterns}

{rules}
"""
                )
            )
        )

        for attempt in range(
            self.MAX_JSON_FIX_ATTEMPTS
        ):

            if self.is_empty_response(
                state["code"]
            ):

                print(
                    "\nПустой ответ, повтор...\n"
                )

            else:

                is_valid, error = (
                    ResponseValidator.validate(
                        state["code"]
                    )
                )

                if is_valid:

                    return state

                print(
                    f"\nОшибка ответа: {error}"
                )

                print(
                    "\n=== RAW RESPONSE ===\n"
                )

                print(
                    state["code"][:3000]
                )

            state["code"] = self.repair_json(
                self.extract_content(
                    self.developer.run(
                        f"""
Исправь проект.

Предыдущий ответ:

{state["code"]}

{rules}

Верни только JSON.
"""
                    )
                )
            )

        state["runtime_errors"] = [
            "Не удалось получить валидный JSON"
        ]

        state["code"] = ""

        return state