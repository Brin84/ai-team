from pathlib import Path

from app.services.agent_factory import (
    AgentFactory
)

from app.services.team import (
    AITeam
)

from app.services.file_writer import (
    FileWriter
)

from app.services.code_validator import (
    CodeValidator
)

from app.services.import_validator import (
    ImportValidator
)

from app.services.project_runner import (
    ProjectRunner
)

from app.services.history_service import (
    HistoryService
)

from app.services.runtime_analyzer import (
    RuntimeAnalyzer
)

from app.services.knowledge_service import (
    KnowledgeService
)

from app.services.pattern_service import (
    PatternService
)

from app.services.prompt_builder import (
    PromptBuilder
)

from app.services.json_repair_service import (
    JsonRepairService
)

from app.services.dependency_resolver import (
    DependencyResolver
)

from app.services.patch_scope_validator import (
    PatchScopeValidator
)

from app.services.architecture_validator import (
    ArchitectureValidator
)

from app.services.missing_file_resolver import (
    MissingFileResolver
)

MAX_RUNTIME_FIX_ATTEMPTS = 2


class RepairType:

    DEPENDENCY = "dependency"

    IMPORT = "import"

    SYNTAX = "syntax"

    RUNTIME = "runtime"

    JSON = "json"


def load_task() -> str:

    task_file = Path(
        "task.txt"
    )

    if not task_file.exists():

        raise FileNotFoundError(
            "task.txt не найден"
        )

    return task_file.read_text(
        encoding="utf-8"
    )


def save_history_safe(
    result
):

    try:

        HistoryService.save(
            result
        )

    except Exception:
        pass


def save_pattern_safe(
    result
):

    try:

        project_dir = Path(
            "generated_projects/project_1"
        )

        files_count = len(
            [
                file
                for file in project_dir.rglob("*")
                if file.is_file()
            ]
        )

        PatternService.save_pattern(
            task=result.get(
                "task",
                ""
            ),
            architecture=result.get(
                "architecture",
                ""
            ),
            files_count=files_count
        )

    except Exception as e:

        print(
            f"\nОшибка сохранения шаблона: {e}"
        )


def detect_repair_type(
    runtime_error: str
) -> str:

    error = runtime_error.lower()

    dependency_markers = [

        "missing dependency",

        "отсутствует dependency",

        "no module named",

        "modulenotfounderror",

        "could not find a version that satisfies the requirement",

        "no matching distribution found",

        "pip",

        "requires",

        "requirement",

        "dependency",
    ]

    import_markers = [

        "cannot import",
        "importerror",
        "cannot import name",
        "internal import",
    ]

    syntax_markers = [

        "syntaxerror",
        "indentationerror",
    ]

    if any(
        marker in error
        for marker in dependency_markers
    ):
        return RepairType.DEPENDENCY

    if any(
        marker in error
        for marker in import_markers
    ):
        return RepairType.IMPORT

    if any(
        marker in error
        for marker in syntax_markers
    ):
        return RepairType.SYNTAX

    return RepairType.RUNTIME

def extract_missing_files(
    runtime_error: str
) -> list[str]:

    missing_files = []

    for line in runtime_error.splitlines():

        normalized = line.strip()

        if not normalized:
            continue

        if (
            "отсутствует файл:" in normalized.lower()
        ):

            try:

                file_path = (
                    normalized.split(
                        ":",
                        1
                    )[1]
                    .strip()
                )

                if file_path:

                    missing_files.append(
                        file_path
                    )

            except Exception:
                pass

    return missing_files

def extract_missing_internal_imports(
    runtime_error: str
) -> list[str]:

    missing = []

    for line in runtime_error.splitlines():

        normalized = line.strip()

        if (
            "internal import" not in normalized
            or
            "не существует" not in normalized
        ):

            continue

        try:

            import_name = (
                normalized.split(
                    "internal import '"
                )[1]
                .split("'")[0]
            )

            missing.append(
                import_name
            )

        except Exception:
            pass

    return missing

def create_team():

    factory = AgentFactory()

    planner = factory.create_agent(
        "Создай технического руководителя",
        "planner"
    )

    architect = factory.create_agent(
        "Создай Telegram архитектора",
        "architect"
    )

    developer = factory.create_agent(
        "Создай senior Python разработчика",
        "developer"
    )

    qa = factory.create_agent(
        "Создай QA инженера",
        "qa"
    )

    return AITeam(
        planner=planner,
        architect=architect,
        developer=developer,
        qa=qa
    )


