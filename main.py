#!/usr/bin/env python3
"""Deliver the finished news image to the harness output folder.

This entry is a single pre-rendered picture: ``entry.png`` lives next to
this script and is already the final artwork.  All this entrypoint does is
hand that exact file over to the grader by copying it, byte for byte, into
the directory named by ``MAKEFUN_OUTPUT_DIR`` (``/output`` when the
variable is unset).

The copy is guarded in two ways, and both checks run before anything is
written: the picture must actually be present, and it must fit inside the
competition's one-mebibyte size cap.  Anything else is a hard failure,
reported on stderr with a non-zero exit code, and no partial output is
left behind.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Competition cap: the delivered image may not exceed one mebibyte.
MAX_IMAGE_BYTES = 1_048_576

IMAGE_NAME = "entry.png"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"


def locate_picture() -> Path:
    """Return the path of the artwork shipped beside this script."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def resolve_output_dir() -> Path:
    """Return the harness output directory from the environment."""
    return Path(os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_DIR))


def fail(message: str) -> "SystemExit":
    """Print an error to stderr and build the non-zero exit."""
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def main() -> int:
    picture = locate_picture()
    if not picture.is_file():
        raise fail(f"{IMAGE_NAME} is missing next to {Path(__file__).name}")

    size = picture.stat().st_size
    if size > MAX_IMAGE_BYTES:
        raise fail(
            f"{IMAGE_NAME} is {size} bytes, over the "
            f"{MAX_IMAGE_BYTES} byte limit"
        )

    out_dir = resolve_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    destination = out_dir / IMAGE_NAME
    shutil.copyfile(picture, destination)
    print(f"wrote {destination} ({size} bytes, byte-exact copy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
