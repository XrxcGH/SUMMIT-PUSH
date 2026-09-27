#!/usr/bin/env bash
# Print every Team Update to PDF beside its Markdown source.
#
#   bash organizers/source/typesetting/pdf/team_updates.sh
#       -> participants/05-team-updates/TEAM-UPDATE-NN.pdf
#
# Needs Python 3 with markdown-it-py, and Node 18+ with playwright-core (npm ci, as for the
# manual).  Chromium: set CHROME_PATH, or run `npx playwright install chromium` once.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../../../.." && pwd)"

[ -d "$here/node_modules/playwright-core" ] || npm ci --prefix "$here" --no-audit --no-fund
cd "$here"
# Python on Windows ends each printed path with CR LF; strip the CR or basename keeps it
python3 team_update.py | tr -d '\r' | while read -r page; do
  name="$(basename "$page" .html)"
  node print_html.mjs "$root/$page" "$root/participants/05-team-updates/$name.pdf"
done
