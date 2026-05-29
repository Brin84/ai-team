import json
from pathlib import Path


class PatternService:

    FILE = Path(
        "patterns.json"
    )

    @classmethod
    def get_patterns(
        cls
    ) -> list:

        if not cls.FILE.exists():

            return []

        try:

            return json.loads(
                cls.FILE.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return []

    @classmethod
    def save_pattern(
        cls,
        task: str,
        architecture: str,
        files_count: int
    ):

        patterns = (
            cls.get_patterns()
        )

        pattern = {

            "task":
                str(task)[:300],

            "architecture":
                str(
                    architecture
                )[:500],

            "files_count":
                files_count
        }

        patterns.append(
            pattern
        )

        cls.FILE.write_text(
            json.dumps(
                patterns,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    @classmethod
    def get_best_patterns(
        cls,
        limit: int = 5
    ) -> list:

        patterns = (
            cls.get_patterns()
        )

        return patterns[
            -limit:
        ]