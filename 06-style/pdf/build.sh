#!/usr/bin/env bash
# Typeset the SUMMIT PUSH Game Manual as a PDF.
#
#   bash 06-style/pdf/build.sh            -> 02-manual/SUMMIT-PUSH-Game-Manual.pdf
#
# Needs Python 3 with markdown-it-py and pypdf, and Node 18+ (npm ci installs Paged.js and
# playwright-core).  Chromium: set CHROME_PATH, or run `npx playwright install chromium` once.
# Two passes: the first counts the manual's pages, the second prints the final
# "N of TOTAL" footers (the drawing plates are counted) and the plate page numbers.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
out="$root/02-manual/SUMMIT-PUSH-Game-Manual.pdf"
nplates=6

[ -d "$here/node_modules/pagedjs" ] || npm ci --prefix "$here" --no-audit --no-fund
bash "$root/02-manual/build.sh" >/dev/null
mkdir -p "$here/build"
cd "$here"

python make_html.py
node render.mjs build/pass1.pdf
body=$(python -c "import json; print(json.load(open('build/pages.json.part'))['pages'])")

for attempt in 1 2 3; do
  total=$((body + nplates))
  python make_html.py --total "$total" --plates-from $((body + 1))
  node render.mjs build/manual.pdf build/plates.pdf
  got=$(python -c "import json; print(json.load(open('build/pages.json.part'))['pages'])")
  [ "$got" -eq "$body" ] && break
  body=$got
done

python - <<'PY'
import json
meta = json.load(open("build/meta.json"))
part = json.load(open("build/pages.json.part"))
import make_html
json.dump({"title": meta["title"], "version": meta["version"], "revision": meta["revision"],
           "outline": part["outline"], "plates": [n for _, n in make_html.PLATES]},
          open("build/pages.json", "w"), indent=1)
PY
python postprocess.py build/manual.pdf build/plates.pdf build/pages.json "$out"
