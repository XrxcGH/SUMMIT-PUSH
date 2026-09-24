#!/usr/bin/env bash
# Compile 02-manual/sections/*.md into GAME-MANUAL.md
# Usage: bash 02-manual/build.sh   (run from the package root or from 02-manual/)
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
out="$here/GAME-MANUAL.md"
cat "$here/manual-header.md" > "$out"
first=1
for f in "$here"/sections/*.md; do
  if [ $first -eq 0 ]; then printf -- '\n---\n\n' >> "$out"; fi
  cat "$f" >> "$out"
  first=0
done
echo "wrote $out"
