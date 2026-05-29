from pathlib import Path
import re


class ImportValidator:

    @classmethod
    def validate(
        cls
    ):

        errors = []

        project_path = Path(
            "generated_projects/project_1"
        )

        python_files = list(
            project_path.rglob(
                "*.py"
            )
        )

        existing_modules = {

            file.stem
            for file in python_files

        }

        forbidden_local_modules = {

            "database",
            "models",
            "routers",
            "config",
            "settings",
            "services",
            "repository",
            "repositories",
            "parser",
            "parsers"
        }

        for file in python_files:

            try:

                content = file.read_text(
                    encoding="utf-8"
                )

            except Exception as e:

                errors.append(
                    f"{file}: {e}"
                )

                continue

            from_imports = re.findall(
                r"from\s+([a-zA-Z0-9_.]+)\s+import",
                content
            )

            normal_imports = re.findall(
                r"^import\s+([a-zA-Z0-9_.]+)",
                content,
                re.MULTILINE
            )

            imports = (
                from_imports +
                normal_imports
            )

            for module in imports:

                root = (
                    module
                    .split(".")[0]
                    .strip()
                    .lower()
                )

                if root in forbidden_local_modules:

                    errors.append(
                        f"{file}: модуль '{root}' запрещён"
                    )

        return errors