import json
from pathlib import Path
from datetime import datetime


class HistoryService:

    FILE = Path(
        "team_memory.json"
    )


    @classmethod
    def load(
        cls
    ) -> list:

        if not cls.FILE.exists():

            return []

        try:

            with open(
                cls.FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(
                    f
                )

        except Exception:

            return []


    @classmethod
    def save_file(
        cls,
        history: list
    ):

        with open(
            cls.FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                ensure_ascii=False,
                indent=4
            )


    @classmethod
    def save(
        cls,
        state: dict
    ):

        history = cls.load()

        history.append(
            {
                "created_at":
                    datetime.now().isoformat(),

                "success":
                    False,

                "task":
                    state.get(
                        "task",
                        ""
                    ),

                "architecture":
                    state.get(
                        "architecture",
                        ""
                    ),

                "review":
                    state.get(
                        "review",
                        ""
                    ),

                "runtime_errors":
                    state.get(
                        "runtime_errors",
                        []
                    )
            }
        )

        cls.save_file(
            history
        )


    @classmethod
    def save_success_pattern(
        cls,
        state: dict
    ):

        history = cls.load()

        history.append(
            {
                "created_at":
                    datetime.now().isoformat(),

                "success":
                    True,

                "task":
                    state.get(
                        "task",
                        ""
                    ),

                "plan":
                    state.get(
                        "plan",
                        ""
                    ),

                "architecture":
                    state.get(
                        "architecture",
                        ""
                    )
            }
        )

        cls.save_file(
            history
        )


    @classmethod
    def get_known_errors(
        cls
    ) -> str:

        history = cls.load()

        errors = []

        for item in history:

            review = item.get(
                "review",
                ""
            )

            runtime = item.get(
                "runtime_errors",
                []
            )

            if review:

                errors.append(
                    review
                )

            if runtime:

                errors.extend(
                    runtime
                )

        return "\n".join(
            errors[-10:]
        )


    @classmethod
    def get_success_patterns(
        cls
    ) -> list:

        history = cls.load()

        return [

            item

            for item in history

            if item.get(
                "success",
                False
            )
        ][-5:]