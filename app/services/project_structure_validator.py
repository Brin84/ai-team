import json


class ProjectStructureValidator:

    @staticmethod
    def validate(
            architecture: str,
            project_json: str
    ) -> list[str]:

        errors = []

        try:

            architecture_data = json.loads(
                architecture
            )

            project_data = json.loads(
                project_json
            )

        except Exception:

            return [
                "Некорректный JSON"
            ]

        required_files = {

            str(path).replace(
                "\\",
                "/"
            ).strip()

            for path in architecture_data.get(
                "project_structure",
                []
            )

            if str(path).strip()
        }

        actual_files = {

            str(
                file.get(
                    "path",
                    ""
                )
            ).replace(
                "\\",
                "/"
            ).strip()

            for file in project_data.get(
                "files",
                []
            )

            if (
                isinstance(file, dict)
                and
                file.get("path")
            )
        }

        missing = (
            required_files
            - actual_files
        )

        optional_init_files = {

            "app/__init__.py",
            "app/api/__init__.py",
            "app/services/__init__.py",
            "app/models/__init__.py",
            "app/db/__init__.py",
            "app/utils/__init__.py"
        }

        missing = {

            file

            for file in missing

            if file not in optional_init_files
        }

        for file in sorted(
                missing
        ):

            errors.append(
                f"Отсутствует файл: {file}"
            )

        return errors