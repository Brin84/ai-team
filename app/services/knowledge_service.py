import json
from pathlib import Path


class KnowledgeService:

    FILE = Path(
        "knowledge.json"
    )

    @classmethod
    def get_rules(
        cls
    ) -> list[str]:

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
    def save_rule(
        cls,
        rule: str
    ):

        if not rule:
            return

        rules = cls.get_rules()

        if rule in rules:
            return

        rules.append(
            rule
        )

        cls.FILE.write_text(
            json.dumps(
                rules,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )