import json
import re


class ResponseValidator:

    ALLOWED_FILES = {
        "app/main.py",
        "requirements.txt"
    }

    FORBIDDEN_WORDS = [

        "selenium",
        "webdriver",
        "chromedriver",

        "asyncpg",
        "psycopg",

        "database",
        "db_manager",

        "models",
        "model",

        "routers",
        "router",

        "repository",

        "services",

        "parser",
        "parsers",

        "basesettings",
        "configdict"
    ]

    @classmethod
    def validate(
        cls,
        response: str
    ):

        if not response:

            return (
                False,
                "Пустой ответ"
            )

        try:

            data = json.loads(
                response
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            try:

                data = cls.fix_json(
                    response
                )

            except (
                ValueError,
                json.JSONDecodeError
            ):

                return (
                    False,
                    "Невалидный JSON"
                )

        files = data.get(
            "files",
            []
        )

        if len(files) != 2:

            return (
                False,
                "Должно быть 2 файла"
            )

        paths = []

        requirements = ""
        all_content = ""

        for file in files:

            path = str(
                file.get(
                    "path",
                    ""
                )
            )

            content = str(
                file.get(
                    "content",
                    ""
                )
            )

            if not content:

                return (
                    False,
                    f"Пустой content: {path}"
                )

            paths.append(
                path
            )

            all_content += (
                "\n" +
                content.lower()
            )

            if path == "requirements.txt":

                requirements = (
                    content.lower()
                )

        if set(paths) != cls.ALLOWED_FILES:

            return (
                False,
                "Неверная структура"
            )

        if "aiogram==" in requirements:

            return (
                False,
                "Запрещена фиксированная версия aiogram"
            )

        for word in cls.FORBIDDEN_WORDS:

            if word in all_content:

                return (
                    False,
                    f"Запрещено использовать: {word}"
                )

        bad_patterns = [

            "await dp.start_polling(",
            "await dispatcher.start_polling("
        ]

        for item in bad_patterns:

            if item in all_content:

                return (
                    False,
                    f"Неверный aiogram запуск: {item}"
                )

        return (
            True,
            ""
        )

    @classmethod
    def fix_json(
        cls,
        text: str
    ):

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        match = re.search(
            r"({.*})",
            text,
            re.DOTALL
        )

        if not match:

            raise ValueError(
                "JSON не найден"
            )

        raw = match.group()

        return json.loads(
            raw
        )