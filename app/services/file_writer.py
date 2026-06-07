import json
import shutil
from pathlib import Path


class FileWriter:

    BASE_DIR = Path(
        "generated_projects/project_1"
    ).resolve()

    @classmethod
    def clear_project(
            cls
    ):

        if cls.BASE_DIR.exists():

            shutil.rmtree(
                cls.BASE_DIR
            )

        cls.BASE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    @classmethod
    def save(
            cls,
            response: str,
            clear_project: bool = False
    ):

        try:

            if clear_project:

                cls.clear_project()

            else:

                cls.BASE_DIR.mkdir(
                    parents=True,
                    exist_ok=True
                )

            response = (
                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            data = json.loads(
                response
            )

            files = data.get(
                "files",
                []
            )

            if not files:

                raise Exception(
                    "Файлы не найдены"
                )

            created_files = []

            for file_data in files:

                if not isinstance(
                        file_data,
                        dict
                ):
                    continue

                path = str(
                    file_data.get(
                        "path",
                        ""
                    )
                ).strip()

                content = str(
                    file_data.get(
                        "content",
                        ""
                    )
                )

                if not path:
                    continue

                full_path = (
                        cls.BASE_DIR
                        / Path(path)
                ).resolve()

                if not str(
                        full_path
                ).startswith(
                    str(cls.BASE_DIR)
                ):

                    raise Exception(
                        f"Недопустимый путь: {path}"
                    )

                full_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                with open(
                        full_path,
                        "w",
                        encoding="utf-8"
                ) as f:

                    f.write(
                        content
                    )

                created_files.append(
                    str(full_path)
                )

            print(
                "\nСозданы файлы:\n"
            )

            for file in created_files:

                print(
                    f"✓ {file}"
                )

            return True

        except Exception as e:

            print(
                f"\nОшибка сохранения:\n{e}"
            )

            print(
                "\n=== ОТВЕТ ===\n"
            )

            print(
                response[:3000]
            )

            return False