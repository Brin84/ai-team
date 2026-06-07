import json


class PackageValidator:

    REQUIRED_PACKAGES = {

        "app/__init__.py"
    }

    @classmethod
    def validate(
            cls,
            project_json: str
    ) -> list[str]:

        try:

            data = json.loads(
                project_json
            )

        except Exception:

            return [
                "Некорректный JSON"
            ]

        files = data.get(
            "files",
            []
        )

        paths = {

            str(
                file.get(
                    "path",
                    ""
                )
            ).replace(
                "\\",
                "/"
            )

            for file in files

            if isinstance(
                file,
                dict
            )
        }

        errors = []

        for required in (
                cls.REQUIRED_PACKAGES
        ):

            if required not in paths:

                errors.append(
                    f"Отсутствует {required}"
                )

        return errors