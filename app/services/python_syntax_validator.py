import ast
import json


class PythonSyntaxValidator:

    @staticmethod
    def validate(
            project_json: str
    ) -> list[str]:

        errors = []

        try:

            data = json.loads(
                project_json
            )

        except Exception:

            return [
                "Некорректный JSON"
            ]

        for file in data.get(
                "files",
                []
        ):

            path = file.get(
                "path",
                ""
            )

            content = file.get(
                "content",
                ""
            )

            if not path.endswith(".py"):

                continue

            try:

                ast.parse(content)

            except SyntaxError as error:

                errors.append(
                    f"{path}: syntax error "
                    f"line {error.lineno}"
                )

        return errors