from typing import Any

from app.services.history_service import (
    HistoryService
)

from app.services.response_validator import (
    ResponseValidator
)

from app.services.knowledge_service import (
    KnowledgeService
)

from app.services.json_repair_service import (
    JsonRepairService
)

from app.services.prompt_builder import (
    PromptBuilder
)


class AITeam:

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

        success_patterns = []

        knowledge = (
            KnowledgeService.get_rules()
        )

        print(
            "\n=== ПЛАНИРОВЩИК ===\n"
        )

        state["plan"] = self.compress(
            JsonRepairService.extract_content(
                self.planner.run(
                    PromptBuilder.planner_prompt(
                        task
                    )
                )
            ),
            400
        )

        print(
            "\n=== АРХИТЕКТОР ===\n"
        )

        state["architecture"] = self.compress(
            JsonRepairService.extract_content(
                self.architect.run(
                    PromptBuilder.architect_prompt(
                        task=task,
                        plan=state["plan"],
                        team_errors=team_errors,
                        success_patterns=success_patterns,
                        knowledge=knowledge
                    )
                )
            )
        )

        print(
            "\n=== РАЗРАБОТЧИК ===\n"
        )

        raw_response = (
            JsonRepairService.extract_content(
                self.developer.run(
                    PromptBuilder.developer_prompt(
                        task=task,
                        architecture=state["architecture"],
                        team_errors=team_errors,
                        success_patterns=success_patterns,
                        knowledge=knowledge
                    )
                )
            )
        )

        state["code"] = (
            JsonRepairService.repair_json(
                raw_response
            )
        )

        for _ in range(
            self.MAX_JSON_FIX_ATTEMPTS
        ):

            if (
                JsonRepairService.is_empty_response(
                    state["code"]
                )
            ):

                error = (
                    "Пустой ответ"
                )

            else:

                is_valid, error = (
                    ResponseValidator.validate(
                        state["code"]
                    )
                )

                if is_valid:

                    state["runtime_errors"] = []

                    return state

            print(
                f"\nОшибка ответа: {error}"
            )

            print(
                "\n=== RAW RESPONSE ===\n"
            )

            print(
                state["code"]
            )

            raw_response = (
                JsonRepairService.extract_content(
                    self.developer.run(
                        PromptBuilder.fix_prompt(
                            error=error,
                            previous_code=state["code"],
                            knowledge = knowledge[:2000]
                        )
                    )
                )
            )

            print(
                "\n=== RAW MODEL RESPONSE ===\n"
            )

            print(
                raw_response
            )

            state["code"] = (
                JsonRepairService.repair_json(
                    raw_response
                )
            )

        state["runtime_errors"] = [
            "Не удалось получить валидный JSON"
        ]

        state["code"] = ""

        return state