def validate_project(
    result
):

    print(
        "\n=== ПРОВЕРКА ===\n"
    )

    errors = (
        CodeValidator.validate()
    )

    if errors:

        for error in errors:

            if isinstance(error, dict):

                print(
                    f"{error.get('file')}: "
                    f"{error.get('message')}"
                )

            else:

                print(error)

        return errors

    print(
        "Ошибок не найдено"
    )

    print(
        "\n=== ИМПОРТЫ ===\n"
    )

    import_errors = (
        ImportValidator.validate()
    )

    if import_errors:

        for error in import_errors:

            if isinstance(error, dict):

                print(
                    f"{error.get('file')}: "
                    f"{error.get('message')}"
                )

            else:

                print(error)

        return import_errors

    print(
        "Ошибок импорта не найдено"
    )

    return []


def save_project(
    result
) -> bool:

    print(
        "\n=== СОХРАНЕНИЕ ==="
    )

    if (

        not result.get(
            "code"
        )

        or

        result.get(
            "runtime_errors"
        )

    ):

        print(
            "\nПроект не сохранён"
        )

        errors = result.get(
            "runtime_errors",
            [
                "Неизвестная ошибка"
            ]
        )

        for error in errors:
            print(error)

        return False

    success = FileWriter.save(
        result["code"],
        clear_project=True
    )

    return success


