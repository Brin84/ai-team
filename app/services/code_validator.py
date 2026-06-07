from pathlib import Path
import ast


class CodeValidator:

    PROJECT_PATH = Path(
        "generated_projects/project_1"
    )

    @classmethod
    def validate(
            cls
    ) -> list[dict]:

        errors = []

        files = cls.PROJECT_PATH.rglob(
            "*.py"
        )

        for file in files:
            code = ""
            try:

                code = file.read_text(
                    encoding="utf-8"
                )

                ast.parse(
                    code
                )

            except SyntaxError as e:

                errors.append(
                    {
                        "type": "syntax_error",
                        "file": str(
                            file.relative_to(
                                cls.PROJECT_PATH
                            )
                        ).replace(
                            "\\",
                            "/"
                        ),
                        "line": e.lineno,
                        "message": str(e),
                        "code": code
                    }
                )

            except Exception as e:

                errors.append(
                    {
                        "type": "validation_error",
                        "file": str(
                            file.relative_to(
                                cls.PROJECT_PATH
                            )
                        ).replace(
                            "\\",
                            "/"
                        ),
                        "message": str(e),
                        "code": code
                    }
                )

        return errors