import subprocess
from pathlib import Path
import sys
import time


class ProjectRunner:

    @staticmethod
    def install_requirements(project: Path):

        requirements = project / "requirements.txt"

        if not requirements.exists():
            print("\nrequirements.txt не найден\n")
            return

        print("\nУстановка зависимостей...\n")

        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt"
            ],
            cwd=project
        )


    @classmethod
    def run(cls):

        project = Path(
            "generated_projects/project_1"
        )

        cls.install_requirements(
            project
        )

        try:

            print(
                "\nЗапуск проекта...\n"
            )

            process = subprocess.Popen(
                [
                    sys.executable,
                    "main.py"
                ],
                cwd=project,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            time.sleep(3)

            if process.poll() is not None:

                stdout, stderr = process.communicate()

                return {
                    "success": False,
                    "stdout": stdout,
                    "stderr": stderr
                }

            return {
                "success": True,
                "stdout": (
                    f"Процесс запущен PID={process.pid}"
                ),
                "stderr": ""
            }

        except Exception as e:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(e)
            }