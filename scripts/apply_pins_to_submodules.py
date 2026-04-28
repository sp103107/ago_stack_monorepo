#!/usr/bin/env python3
"""
For each repository in stack_pins.json, if <root>/<path> is a git checkout,
run git fetch and git checkout --detach <sha>.

If the path is missing, print a hint to run print_submodule_commands.py.

Documented in ../README.md (ago_stack_monorepo).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> int:
    return int(subprocess.run(cmd, cwd=cwd).returncode)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."), help="Monorepo root")
    ap.add_argument("--pins", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = args.root.resolve()
    pins = args.pins or (root / "stack_pins.json")
    if not pins.is_file():
        print(f"error: missing {pins}", file=sys.stderr)
        return 2
    data = json.loads(pins.read_text(encoding="utf-8"))
    for repo in data.get("repositories") or []:
        path = repo.get("path")
        pin = repo.get("pin") or {}
        sha = pin.get("value") if pin.get("kind") == "sha" else None
        if not path or not sha:
            continue
        dest = root / path
        git_dir = dest / ".git"
        if not dest.is_dir() or not git_dir.exists():
            print(f"missing: {path} — run: python3 scripts/print_submodule_commands.py", file=sys.stderr)
            continue
        if args.dry_run:
            print(f"[dry-run] git -C {dest} fetch --all && git checkout --detach {sha}")
            continue
        rc = _run(["git", "-C", str(dest), "fetch", "--all"], dest)
        if rc != 0:
            return rc
        rc = _run(["git", "-C", str(dest), "checkout", "--detach", sha], dest)
        if rc != 0:
            return rc
        print(f"ok: {path} @ {sha[:7]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
