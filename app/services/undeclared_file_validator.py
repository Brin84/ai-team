import json


class UndeclaredFileValidator:

    @classmethod
    def validate(
            cls,
            architecture: str,
            project_json: str
    ) -> list[str]:

        try:

            architecture_data = json.loads(
                architecture
            )

            project_data = json.loads(
                project_json
            )

        except Exception:

            return [
                "Ошибка чтения JSON"
            ]

        allowed_files = set(

            architecture_data.get(
                "project_structure",
                []
            )
        )

        project_files = {

            file.get(
                "path",
                ""
            )

            for file in project_data.get(
                "files",
                []
            )
        }

        errors = []

        for file_path in project_files:

            if (
                    file_path
                    and
                    file_path
                    not in allowed_files
                    and
                    file_path != "requirements.txt"
            ):

                errors.append(
                    (
                        "Файл отсутствует "
                        "в architecture.project_structure: "
                        f"{file_path}"
                    )
                )

        return errors