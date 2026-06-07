import json
import re


class ResponseValidator:

    REQUIRED_FILES = {

        "app/main.py",
        "requirements.txt"
    }

    PATCH_REQUIRED_KEYS = {
        "files"
    }

    FORBIDDEN_WORDS = [

        "selenium",
        "webdriver",
        "chromedriver"
    ]

    MIN_FILES = 2

    MAX_FILES = 50

    REQUIRED_FILE_KEYS = {

        "path",
        "content"
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

        if not isinstance(
                data,
                dict
        ):

            return (
                False,
                "Корневой JSON должен быть объектом"
            )

        if set(data.keys()) != cls.PATCH_REQUIRED_KEYS:

            return (
                False,
                (
                    "Корневой JSON должен "
                    "содержать только files"
                )
            )

        if "files" not in data:

            return (
                False,
                "Отсутствует ключ files"
            )

        files = data.get(
            "files",
            []
        )

        if not isinstance(
                files,
                list
        ):

            return (
                False,
                "files должен быть массивом"
            )

        if not files:

            return (
                False,
                "Пустой files"
            )

        is_patch = not cls.REQUIRED_FILES.issubset(
            {
                str(
                    file.get(
                        "path",
                        ""
                    )
                ).strip()

                for file in files

                if isinstance(
                    file,
                    dict
                )
            }
        )

        min_files = (
            1
            if is_patch
            else cls.MIN_FILES
        )

        if not (
                min_files
                <= len(files)
                <= cls.MAX_FILES
        ):

            return (
                False,
                (
                    "Количество файлов должно быть "
                    f"от {min_files} "
                    f"до {cls.MAX_FILES}"
                )
            )

        paths = []

        requirements = ""

        all_content = ""

        for file in files:

            if not isinstance(
                    file,
                    dict
            ):

                return (
                    False,
                    (
                        "Элемент files "
                        "должен быть объектом"
                    )
                )

            file_keys = set(
                file.keys()
            )

            if file_keys != cls.REQUIRED_FILE_KEYS:

                return (
                    False,
                    (
                        "Файл должен содержать "
                        "ТОЛЬКО ключи "
                        "'path' и 'content'"
                    )
                )

            path = str(
                file.get(
                    "path",
                    ""
                )
            ).strip()

            content = str(
                file.get(
                    "content",
                    ""
                )
            )

            if not path:

                return (
                    False,
                    "Файл без path"
                )

            if "\\" in path:

                return (
                    False,
                    (
                        "Путь должен "
                        "использовать "
                        "только /"
                    )
                )

            if path.startswith("/"):

                return (
                    False,
                    (
                        "Путь файла "
                        "не должен быть "
                        "абсолютным"
                    )
                )

            if "//" in path:

                return (
                    False,
                    (
                        "Путь файла "
                        "содержит //"
                    )
                )

            init_file = (
                path.endswith(
                    "__init__.py"
                )
            )

            if (
                    not content.strip()
                    and
                    not init_file
            ):

                return (
                    False,
                    f"Пустой content: {path}"
                )

            if (
                    is_patch
                    and
                    path in cls.REQUIRED_FILES
                    and
                    not content.strip()
            ):

                return (
                    False,
                    (
                        f"PATCH удаляет "
                        f"критический файл: {path}"
                    )
                )

            paths.append(
                path
            )

            all_content += (
                    "\n"
                    + content.lower()
            )

            if path == "requirements.txt":

                requirements = (
                    content.lower()
                )

        paths_set = set(
            paths
        )

        if (
                not is_patch
                and
                not cls.REQUIRED_FILES.issubset(
                    paths_set
                )
        ):

            missing = (
                    cls.REQUIRED_FILES
                    - paths_set
            )

            return (
                False,
                (
                    "Отсутствуют обязательные файлы: "
                    + ", ".join(
                        sorted(
                            missing
                        )
                    )
                )
            )

        if len(paths) != len(paths_set):

            return (
                False,
                "Обнаружены дубликаты файлов"
            )

        if "aiogram==" in requirements:

            return (
                False,
                (
                    "Запрещена фиксированная "
                    "версия aiogram"
                )
            )

        for word in cls.FORBIDDEN_WORDS:

            if word in all_content:

                return (
                    False,
                    (
                        f"Запрещено использовать: "
                        f"{word}"
                    )
                )

        bad_patterns = [

            "await dp.start_polling(",
            "await dispatcher.start_polling(",
            "updater(",
            "dispatcher(bot)",
            "use_context=",
            "filters.filters"
        ]

        for item in bad_patterns:

            if item in all_content:

                return (
                    False,
                    (
                        "Обнаружен legacy API: "
                        f"{item}"
                    )
                )

        if (

                "async def main(" in all_content

                and

                "asyncio.run(main())"
                not in all_content
        ):

            return (
                False,
                (
                    "async main должен "
                    "использовать "
                    "asyncio.run(main())"
                )
            )

        if response.count("{") != response.count("}"):

            return (
                False,
                "JSON содержит незакрытые объекты"
            )

        if response.count("[") != response.count("]"):

            return (
                False,
                "JSON содержит незакрытые массивы"
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
            r"\{[\s\S]*}",
            text
        )

        if not match:

            raise ValueError(
                "JSON не найден"
            )

        raw = match.group()

        return json.loads(
            raw
        )