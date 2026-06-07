import subprocess
from pathlib import Path
import sys


class ProjectRunner:

    SAFE_REQUIREMENTS = {

        "aiogram":
            "aiogram>=3.28.2",

        "fastapi":
            "fastapi>=0.136",

        "uvicorn":
            "uvicorn>=0.35",

        "pydantic-settings":
            "pydantic-settings>=2.10"
    }

    @classmethod
    def fix_requirements(
            cls,
            project: Path
    ):

        requirements = (
            project /
            "requirements.txt"
        )

        packages = {}

        if requirements.exists():

            with open(
                    requirements,
                    "r",
                    encoding="utf-8"
            ) as f:

                for line in f:

                    line = line.strip()

                    if not line:
                        continue

                    package = (
                        line
                        .split("==")[0]
                        .split(">=")[0]
                        .split("<=")[0]
                        .strip()
                        .lower()
                    )

                    packages[
                        package
                    ] = line

        packages.update(
            cls.SAFE_REQUIREMENTS
        )

        with open(
                requirements,
                "w",
                encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(
                    sorted(
                        packages.values()
                    )
                )
            )

    @classmethod
    def run(
            cls
    ):

        project = Path(
            "generated_projects/project_1"
        )

        if not project.exists():

            return {

                "success": False,

                "stdout": "",

                "stderr":
                    "Проект не найден"
            }

        requirements = (
            project /
            "requirements.txt"
        )

        if not requirements.exists():

            return {

                "success": False,

                "stdout": "",

                "stderr":
                    "requirements.txt не найден"
            }

        cls.fix_requirements(
            project
        )

        print(
            "\nУстановка зависимостей...\n"
        )

        install = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(requirements.name)
            ],
            cwd=str(project),
            capture_output=True,
            text=True
        )

        if install.returncode != 0:

            return {

                "success": False,

                "stdout":
                    install.stdout,

                "stderr":
                    install.stderr
            }

        print(
            "\nЗапуск проекта...\n"
        )

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "app.main"
                ],
                cwd=str(project),
                capture_output=True,
                text=True,
                timeout=15
            )

            stdout = (
                    result.stdout or ""
            )

            stderr = (
                    result.stderr or ""
            )

            combined = (
                    stdout +
                    stderr
            ).lower()

            runtime_errors = [

                "traceback",
                "syntaxerror",
                "modulenotfounderror",
                "importerror",
                "attributeerror",
                "typeerror",
                "nameerror"
            ]

            has_runtime_error = any(
                item in combined
                for item in runtime_errors
            )

            return {

                "success":
                    not has_runtime_error,

                "stdout":
                    stdout,

                "stderr":
                    stderr
            }

        except subprocess.TimeoutExpired:

            return {

                "success": True,

                "stdout":
                    "Проект успешно запущен",

                "stderr": ""
            }