def runtime_fix_loop(
    team,
    result
):

    for attempt in range(
        MAX_RUNTIME_FIX_ATTEMPTS
    ):

        print(
            "\n=== ЗАПУСК ПРОЕКТА ===\n"
        )

        runtime = (
            ProjectRunner.run()
        )

        if runtime.get(
            "success"
        ):

            stdout = runtime.get(
                "stdout",
                ""
            )

            if stdout:
                print(stdout)

            try:

                HistoryService.save_success_pattern(
                    result
                )

                save_pattern_safe(
                    result
                )

                print(
                    "\nКоманда сохранила успешный паттерн"
                )

            except Exception as e:

                print(
                    f"\nОшибка сохранения паттерна: {e}"
                )

            return True

        print(
            "\n=== RUNTIME QA ===\n"
        )

        validation_errors = result.get(
            "runtime_errors",
            []
        )

        if validation_errors:

            runtime_error = "\n".join(

                str(error)

                for error in validation_errors
            )

        else:

            runtime_error = runtime.get(
                "stderr",
                "Неизвестная ошибка"
            )

        broken_file = ""
        broken_code = ""

        validation_errors = result.get(
            "runtime_errors",
            []
        )

        if validation_errors:

            first_error = validation_errors[0]

            if isinstance(
                    first_error,
                    dict
            ):
                broken_file = first_error.get(
                    "file",
                    ""
                )

                broken_code = first_error.get(
                    "code",
                    ""
                )

        if not broken_file:

            runtime_stderr = runtime.get(
                "stderr",
                ""
            )

            runtime_lines = runtime_stderr.splitlines()

            for line in runtime_lines:

                normalized = line.strip()

                if ".py" not in normalized:
                    continue

                if "File " in normalized:

                    try:

                        file_part = (
                            normalized.split(
                                'File "'
                            )[1]
                        )

                        extracted = (
                            file_part.split('"')[0]
                        )

                        extracted = extracted.replace(
                            "\\",
                            "/"
                        )

                        if extracted.endswith(".py"):
                            broken_file = extracted

                            break

                    except Exception:
                        pass

        print(
            runtime_error
        )

        repair_type = detect_repair_type(
            runtime_error
        )

        print(
            f"\nТип исправления: {repair_type}"
        )

        result["runtime_errors"] = validation_errors

        missing_files = extract_missing_files(
            runtime_error
        )

        if missing_files:

            print(
                "\n=== MISSING FILE REPAIR ===\n"
            )

            created = (
                MissingFileResolver.create(
                    missing_files
                )
            )

            if created:

                print(
                    f"Созданы файлы: {created}"
                )

            else:

                print(
                    "Не удалось создать файлы"
                )

            validation_errors = (
                validate_project(
                    result
                )
            )

            if validation_errors:
                result[
                    "runtime_errors"
                ] = validation_errors

            continue

        if repair_type == RepairType.DEPENDENCY:

            print(
                "\n=== DEPENDENCY REPAIR ===\n"
            )

            packages = (
                DependencyResolver.resolve(
                    runtime_error
                )
            )

            if not packages:
                print(
                    "Не удалось определить dependency"
                )

                continue

            print(
                f"Найдены зависимости: {packages}"
            )

            applied = (
                DependencyResolver.apply(
                    packages
                )
            )

            if not applied:
                print(
                    "Зависимости уже существуют"
                )

            validation_errors = (
                validate_project(
                    result
                )
            )

            if validation_errors:
                result[
                    "runtime_errors"
                ] = validation_errors

            continue

        try:

            rule = (
                RuntimeAnalyzer.analyze(
                    runtime_error
                )
            )

            if rule:

                KnowledgeService.save_rule(
                    rule
                )

                print(
                    "\nНовое знание сохранено:"
                )

                print(rule)

        except Exception as e:

            print(
                f"\nОшибка анализа: {e}"
            )

        print(
            "\n=== RUNTIME FIX ===\n"
        )

        repair_context = {

            "error": runtime_error,

            "broken_file": broken_file,

            "broken_code": broken_code,

            "repair_type": repair_type,
        }

        if repair_type == RepairType.DEPENDENCY:

            repair_context[
                "allowed_files"
            ] = [
                "requirements.txt"
            ]

        else:

            repair_context[
                "allowed_files"
            ] = [
                broken_file
            ]

        raw_response = (
            JsonRepairService.extract_content(
                team.developer.run(
                    PromptBuilder.fix_prompt(
                        task="PATCH MODE",
                        architecture="PATCH ONLY",
                        error=str(
                            repair_context
                        ),
                        previous_code=broken_code,
                        broken_file=broken_file,
                        review="",
                        knowledge=""
                    )
                )
            )
        )

        fixed_code = (
            JsonRepairService.repair_json(
                raw_response
            )
        )

        if not fixed_code:
            print(
                "\nНе удалось исправить проект"
            )

            continue

        if not isinstance(
                fixed_code,
                dict
        ):
            print(
                "\nНекорректный тип patch response"
            )

            print(
                f"Получен тип: {type(fixed_code)}"
            )

            continue

        if "files" not in fixed_code:
            print(
                "\nPatch response не содержит files"
            )

            continue

        if not isinstance(
                fixed_code["files"],
                list
        ):
            print(
                "\nПоле files должно быть списком"
            )

            continue

        patch_files = [

            file.get("path", "")

            for file in fixed_code.get(
                "files",
                []
            )

            if isinstance(file, dict)
        ]

        allowed_files = []

        if broken_file:
            allowed_files.append(
                broken_file
            )

        if repair_type == RepairType.DEPENDENCY:
            allowed_files.append(
                "requirements.txt"
            )

        is_valid_scope, violations = (
            PatchScopeValidator.validate(
                patch_files=patch_files,
                allowed_files=allowed_files
            )
        )

        architecture_paths = []

        architecture = result.get(
            "architecture",
            {}
        )

        if isinstance(
                architecture,
                dict
        ):
            architecture_paths = architecture.get(
                "project_structure",
                []
            )

        is_valid_architecture, invalid_paths = (
            ArchitectureValidator.validate_paths(
                patch_files=patch_files,
                allowed_paths=architecture_paths
            )
        )

        if not is_valid_architecture:

            print(
                "\n=== ARCHITECTURE VIOLATION ===\n"
            )

            for invalid_path in invalid_paths:
                print(
                    f"Недопустимый путь: {invalid_path}"
                )

            continue

        if not is_valid_scope:

            print(
                "\n=== PATCH SCOPE VIOLATION ===\n"
            )

            for violation in violations:
                print(
                    f"Запрещённое изменение: {violation}"
                )

            continue

        result["code"] = fixed_code

        success = FileWriter.save(
            result["code"],
            clear_project=False
        )

        if not success:

            print(
                "\nОшибка сохранения исправленного проекта"
            )

            continue

        validation_errors = (
            validate_project(
                result
            )
        )

        if validation_errors:

            result[
                "runtime_errors"
            ] = validation_errors

            continue

    return False


def main():

    try:

        task = load_task()

    except Exception as e:

        print(
            f"\nОшибка загрузки задания: {e}"
        )

        return

    team = create_team()

    result = team.run(
        task
    )

    success = save_project(
        result
    )

    if not success:

        save_history_safe(
            result
        )

        return

    validation_errors = (
        validate_project(
            result
        )
    )

    if validation_errors:

        result[
            "runtime_errors"
        ] = validation_errors

        save_history_safe(
            result
        )

        return

    runtime_success = (
        runtime_fix_loop(
            team,
            result
        )
    )

    if not runtime_success:

        save_history_safe(
            result
        )


if __name__ == "__main__":

    main()