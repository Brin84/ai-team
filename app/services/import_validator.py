from pathlib import Path
import importlib.util
import sys
import os


class ImportValidator:

    @staticmethod
    def validate():

        errors = []

        project_path = Path(
            "generated_projects/project_1"
        )

        old_path = os.getcwd()

        os.chdir(
            project_path
        )

        sys.path.insert(
            0,
            str(project_path)
        )

        try:

            for file in project_path.rglob(
                "*.py"
            ):

                try:

                    spec = importlib.util.spec_from_file_location(
                        file.stem,
                        file
                    )

                    module = importlib.util.module_from_spec(
                        spec
                    )

                    spec.loader.exec_module(
                        module
                    )

                except Exception as e:

                    errors.append(
                        f"{file}: {e}"
                    )

        finally:

            os.chdir(
                old_path
            )

        return errors