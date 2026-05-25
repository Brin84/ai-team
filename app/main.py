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


def main():

    try:

        task = load_task()

    except Exception as e:

        print(
            f"\nОшибка загрузки задания: {e}"
        )

        return

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

    team = AITeam(
        planner=planner,
        architect=architect,
        developer=developer,
        qa=qa
    )

    result = team.run(
        task
    )

    print(
        "\n=== СОХРАНЕНИЕ ==="
    )

    if (

            not result.get("code")

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
            ["Неизвестная ошибка"]
        )

        for error in errors:

            print(error)

        try:

            HistoryService.save(
                result
            )

        except Exception:
            pass

        return

    success = FileWriter.save(
        result["code"]
    )

    if not success:

        try:

            HistoryService.save(
                result
            )

        except Exception:
            pass

        return

    print(
        "\n=== ПРОВЕРКА ===\n"
    )

    errors = (
        CodeValidator.validate()
    )

    if errors:

        for error in errors:

            print(error)

        result[
            "runtime_errors"
        ] = errors

        try:

            HistoryService.save(
                result
            )

        except Exception:
            pass

        return

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

            print(error)

        result[
            "runtime_errors"
        ] = import_errors

        try:

            HistoryService.save(
                result
            )

        except Exception:
            pass

        return

    print(
        "Ошибок импорта не найдено"
    )

    print(
        "\n=== ЗАПУСК ПРОЕКТА ===\n"
    )

    runtime = (
        ProjectRunner.run()
    )

    if runtime.get(
        "success"
    ):

        print(
            runtime.get(
                "stdout",
                ""
            )
        )

        try:

            HistoryService.save_success_pattern(
                result
            )

            print(
                "\nКоманда сохранила успешный паттерн"
            )

        except Exception as e:

            print(
                f"\nОшибка сохранения паттерна: {e}"
            )

    else:

        print(
            "\n=== RUNTIME QA ===\n"
        )

        print(
            runtime.get(
                "stderr",
                "Неизвестная ошибка"
            )
        )

        result[
            "runtime_errors"
        ] = [
            runtime.get(
                "stderr",
                "Неизвестная ошибка"
            )
        ]

        try:

            HistoryService.save(
                result
            )

        except Exception:
            pass


if __name__ == "__main__":

    main()