class ArchitectureValidator:

    @staticmethod
    def validate_paths(
        patch_files: list[str],
        allowed_paths: list[str]
    ) -> tuple[bool, list[str]]:

        normalized_allowed = {

            path.strip()

            for path in allowed_paths
        }

        invalid = []

        for path in patch_files:

            normalized = path.strip()

            if normalized not in normalized_allowed:

                invalid.append(
                    normalized
                )

        return (

            len(invalid) == 0,

            invalid
        )