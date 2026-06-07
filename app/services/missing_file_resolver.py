from pathlib import Path


class MissingFileResolver:

    @staticmethod
    def create(
        missing_files: list[str]
    ) -> list[str]:

        created = []

        project_root = Path(
            "generated_projects/project_1"
        )

        for relative_path in missing_files:

            file_path = (
                project_root / relative_path
            )

            try:

                file_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                if not file_path.exists():

                    file_path.write_text(
                        "",
                        encoding="utf-8"
                    )

                    created.append(
                        relative_path
                    )

            except Exception as e:

                print(
                    f"\nОшибка создания файла "
                    f"{relative_path}: {e}"
                )

        return created