#!/usr/bin/env bash
# Rebuild every generated artefact, then run all four checks.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/.." && pwd)"
cd "$root"

bash 02-manual/build.sh
python 03-field/renderings/generate_drawings.py

fail=0
for f in verify.py consist.py crossdoc.py svg_collide.py svg_geom.py; do
  printf '\n================ %s ================\n' "$f"
  python "verify/$f" || fail=1
done
printf '\n'
[ $fail -eq 0 ] && echo "all checks ran" || echo "a check exited non-zero"
