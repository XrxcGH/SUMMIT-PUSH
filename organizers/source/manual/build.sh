#!/usr/bin/env bash
# Compile sections/*.md into participants/01-game-manual/GAME-MANUAL.md
# Usage: bash organizers/source/manual/build.sh   (from any directory)
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
out="$(cd "$here/../../../participants/01-game-manual" && pwd)/GAME-MANUAL.md"
cat "$here/manual-header.md" > "$out"
first=1
for f in "$here"/sections/*.md; do
  if [ $first -eq 0 ]; then printf -- '\n---\n\n' >> "$out"; fi
  # sections link figures as ../figures/; the compiled manual has figures/ beside it
  sed 's#](\.\./figures/#](figures/#g' "$f" >> "$out"
  first=0
done
echo "wrote $out"
