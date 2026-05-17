from pathlib import Path
import ast


class CodeValidator:

    @staticmethod
    def validate():

        errors = []

        files = Path(
            "app"
        ).rglob(
            "*.py"
        )

        for file in files:

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    code = f.read()

                ast.parse(
                    code
                )

            except Exception as e:

                errors.append(
                    f"{file}: {e}"
                )

        return errors