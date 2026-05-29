class JsonRepairService:

    @staticmethod
    def extract_content(
        response
    ) -> str:

        if response is None:
            return ""

        if hasattr(
            response,
            "content"
        ):

            return str(
                response.content
            )

        if isinstance(
            response,
            dict
        ):

            return str(
                response.get(
                    "content",
                    ""
                )
            )

        return str(
            response
        )

    @staticmethod
    def repair_json(
            text: str
    ) -> str:

        if not text:
            return ""

        text = str(text)

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        start = text.find(
            "{"
        )

        end = text.rfind(
            "}"
        )

        if (
                start == -1
                or
                end == -1
        ):
            return ""

        candidate = text[
            start:end + 1
        ]

        try:

            import json

            data = json.loads(
                candidate
            )

            return json.dumps(
                data,
                ensure_ascii=False
            )

        except Exception:

            return candidate
    @staticmethod
    def is_empty_response(
        text: str
    ) -> bool:

        return (
            not text
            or
            not str(text).strip()
        )