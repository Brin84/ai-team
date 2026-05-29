class RuntimeAnalyzer:

    @staticmethod
    def analyze(
        error: str
    ) -> str:

        error = str(
            error or ""
        ).lower()

        if (
            "selenium"
            in error
        ):

            return (
                "Запрещено использовать selenium"
            )

        if (
            "chromedriver"
            in error
        ):

            return (
                "Запрещено использовать chromedriver"
            )

        if (
            "asyncpg"
            in error
        ):

            return (
                "Запрещено использовать asyncpg"
            )

        if (
            "psycopg-async"
            in error
        ):

            return (
                "Запрещено использовать несуществующий пакет psycopg-async"
            )

        if (
            "no matching distribution found"
            in error
        ):

            return (
                "Используй только существующие пакеты из PyPI"
            )

        if (
            "could not find a version"
            in error
        ):

            return (
                "Проверяй существование пакета перед добавлением в requirements.txt"
            )

        if (
            "modulenotfounderror"
            in error
        ):

            return (
                "Не импортируй модули которые не создаются в проекте"
            )

        if (
            "database"
            in error
        ):

            return (
                "Не импортируй database если файл database.py не создаётся"
            )

        if (
            "routers"
            in error
        ):

            return (
                "Не импортируй routers если файл routers.py не создаётся"
            )

        if (
            "models"
            in error
        ):

            return (
                "Не импортируй models если файл models.py не создаётся"
            )

        if (
            "config"
            in error
        ):

            return (
                "Не импортируй config если файл config.py не создаётся"
            )

        if (
            "syntaxerror"
            in error
        ):

            return (
                "Проверяй синтаксис Python перед завершением генерации"
            )

        if (
            "importerror"
            in error
        ):

            return (
                "Проверяй корректность импортов"
            )

        if (
            "tokenvalidationerror"
            in error
        ):

            return (
                "Используй os.getenv() для токенов"
            )

        if (
            "validationerror"
            in error
        ):

            return (
                "Не создавай обязательные настройки без значений по умолчанию"
            )

        if (
            "attributeerror"
            in error
        ):

            return (
                "Проверяй существование методов и атрибутов"
            )

        if (
            "typeerror"
            in error
        ):

            return (
                "Проверяй сигнатуры функций и типы аргументов"
            )

        return (
            "Проверяй проект перед запуском"
        )