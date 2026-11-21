"""news-image-20261121 v1 — "The Night Lima Stepped Outside".

Writes the entry image to the output directory.

The image (entry.png, 1024x833) is a photorealistic witness
photograph of Lima on the evening of Friday 20 November 2026,
minutes after a magnitude 6.8 earthquake struck the Junin region
and sent residents into the streets of the capital, under a
masthead naming the day: Saturday 21 November 2026.

The image is shipped in this repository. This program does no
rendering, no network access and no randomness: it copies the image
byte-for-byte into the directory given by MAKEFUN_OUTPUT_DIR
(default /output), refuses if the file exceeds 1 MiB, and verifies
the copy by size and SHA-256 before reporting success.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1 * 1024 * 1024  # 1 MiB limit for the entry image
IMAGE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(
            f"error: {IMAGE_NAME} is {size} bytes, "
            f"over the {MAX_BYTES} byte limit",
            file=sys.stderr,
        )
        return 1

    digest = sha256_of(source)

    with open(source, "rb") as handle:
        if handle.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print(f"error: {IMAGE_NAME} is not a PNG file", file=sys.stderr)
            return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, IMAGE_NAME)

    shutil.copyfile(source, destination)

    copied_size = os.path.getsize(destination)
    if copied_size != size or sha256_of(destination) != digest:
        print("error: copied file failed verification", file=sys.stderr)
        return 1

    print(f"wrote {destination} ({size} bytes)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
