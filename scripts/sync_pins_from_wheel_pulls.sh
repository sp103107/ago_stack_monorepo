#!/usr/bin/env bash
# Copies stack_pins.json from sibling ago_stack_wheel_pulls.
# Usage: ./scripts/sync_pins_from_wheel_pulls.sh ../ago_stack_wheel_pulls
set -euo pipefail
MONO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$(cd "$1" && pwd)/stack_pins.json"
test -f "$SRC"
cp "$SRC" "$MONO/stack_pins.json"
echo "Copied -> $MONO/stack_pins.json"
