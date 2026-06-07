class PatchScopeValidator:

    @staticmethod
    def validate(
        patch_files: list[str],
        allowed_files: list[str]
    ) -> tuple[bool, list[str]]:

        violations = []

        normalized_allowed = {

            file.strip()

            for file in allowed_files

            if file.strip()
        }

        for file in patch_files:

            normalized_file = file.strip()

            if (
                normalized_file
                not in normalized_allowed
            ):

                violations.append(
                    normalized_file
                )

        return (

            len(violations) == 0,

            violations
        )