import json
import re


class ResponseValidator:

    ALLOWED_FILES = {
        "app/main.py",
        "requirements.txt"
    }

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
        main_content = ""

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

            if path == "requirements.txt":

                requirements = (
                    content.lower()
                )

            elif path == "app/main.py":

                main_content = (
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

        bad_patterns = [

            "await dp.start_polling(",
            "await dispatcher.start_polling("
        ]

        for item in bad_patterns:

            if item in main_content:

                return (
                    False,
                    f"Неверный aiogram запуск: {item}"
                )
        forbidden_patterns = [

            r"from\s+selenium",
            r"import\s+selenium",

            r"from\s+asyncpg",
            r"import\s+asyncpg",

            r"chromedriver",

            r"class\s+.*BaseSettings",
            r"Settings\("
        ]

        for pattern in forbidden_patterns:

            if re.search(
                    pattern,
                    main_content,
                    re.IGNORECASE
            ):
                return (
                    False,
                    f"Запрещено: {pattern}"
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
            r'({.*})',
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