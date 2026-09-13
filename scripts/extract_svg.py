#!/usr/bin/env python3
"""Pull the first <svg>...</svg> out of a downloaded widget and write it as XML."""

import pathlib
import re
import sys


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {sys.argv[0]} SRC DST")
    src, dst = map(pathlib.Path, sys.argv[1:])
    text = src.read_text(errors="replace")
    match = re.search(r"<svg[\s\S]*</svg>", text, re.I)
    if not match:
        raise SystemExit(f"no svg root in {src}")
    svg = match.group(0)
    if not svg.startswith("<?xml"):
        svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(svg)
    print(f"wrote {dst} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
