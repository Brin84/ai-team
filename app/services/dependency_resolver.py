from pathlib import Path


class DependencyResolver:

    IMPORT_TO_PACKAGE = {

        "dotenv": "python-dotenv",

        "google.oauth2": "google-auth",

        "googleapiclient": "google-api-python-client",

        "telegram": "python-telegram-bot",

        "gspread": "gspread",

        "oauth2client": "oauth2client",
    }

    @classmethod
    def resolve(
        cls,
        runtime_error: str
    ) -> list[str]:

        resolved = []

        error = runtime_error.lower()

        for import_name, package_name in (

            cls.IMPORT_TO_PACKAGE.items()

        ):

            if import_name.lower() in error:

                resolved.append(
                    package_name
                )

        return list(
            set(resolved)
        )

    @classmethod
    def apply(
        cls,
        packages: list[str]
    ) -> bool:

        if not packages:
            return False

        requirements_path = Path(
            "generated_projects/project_1/requirements.txt"
        )

        existing = []

        if requirements_path.exists():

            existing = requirements_path.read_text(
                encoding="utf-8"
            ).splitlines()

        normalized_existing = {

            line.strip().lower()

            for line in existing

            if line.strip()
        }

        updated = existing.copy()

        changed = False

        for package in packages:

            if package.lower() not in normalized_existing:

                updated.append(package)

                changed = True

        if not changed:
            return False

        requirements_path.write_text(
            "\n".join(updated) + "\n",
            encoding="utf-8"
        )

        return True