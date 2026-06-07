import json
import re


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

        text = text.strip()

        candidate = (
            JsonRepairService
            .extract_json_block(
                text
            )
        )

        if not candidate:
            return ""

        data = (
            JsonRepairService
            .safe_json_loads(
                candidate
            )
        )

        if not isinstance(
                data,
                dict
        ):
            return ""

        files = data.get(
            "files"
        )

        if files is not None:

            if not isinstance(
                    files,
                    list
            ):
                return ""

            cleaned_files = []

            seen_paths = set()

            for file in files:

                if not isinstance(
                        file,
                        dict
                ):
                    continue

                path = str(
                    file.get(
                        "path",
                        ""
                    )
                ).replace(
                    "\\",
                    "/"
                ).strip()

                if not path:
                    continue

                content = file.get(
                    "content",
                    ""
                )

                if content is None:
                    content = ""

                normalized = (
                    path.lower()
                )

                if normalized in seen_paths:
                    continue

                seen_paths.add(
                    normalized
                )

                cleaned_files.append(
                    {
                        "path": path,
                        "content": str(
                            content
                        )
                    }
                )

            if not cleaned_files:
                return ""

            data["files"] = (
                cleaned_files
            )

        return json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )

    @staticmethod
    def extract_json_block(
            text: str
    ) -> str:

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
                or
                end <= start
        ):
            return ""

        return text[
            start:end + 1
        ]

    @staticmethod
    def safe_json_loads(
            text: str
    ):

        try:

            return json.loads(
                text
            )

        except Exception:

            pass

        repaired = text

        repaired = re.sub(
            r",\s*}",
            "}",
            repaired
        )

        repaired = re.sub(
            r",\s*]",
            "]",
            repaired
        )

        repaired = repaired.replace(
            "\t",
            " "
        )

        try:

            return json.loads(
                repaired
            )

        except Exception:

            return None

    @staticmethod
    def is_empty_response(
            text: str
    ) -> bool:

        return (
                not text
                or
                not str(text).strip()
        )