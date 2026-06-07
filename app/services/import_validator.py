from pathlib import Path
import re
import sys


class ImportValidator:

    PROJECT_PATH = Path(
        "generated_projects/project_1"
    )

    PACKAGE_IMPORT_ALIASES = {

        "python-dotenv": {
            "dotenv"
        },

        "python-telegram-bot": {
            "telegram",
            "telegram.ext"
        },

        "pytelegrambotapi": {
            "telebot"
        },

        "beautifulsoup4": {
            "bs4"
        },

        "pyyaml": {
            "yaml"
        },

        "google-auth": {
            "google.oauth2",
            "google.auth"
        },

        "google-api-python-client": {
            "googleapiclient",
            "googleapiclient.discovery"
        },

        "requests-oauthlib": {
            "requests_oauthlib"
        },

        "python-dateutil": {
            "dateutil"
        },

        "fastapi": {
            "fastapi",
            "starlette"
        },

        "gspread": {
            "gspread"
        }
    }

    SAFE_MODULES = {

        "typing",
        "pathlib",
        "asyncio",
        "datetime",
        "json",
        "os",
        "sys",
        "re",
        "logging",
        "dataclasses",
        "collections"
    }

    @classmethod
    def validate(
            cls
    ) -> list[str]:

        errors = []

        python_files = list(
            cls.PROJECT_PATH.rglob(
                "*.py"
            )
        )

        stdlib_modules = (
            cls._get_stdlib_modules()
        )

        project_modules = (
            cls._get_project_modules(
                python_files
            )
        )

        requirements_modules = (
            cls._get_requirements_modules()
        )

        for file in python_files:

            try:

                content = file.read_text(
                    encoding="utf-8"
                )

            except Exception as e:

                errors.append(
                    f"{file}: {e}"
                )

                continue

            imports = cls._extract_imports(
                content
            )

            for module in imports:

                module = (
                    module
                    .strip()
                    .lower()
                )

                if not module:
                    continue

                if module.startswith(
                        "typing."
                ):
                    continue

                root = (
                    module
                    .split(".")[0]
                )

                if (
                        root in stdlib_modules
                        or
                        root in cls.SAFE_MODULES
                ):
                    continue

                if (
                        module in project_modules
                        or
                        root in project_modules
                ):
                    continue

                if cls._is_known_dependency(
                        module,
                        requirements_modules
                ):
                    continue

                print(
                    f"[IMPORT ERROR] "
                    f"{file} -> {module}"
                )
                
                errors.append(
                    (
                        f"{file}: "
                        f"модуль '{module}' "
                        f"не найден"
                    )
                )

        errors.extend(
            cls.validate_internal_imports()
        )

        return list(
            dict.fromkeys(
                errors
            )
        )

    @classmethod
    def _is_known_dependency(
            cls,
            module: str,
            requirements_modules: set[str]
    ) -> bool:

        if module in requirements_modules:
            return True

        for requirement in requirements_modules:

            if (
                    module.startswith(
                        requirement + "."
                    )
            ):
                return True

        aliases = (
            cls._build_alias_index()
        )

        for package, package_aliases in (
                aliases.items()
        ):

            if package not in requirements_modules:
                continue

            for alias in package_aliases:

                if (
                        module == alias
                        or
                        module.startswith(
                            alias + "."
                        )
                ):
                    return True

        return False

    @classmethod
    def _build_alias_index(
            cls
    ) -> dict[str, set[str]]:

        index = {}

        for package, aliases in (
                cls.PACKAGE_IMPORT_ALIASES.items()
        ):

            normalized = set()

            for alias in aliases:

                alias = alias.lower()

                normalized.add(
                    alias
                )

                parts = alias.split(
                    "."
                )

                for i in range(
                        1,
                        len(parts) + 1
                ):

                    normalized.add(
                        ".".join(
                            parts[:i]
                        )
                    )

            index[package] = normalized

        return index

    @classmethod
    def _extract_imports(
            cls,
            content: str
    ) -> list[str]:

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

        return sorted(
            imports
        )

    @classmethod
    def _get_stdlib_modules(
            cls
    ) -> set[str]:

        return {

            module.lower()

            for module in (
                sys.stdlib_module_names
            )
        }

    @classmethod
    def _get_project_modules(
            cls,
            python_files: list[Path]
    ) -> set[str]:

        modules = set()

        for file in python_files:

            relative = file.relative_to(
                cls.PROJECT_PATH
            )

            module_name = (
                str(relative)
                .replace("\\", ".")
                .replace("/", ".")
                .replace(".py", "")
                .lower()
            )

            modules.add(
                module_name
            )

            if module_name.endswith(
                    ".__init__"
            ):

                package_name = (
                    module_name.replace(
                        ".__init__",
                        ""
                    )
                )

                modules.add(
                    package_name
                )

            parts = module_name.split(
                "."
            )

            for i in range(
                    1,
                    len(parts)
            ):

                modules.add(
                    ".".join(
                        parts[:i]
                    )
                )

        return modules

    @classmethod
    def _get_requirements_modules(
            cls
    ) -> set[str]:

        requirements = set()

        requirements_file = (
                cls.PROJECT_PATH
                / "requirements.txt"
        )

        if not requirements_file.exists():

            return requirements

        try:

            content = requirements_file.read_text(
                encoding="utf-8"
            )

        except Exception:

            return requirements

        for line in content.splitlines():

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
            )[0]

            package = (
                package
                .strip()
                .lower()
            )

            if not package:
                continue

            requirements.add(
                package
            )

            requirements.add(
                package.replace(
                    "-",
                    "_"
                )
            )

        return requirements

    @classmethod
    def validate_internal_imports(
            cls
    ) -> list[str]:

        errors = []

        python_files = list(
            cls.PROJECT_PATH.rglob(
                "*.py"
            )
        )

        project_modules = (
            cls._get_project_modules(
                python_files
            )
        )

        for file in python_files:

            try:

                content = file.read_text(
                    encoding="utf-8"
                )

            except Exception:
                continue

            imports = cls._extract_imports(
                content
            )

            for module in imports:

                if not module.startswith(
                        "app."
                ):
                    continue

                if (
                        module not in project_modules
                        and
                        not any(
                            item.startswith(
                                module + "."
                            )
                            for item in project_modules
                        )
                ):

                    errors.append(
                        (
                            f"{file}: "
                            f"internal import "
                            f"'{module}' "
                            f"не существует"
                        )
                    )

        return errors