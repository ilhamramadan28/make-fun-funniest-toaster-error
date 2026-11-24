#!/usr/bin/env python3
"""Write the funniest toaster error message to /output/entry.txt.

The entry is one line, 1-120 characters of UTF-8, not only whitespace.
The script reads the entry from entry.txt next to this file, checks it
against the gate, writes it to /output/entry.txt, and verifies the copy
byte for byte.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_PATH = os.path.join(HERE, "entry.txt")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")
MAX_CHARS = 120


def load_entry():
    with open(ENTRY_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def check_gate(text):
    if not text:
        return "entry is empty or only whitespace"
    if len(text) > MAX_CHARS:
        return "entry is longer than 120 characters"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    return None


def main():
    text = load_entry()
    problem = check_gate(text)
    if problem is not None:
        print("entry fails gate: " + problem, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    os.chmod(OUT_PATH, 0o644)
    with open(OUT_PATH, "r", encoding="utf-8") as f:
        if f.read().strip() != text:
            print("byte-verify failed", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
