#!/usr/bin/env bash
# Render the manual's figures (02-manual/figures/*.png) from the field model.
#
#   bash 06-style/pdf/render_figures.sh
#
# Builds the field off-line with the OpenCascade twin of the Onshape generator, exports it
# to glTF (03-field/featurescript/verify/export_glb.py) and renders the views in
# figure-shots.json with the headless three.js stage in 03-field/featurescript/verify/webrender.
# Needs cadquery-ocp, numpy, Pillow, Node 18+ and Chromium (CHROMIUM=path, or the Playwright install).
# Run it after any change to the field geometry; the PDF build only reads the PNGs.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
fs="$root/03-field/featurescript"
tmp="$here/build/figures"
mkdir -p "$tmp" "$root/02-manual/figures"

python3 "$fs/verify/export_glb.py" --out "$tmp/field.glb"
[ -d "$fs/verify/webrender/node_modules/three" ] || npm install --prefix "$fs/verify/webrender" --no-audit --no-fund

# neutral, even lighting on white for print: no fog, bloom or arena spotlights
python3 - "$here/figure-shots.json" "$tmp/shots.json" <<'PY'
import json, sys
light = {"background": 16777215, "fog": False, "bloom": 0, "exposure": 0.95, "ambient": 1.05, "env": 0.55,
         "key": 1.25, "rim": 0.35, "top": 0.9, "floor": False}
shots = [dict(light, **s) for s in json.load(open(sys.argv[1]))]
json.dump(shots, open(sys.argv[2], "w"))
PY
(cd "$fs/verify/webrender" && node render.mjs --model "$tmp/field.glb" --shots "$tmp/shots.json" --out "$tmp")

# trim, size for a 7-in column at 300 dpi, and project the callout anchors
python3 "$here/figures.py" "$tmp" "$here/figure-shots.json" "$root/02-manual/figures"
