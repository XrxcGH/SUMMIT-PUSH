#!/usr/bin/env bash
# Typeset the SUMMIT PUSH Game Manual as a PDF.
#
#   bash organizers/source/typesetting/pdf/build.sh            -> participants/01-game-manual/SUMMIT-PUSH-Game-Manual.pdf
#
# Needs Python 3 with markdown-it-py and pypdf, and Node 18+ (npm ci installs Paged.js and
# playwright-core).  Chromium: set CHROME_PATH, or run `npx playwright install chromium` once.
# Two passes: the first counts the manual's pages, the second prints the final
# "N of TOTAL" footers (the drawing plates are counted) and the plate page numbers,
# and runs again (up to three times) if the page count changes.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../../../.." && pwd)"
out="$root/participants/01-game-manual/SUMMIT-PUSH-Game-Manual.pdf"
nplates=6

[ -d "$here/node_modules/pagedjs" ] || npm ci --prefix "$here" --no-audit --no-fund
bash "$root/organizers/source/manual/build.sh" >/dev/null
mkdir -p "$here/build"
cd "$here"

python3 make_html.py
node render.mjs build/pass1.pdf
body=$(python3 -c "import json; print(json.load(open('build/pages.json.part'))['pages'])")

settled=0
for attempt in 1 2 3; do
  total=$((body + nplates))
  python3 make_html.py --total "$total" --plates-from $((body + 1))
  node render.mjs build/manual.pdf build/plates.pdf
  got=$(python3 -c "import json; print(json.load(open('build/pages.json.part'))['pages'])")
  [ "$got" -eq "$body" ] && { settled=1; break; }
  body=$got
done
[ "$settled" = 1 ] || { echo "the page count did not settle after 3 passes" >&2; exit 1; }

python3 - <<'PY'
import json
meta = json.load(open("build/meta.json"))
part = json.load(open("build/pages.json.part"))
import make_html
json.dump({"title": meta["title"], "version": meta["version"], "revision": meta["revision"],
           "outline": part["outline"], "plates": [n for _, n in make_html.PLATES]},
          open("build/pages.json", "w"), indent=1)
PY
python3 postprocess.py build/manual.pdf build/plates.pdf build/pages.json "$out"
