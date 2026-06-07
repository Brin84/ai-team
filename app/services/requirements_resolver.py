import json
import re

from app.services.import_validator import (
    ImportValidator
)


class RequirementsResolver:

    REQUIRED_PACKAGES = {

        "google.oauth2":
            "google-auth",

        "googleapiclient":
            "google-api-python-client",

        "oauth2client":
            "oauth2client",

        "gspread":
            "gspread"
    }

    @classmethod
    def resolve(
            cls,
            project_json: str
    ) -> str:

        if not project_json:
            return project_json

        try:

            data = json.loads(
                project_json
            )

        except Exception:

            return project_json

        files = data.get(
            "files",
            []
        )

        imports = set()

        requirements_file = None

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
            ).strip()

            content = str(
                file.get(
                    "content",
                    ""
                )
            )

            if path.endswith(".py"):

                imports.update(
                    cls._extract_imports(
                        content
                    )
                )

            if path == "requirements.txt":

                requirements_file = file

        if requirements_file is None:

            requirements_file = {

                "path":
                    "requirements.txt",

                "content": ""
            }

            files.append(
                requirements_file
            )

        existing_requirements = {}

        for line in requirements_file[
            "content"
        ].splitlines():

            line = line.strip()

            if (
                    not line
                    or
                    line.startswith("#")
            ):
                continue

            package = re.split(
                r"[<>=!~]",
                line
            )[0].strip().lower()

            if not package:
                continue

            existing_requirements[
                package
            ] = line

        alias_map = (
            ImportValidator
            .PACKAGE_IMPORT_ALIASES
        )

        stdlib_modules = (
            ImportValidator
            ._get_stdlib_modules()
        )

        for module in imports:

            module = (
                module
                .strip()
                .lower()
            )

            if not module:
                continue

            root = (
                module
                .split(".")[0]
            )

            if (
                    root in stdlib_modules
                    or
                    root.startswith("app")
            ):
                continue

            required_package = (
                cls.REQUIRED_PACKAGES.get(
                    module
                )
                or
                cls.REQUIRED_PACKAGES.get(
                    root
                )
            )

            if required_package:

                existing_requirements.setdefault(
                    required_package,
                    required_package
                )

                continue

            resolved = False

            for package, aliases in (
                    alias_map.items()
            ):

                normalized_aliases = [

                    alias.lower()

                    for alias in aliases
                ]

                for alias in normalized_aliases:

                    if (
                            module == alias
                            or
                            module.startswith(
                                alias + "."
                            )
                    ):

                        existing_requirements.setdefault(
                            package,
                            package
                        )

                        resolved = True

                        break

                if resolved:
                    break

            if resolved:
                continue

            existing_requirements.setdefault(
                root,
                root
            )

        requirements_file[
            "content"
        ] = "\n".join(
            sorted(
                existing_requirements.values()
            )
        )

        return json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )

    @classmethod
    def merge_requirements(
            cls,
            old_content: str,
            new_content: str
    ) -> str:

        packages = {}

        for line in (
                old_content.splitlines()
                + new_content.splitlines()
        ):

            line = line.strip()

            if (
                    not line
                    or
                    line.startswith("#")
            ):
                continue

            name = re.split(
                r"[<>=!~]",
                line
            )[0].strip().lower()

            if not name:
                continue

            packages[name] = line

        return "\n".join(
            sorted(
                packages.values()
            )
        )

    @classmethod
    def _extract_imports(
            cls,
            content: str
    ) -> set[str]:

        imports = set()

        from_imports = re.findall(
            r"from\s+([a-zA-Z0-9_.]+)\s+import",
            content
        )

        normal_imports = re.findall(
            r"^import\s+([a-zA-Z0-9_., ]+)",
            content,
            re.MULTILINE
        )

        for item in from_imports:

            item = item.strip()

            if (
                    item
                    and
                    not item.startswith(".")
            ):

                imports.add(
                    item
                )

        for item in normal_imports:

            modules = item.split(",")

            for module in modules:

                module = (
                    module
                    .split(" as ")[0]
                    .strip()
                )

                if (
                        module
                        and
                        not module.startswith(".")
                ):

                    imports.add(
                        module
                    )

        return imports