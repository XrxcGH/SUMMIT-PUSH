#!/usr/bin/env bash
# Rebuild the compiled manual and the six drawing sheets, run the five checks, and confirm the
# AprilTag layout JSON matches the vision guide's tag table.
# The checks report failures in their output (RESULT, TOTAL and CLEAN lines), not in
# their exit status, so the last line printed here says only whether every script
# ran to completion.
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
printf '\n================ 04-vision/make_layout.py --check ================\n'
python 04-vision/make_layout.py --check || fail=1
printf '\n'
[ $fail -eq 0 ] && echo "all checks ran to completion; read each summary above for failures" || echo "a check exited non-zero (it stopped with an error; see its output above)"
