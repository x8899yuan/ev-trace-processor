import subprocess


class ArchiveValidator:

    @staticmethod
    def test_archive(
        archive,
        seven_zip
    ):

        result = subprocess.run(
            [
                seven_zip,
                "t",
                str(archive)
            ],
            capture_output=True,
            text=True
        )

        if (
            "Everything is Ok"
            not in result.stdout
        ):
            raise Exception(
                result.stdout
            )

        print(
            "Archive validated"
        )