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

def main():

    factory = AgentFactory()


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
        architect=architect,
        developer=developer,
        qa=qa
    )


    result = team.run(
        """
Создать Telegram бота
для обработки заявок клиентов
с использованием:

- FastAPI
- PostgreSQL
- aiogram
"""
    )


    print(
        "\n=== СОХРАНЕНИЕ ==="
    )


    success = FileWriter.save(
        result["code"]
    )


    if success:

        errors = CodeValidator.validate()

        print(
            "\n=== ПРОВЕРКА ===\n"
        )

        if errors:

            for error in errors:

                print(
                    error
                )

        else:

            print(
                "Ошибок не найдено"
            )


        import_errors = ImportValidator.validate()

        print(
            "\n=== ИМПОРТЫ ===\n"
        )

        if import_errors:

            for error in import_errors:
                print(error)

        else:

            print(
                "Ошибок импорта не найдено"
            )



        print(
            "\n=== ЗАПУСК ПРОЕКТА ===\n"
        )

        result = ProjectRunner.run()

        if result["success"]:

            print(
                "Проект стартовал"
            )

        else:

            print(
                result["stderr"]
            )
if __name__ == "__main__":
    main()