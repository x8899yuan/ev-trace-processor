import hashlib


def calculate_sha256(file):

    sha = hashlib.sha256()

    with open(
        file,
        "rb"
    ) as f:

        while chunk := f.read(
            1024 * 1024
        ):
            sha.update(chunk)

    return sha.hexdigest()