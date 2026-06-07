from typing import Any
import json

from app.services.history_service import (
    HistoryService
)

from app.services.response_validator import (
    ResponseValidator
)

from app.services.requirements_validator import (
    RequirementsValidator
)

from app.services.knowledge_service import (
    KnowledgeService
)

from app.services.json_repair_service import (
    JsonRepairService
)

from app.services.requirements_resolver import (
    RequirementsResolver
)

from app.services.prompt_builder import (
    PromptBuilder
)

from app.services.project_structure_validator import (
    ProjectStructureValidator
)

from app.services.package_validator import (
    PackageValidator
)

from app.services.python_syntax_validator import (
    PythonSyntaxValidator
)


class AITeam:

    MAX_JSON_FIX_ATTEMPTS = 6

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
            limit: int = 4000
    ) -> str:

        return str(
            text or ""
        )[:limit]

    @staticmethod
    def get_requirements_content(
            project_json: str
    ) -> str:

        try:

            data = json.loads(
                project_json
            )

        except (
                json.JSONDecodeError,
                TypeError
        ):

            return ""

        for file in data.get(
                "files",
                []
        ):

            if (
                    file.get("path")
                    == "requirements.txt"
            ):

                return str(
                    file.get(
                        "content",
                        ""
                    )
                )

        return ""

    @staticmethod
    def get_missing_files(
            architecture: str,
            project_json: str
    ) -> list[str]:

        try:

            architecture_data = json.loads(
                architecture
            )

            project_data = json.loads(
                project_json
            )

        except (
                json.JSONDecodeError,
                TypeError
        ):

            return []

        required_files = {

            str(path).strip()

            for path in architecture_data.get(
                "project_structure",
                []
            )
        }

        actual_files = {

            str(
                file.get(
                    "path",
                    ""
                )
            ).strip()

            for file in project_data.get(
                "files",
                []
            )

            if isinstance(
                    file,
                    dict
            )
        }

        return sorted(
            required_files
            - actual_files
        )

    @staticmethod
    def merge_projects(
            old_project_json: str,
            new_project_json: str
    ) -> str:

        try:

            old_data = json.loads(
                old_project_json
            )

            new_data = json.loads(
                new_project_json
            )

        except Exception:

            return new_project_json

        merged = {}

        for file in old_data.get(
                "files",
                []
        ):

            path = file.get(
                "path"
            )

            if path:

                content = str(
                    file.get(
                        "content",
                        ""
                    )
                ).strip()

                if not content and path in merged:
                    continue

                merged[path] = file

        for file in new_data.get(
                "files",
                []
        ):

            path = file.get(
                "path"
            )

            if not path:
                continue

            if path == "requirements.txt":

                old_content = (
                    merged.get(
                        path,
                        {}
                    ).get(
                        "content",
                        ""
                    )
                )

                new_content = file.get(
                    "content",
                    ""
                )

                file["content"] = (
                    RequirementsResolver
                    .merge_requirements(
                        old_content,
                        new_content
                    )
                )

            merged[path] = file

        return json.dumps(
            {
                "files": list(
                    merged.values()
                )
            },
            ensure_ascii=False,
            indent=2
        )

    def validate_project(
            self,
            architecture: str,
            project_json: str
    ) -> tuple[bool, str]:

        is_valid, error = (
            ResponseValidator.validate(
                project_json
            )
        )

        if not is_valid:

            return (
                False,
                error
            )

        requirements_content = (
            self.get_requirements_content(
                project_json
            )
        )

        requirements_errors = (
            RequirementsValidator.validate(
                requirements_content
            )
        )

        if requirements_errors:

            return (
                False,
                "\n".join(
                    requirements_errors
                )
            )

        structure_errors = (
            ProjectStructureValidator.validate(
                architecture=architecture,
                project_json=project_json
            )
        )

        if structure_errors:

            return (
                False,
                "\n".join(
                    structure_errors
                )
            )

        package_errors = (
            PackageValidator.validate(
                project_json
            )
        )

        if package_errors:

            return (
                False,
                "\n".join(
                    package_errors
                )
            )

        syntax_errors = (
            PythonSyntaxValidator.validate(
                project_json
            )
        )

        if syntax_errors:

            return (
                False,
                "\n".join(
                    syntax_errors
                )
            )

        return (
            True,
            ""
        )

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
            "runtime_errors": [],
            "last_valid_code": ""

        }

        team_errors = (
            HistoryService.get_known_errors()
        )

        success_patterns = ""

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
            1000
        )

        print(
            "\n=== АРХИТЕКТОР ===\n"
        )

        state["architecture"] = (
            JsonRepairService.extract_content(
                self.architect.run(
                    PromptBuilder.architect_prompt(
                        task=task,
                        plan=state["plan"],
                        team_errors=self.compress(
                            str(team_errors),
                            1000
                        ),
                        success_patterns=self.compress(
                            str(success_patterns),
                            1000
                        ),
                        knowledge=self.compress(
                            str(knowledge),
                            2000
                        )
                    )
                )
            )
        )

        try:

            architecture_data = json.loads(
                state["architecture"]
            )

        except Exception:

            state["runtime_errors"] = [
                "Архитектор вернул невалидный JSON"
            ]

            return state

        if not architecture_data.get(
                "project_structure"
        ):

            state["runtime_errors"] = [
                "Архитектор не вернул project_structure"
            ]

            return state

        developer_architecture = json.dumps(
            {
                "project_structure":
                    architecture_data.get(
                        "project_structure",
                        []
                    ),

                "requirements":
                    architecture_data.get(
                        "requirements",
                        []
                    )
            },
            ensure_ascii=False,
            indent=2
        )

        print(
            "\n=== РАЗРАБОТЧИК ===\n"
        )

        raw_response = (
            JsonRepairService.extract_content(
                self.developer.run(
                    PromptBuilder.developer_prompt(
                        task=task,
                        architecture=developer_architecture,
                        team_errors=self.compress(
                            str(team_errors),
                            1000
                        ),
                        success_patterns=self.compress(
                            str(success_patterns),
                            1000
                        ),
                        knowledge=self.compress(
                            str(knowledge),
                            2000
                        )
                    )
                )
            )
        )

        fixed_json = (
            JsonRepairService.repair_json(
                raw_response or ""
            )
        )

        fixed_json = (
            RequirementsResolver.resolve(
                fixed_json
            )
        )

        if fixed_json:

            state["code"] = fixed_json

            is_valid, _ = (
                self.validate_project(
                    developer_architecture,
                    fixed_json
                )
            )

            if is_valid:

                state["last_valid_code"] = (
                    fixed_json
                )

        print(
            "\n=== QA ===\n"
        )

        state["review"] = (
            JsonRepairService.extract_content(
                self.qa.run(
                    f"""
Проверь проект.

Задача:

{task}

Архитектура:

{developer_architecture}

Код:

{state['code']}

Найди:

- ошибки архитектуры
- отсутствующие зависимости
- несуществующие импорты
- проблемы запуска

Верни JSON.
"""
                )
            )
        )

        short_review = self.compress(
            state["review"],
            1500
        )

        for _ in range(
                self.MAX_JSON_FIX_ATTEMPTS
        ):

            is_valid, error = (
                self.validate_project(
                    developer_architecture,
                    state["code"]
                )
            )

            if is_valid:

                state["runtime_errors"] = []

                return state

            print(
                f"\nОшибка ответа: {error}"
            )

            missing_files = (
                self.get_missing_files(
                    architecture=developer_architecture,
                    project_json=state["code"]
                )
            )

            raw_response = (
                JsonRepairService.extract_content(
                    self.developer.run(
                        PromptBuilder.fix_prompt(
                            architecture=developer_architecture,
                            error=error,
                            task=task,
                            previous_code=(
                                    state.get(
                                        "last_valid_code"
                                    )
                                    or state.get(
                                "code"
                            )
                                    or ""
                            ),
                            review=short_review,
                            knowledge=self.compress(
                                str(knowledge),
                                2000
                            ),
                            missing_files=missing_files
                        )
                    )
                )
            )

            fixed_json = (
                JsonRepairService.repair_json(
                    raw_response or ""
                )
            )

            if not fixed_json:
                continue

            base_project = (
                    state.get(
                        "last_valid_code"
                    )
                    or state.get(
                "code"
            )
                    or "{}"
            )

            merged_project = (
                self.merge_projects(
                    base_project,
                    fixed_json
                )
            )

            merged_project = (
                RequirementsResolver.resolve(
                    merged_project
                )
            )

            state["code"] = merged_project

            is_valid_after_merge, _ = (
                self.validate_project(
                    developer_architecture,
                    merged_project
                )
            )

            if is_valid_after_merge:

                state["last_valid_code"] = (
                    merged_project
                )

        state["runtime_errors"] = [
            "Не удалось получить валидный JSON"
        ]

        return state