import re
import sys


class RequirementsValidator:

    STDLIB = {

        module.lower()

        for module in (
            sys.stdlib_module_names
        )
    }

    REQUIRED_DEPENDENCIES = {

        "gspread": [
            "gspread"
        ],

        "dotenv": [
            "python-dotenv"
        ],

        "telegram": [
            "python-telegram-bot"
        ],

        "oauth2client": [
            "oauth2client"
        ],

        "googleapiclient": [
            "google-api-python-client"
        ],

        "google.oauth2": [
            "google-auth"
        ]
    }

    @classmethod
    def validate(
            cls,
            requirements_content: str
    ) -> list[str]:

        errors = []

        normalized_requirements = set()

        for line in requirements_content.splitlines():

            line = line.strip()

            if (
                    not line
                    or line.startswith("#")
            ):
                continue

            package = re.split(
                r"[<>=!~]",
                line
            )[0]

            package = (
                package
                .strip()
                .lower()
                .replace("-", "_")
            )

            normalized_requirements.add(
                package
            )

            if package in cls.STDLIB:

                errors.append(
                    f"stdlib модуль '{package}' "
                    f"не должен находиться "
                    f"в requirements.txt"
                )

        for import_name, packages in (
                cls.REQUIRED_DEPENDENCIES.items()
        ):

            found = False

            for package in packages:

                normalized = (
                    package
                    .lower()
                    .replace("-", "_")
                )

                if (
                        normalized
                        in normalized_requirements
                ):

                    found = True
                    break

            if not found:

                errors.append(
                    f"отсутствует dependency "
                    f"для импорта '{import_name}'"
                )

        return errors