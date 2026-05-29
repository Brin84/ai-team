import json
from pathlib import Path


class KnowledgeService:

    FILE = Path(
        "knowledge.json"
    )

    MAX_RULES = 50

    @classmethod
    def get_rules(
        cls
    ) -> list[str]:

        if not cls.FILE.exists():

            return []

        try:

            data = json.loads(
                cls.FILE.read_text(
                    encoding="utf-8"
                )
            )

            if not isinstance(
                data,
                list
            ):
                return []

            return [
                str(item)
                for item in data
                if str(item).strip()
            ]

        except Exception:

            return []

    @classmethod
    def save_rule(
        cls,
        rule: str
    ):

        rule = str(
            rule or ""
        ).strip()

        if not rule:
            return

        rules = cls.get_rules()

        rules = [

            item

            for item in rules

            if item.lower()
            !=
            rule.lower()
        ]

        rules.insert(
            0,
            rule
        )

        rules = rules[
            :cls.MAX_RULES
        ]

        cls.FILE.write_text(
            json.dumps(
                rules,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    @classmethod
    def clear(
        cls
    ):

        cls.FILE.write_text(
            "[]",
            encoding="utf-8"
        )