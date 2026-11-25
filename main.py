#!/usr/bin/env python3
"""break-production confession runner: entry.txt -> $MAKEFUN_OUTPUT_DIR/entry.txt."""

import json
import os

CAP = 200
HERE = os.path.dirname(os.path.abspath(__file__))
WHO = "prod-confession-bot"


def read_line():
    with open(os.path.join(HERE, "entry.txt"), "rb") as handle:
        blob = handle.read().decode("utf-8")
    lines = [ln for ln in blob.replace("\r", "").split("\n") if ln.strip()]
    if not lines:
        raise ValueError("no usable line in entry.txt")
    return lines[0].strip()


def gate(text):
    if not 1 <= len(text) <= CAP:
        raise ValueError(f"gate needs 1..{CAP} chars, saw {len(text)}")


def deliver(text):
    root = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(root, exist_ok=True)
    path = os.path.join(root, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def main():
    try:
        confession = read_line()
        gate(confession)
    except (OSError, ValueError) as problem:
        print(json.dumps({"ok": False, "why": str(problem), "who": WHO}))
        return 1
    target = deliver(confession)
    print(json.dumps({"ok": True, "why": "confession staged", "who": WHO,
                      "to": target, "chars": len(confession), "run": "r21-1930"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
