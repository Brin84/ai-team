import re
from pathlib import Path


class FileWriter:

    BASE_DIR = Path(
        "generated_projects/project_1"
    )

    @classmethod
    def save(
        cls,
        response: str
    ):

        try:

            response = response or ""

            response = response.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            )

            response = response.strip()

            # Ищем все завершённые file-блоки
            file_matches = re.findall(
                r'\{\s*"path"\s*:\s*"([^"]+)"\s*,\s*"content"\s*:\s*"([\s\S]*?)"\s*}',
                response
            )

            if not file_matches:
                raise Exception(
                    "Файлы не найдены"
                )

            created_files = []

            for path, content in file_matches:

                content = content.encode(
                    "utf-8"
                ).decode(
                    "unicode_escape"
                )

                full_path = (
                    cls.BASE_DIR /
                    Path(path)
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

                    f.write(content)

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
                response[:1500]
            )

            return False