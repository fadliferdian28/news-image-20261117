"""Write the news-image-20261117 entry image to the output directory.

Copies the pre-built entry.png (1024x1024, one picture summarising
Tuesday 17 November 2026's world news) byte-exact to /output/entry.png.
Standard library only; deterministic; no network access.
"""

import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1_048_576


def main():
    script_dir = Path(__file__).resolve().parent
    source = script_dir / "entry.png"
    size = source.stat().st_size
    if size > MAX_BYTES:
        print(
            f"error: entry.png is {size} bytes, over the {MAX_BYTES} byte limit",
            file=sys.stderr,
        )
        raise SystemExit(1)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
