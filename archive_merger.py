from pathlib import Path


class ArchiveMerger:

    @staticmethod
    def merge(
        volumes,
        output_file
    ):

        with open(output_file, "wb") as out:

            for volume in volumes:

                print(
                    f"Merging {volume.path.name}"
                )

                with open(
                    volume.path,
                    "rb"
                ) as inp:

                    while True:

                        chunk = inp.read(
                            8 * 1024 * 1024
                        )

                        if not chunk:
                            break

                        out.write(chunk)

        return output_file