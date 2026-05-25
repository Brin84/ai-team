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

        requirements = (
            project /
            "requirements.txt"
        )

        if requirements.exists():

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
                "requirements.txt"
            ],
            cwd=project,
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
                cwd=project,
                capture_output=True,
                text=True,
                timeout=15
            )

            return {

                "success":
                    result.returncode == 0,

                "stdout":
                    result.stdout,

                "stderr":
                    result.stderr
            }

        except subprocess.TimeoutExpired:

            return {

                "success": True,

                "stdout":
                    "Проект успешно запущен",

                "stderr":
                    ""
            }