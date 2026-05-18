class AITeam:

    MAX_FIX_ATTEMPTS = 3


    def __init__(
        self,
        architect,
        developer,
        qa
    ):

        self.architect = architect
        self.developer = developer
        self.qa = qa


    @staticmethod
    def compress(
        text: str,
        limit: int = 500
    ) -> str:

        if not text:
            return ""

        return text[:limit]


    def run(
        self,
        task: str
    ):

        state = {
            "task": task,
            "architecture": "",
            "code": "",
            "review": ""
        }


        print(
            "\n=== АРХИТЕКТОР ===\n"
        )


        architecture = self.architect.run(
            f"""
Задача:

{task}

Создай:

1. Стек
2. Структуру проекта
3. Компоненты

Максимум 200 слов.
"""
        )

        state["architecture"] = self.compress(
            architecture,
            500
        )


        print(
            "\n=== РАЗРАБОТЧИК ===\n"
        )


        state["code"] = self.developer.run(
            f"""
Задача:

{task}

Архитектура:

{state["architecture"]}

Верни ТОЛЬКО JSON.

Строгий формат:

{{
    "files": [
        {{
            "path": "app/main.py",
            "content": "..."
        }},
        {{
            "path": "requirements.txt",
            "content": "..."
        }}
    ]
}}

Правила:

- максимум 2 файла
- максимум 150 строк на файл
- content всегда строка
- никаких markdown
- никаких ```json
- без комментариев
- без повторяющихся импортов
- только валидный JSON
"""
        )


        for attempt in range(
            self.MAX_FIX_ATTEMPTS
        ):

            print(
                f"\n=== QA ПРОВЕРКА {attempt + 1} ===\n"
            )


            review = self.qa.run(
                f"""
Проверь проект:

{state["code"]}

Найди:

1. Ошибки
2. Баги
3. Повторяющийся код
4. Лишние импорты
5. Риски

Если проблем нет:

OK
"""
            )


            state["review"] = review


            if "OK" in review.upper():

                print(
                    "\nQA: ошибок нет\n"
                )

                break


            print(
                "\n=== ИСПРАВЛЕНИЕ ===\n"
            )


            state["code"] = self.developer.run(
                f"""
Исправь проект.

Код:

{state["code"]}

Замечания QA:

{review}

Верни только JSON.

Формат:

{{
    "files": [
        {{
            "path": "app/main.py",
            "content": "..."
        }}
    ]
}}
"""
            )


        return state