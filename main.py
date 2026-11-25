#!/usr/bin/env python3
"""One Star for Monday — make.fun entry.

Writes a single line of plain text: a one-star review of Monday, written
as though Monday were a restaurant. The program writes the line to
/output/entry.txt (MAKEFUN_OUTPUT_DIR in the sandbox) and nothing else.
Deterministic: the same line every run.
"""

import os
import sys

LINE = (
    "Booked a table for 8 a.m. The waiter served me a Monday, "
    "the coffee was cold, and the bill came to 2,400 minutes."
)

MAX_CHARS = 180
MAX_WORDS = 25


def validate_line(line: str) -> None:
    """Gate: one non-blank line, at most 25 words and 180 characters.

    Fails loudly (non-zero exit) so a bad line never ships silently.
    """
    if not line or not line.strip():
        print("ERROR: entry line is empty or whitespace-only", file=sys.stderr)
        sys.exit(1)
    if "\n" in line or "\r" in line:
        print("ERROR: entry must be a single line", file=sys.stderr)
        sys.exit(1)
    if len(line) > MAX_CHARS:
        print(f"ERROR: entry is {len(line)} chars, over {MAX_CHARS}",
              file=sys.stderr)
        sys.exit(1)
    words = line.split()
    if len(words) > MAX_WORDS:
        print(f"ERROR: entry is {len(words)} words, over {MAX_WORDS}",
              file=sys.stderr)
        sys.exit(1)


def main() -> None:
    validate_line(LINE)
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    # Read back what was written: the gate reads this file, so a partial
    # write must fail loudly here instead of shipping a truncated line.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != LINE:
        print("ERROR: entry.txt does not match the line", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
