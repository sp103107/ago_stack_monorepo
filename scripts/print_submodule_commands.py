#!/usr/bin/env python3
"""
Emit `git submodule add <url> <path>` lines for each entry in stack_pins.json
that does not yet exist as a directory under the monorepo root.

Documented in ../README.md (ago_stack_monorepo).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."), help="Monorepo root (default .)")
    ap.add_argument("--pins", type=Path, default=None)
    args = ap.parse_args()
    root = args.root.resolve()
    pins = args.pins or (root / "stack_pins.json")
    if not pins.is_file():
        print(f"error: missing {pins}", file=sys.stderr)
        return 2
    data = json.loads(pins.read_text(encoding="utf-8"))
    for repo in data.get("repositories") or []:
        path = repo.get("path")
        url = repo.get("git_url")
        if not path or not url:
            continue
        dest = root / path
        if dest.exists():
            print(f"# exists, skip: {path}")
            continue
        print(f"git submodule add {url} {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
