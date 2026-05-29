class RuntimeAnalyzer:

    @staticmethod
    def analyze(
        error: str
    ) -> str:

        error = str(
            error or ""
        ).lower()

        if (
            "no matching distribution found"
            in error
        ):

            return (
                "Используй только существующие пакеты "
                "из PyPI"
            )

        if (
            "could not find a version"
            in error
        ):

            return (
                "Проверяй существование пакета "
                "перед добавлением в requirements.txt"
            )

        if (
            "modulenotfounderror"
            in error
        ):

            return (
                "Не импортируй модули, "
                "которые не созданы в проекте"
            )

        if (
            "syntaxerror"
            in error
        ):

            return (
                "Проверяй синтаксис Python "
                "перед завершением генерации"
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
                "Используй os.getenv() "
                "для токенов"
            )

        if (
            "validationerror"
            in error
        ):

            return (
                "Не создавай обязательные настройки "
                "без значений по умолчанию"
            )

        if (
            "attributeerror"
            in error
        ):

            return (
                "Проверяй существование методов "
                "и атрибутов"
            )

        if (
            "typeerror"
            in error
        ):

            return (
                "Проверяй сигнатуры функций "
                "и типы аргументов"
            )

        return (
            "Проверяй проект перед запуском"
        )