import json


class PackageInitializer:

    PACKAGE_DIRS = [

        "app",
        "app/services",
        "app/models",
        "app/db",
        "app/api",
        "app/utils"
    ]

    @classmethod
    def apply(
            cls,
            project_json: str
    ) -> str:

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

        existing_paths = {

            file.get(
                "path",
                ""
            )

            for file in files
        }

        for package_dir in cls.PACKAGE_DIRS:

            init_path = (
                f"{package_dir}/__init__.py"
            )

            if init_path not in existing_paths:

                files.append({

                    "path": init_path,
                    "content": ""
                })

        data["files"] = files

        return json.dumps(
            data,
            ensure_ascii=False
        )