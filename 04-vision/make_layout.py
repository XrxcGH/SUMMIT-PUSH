# -*- coding: utf-8 -*-
"""
Generate apriltag-field-layout.json from the tag table in VISION-GUIDE.md §3.

    python 04-vision/make_layout.py            write the JSON
    python 04-vision/make_layout.py --check    exit 1 if the committed JSON differs

The table (inches, degrees, always-blue-origin NWU) is the source; the JSON is the WPILib
AprilTagFieldLayout form: meters, and each tag's yaw about +Z as a unit quaternion.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(HERE, "VISION-GUIDE.md")
OUT = os.path.join(HERE, "apriltag-field-layout.json")
IN = 0.0254
FIELD_L, FIELD_W = 648, 324


def tag_rows():
    text = open(GUIDE, encoding="utf-8").read()
    section = text[text.index("## 3. Tag Placement Table"):text.index("### 3.3")]
    rows = []
    for m in re.finditer(r"^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*([-\d.]+)\s*\|\s*([-\d.]+)\s*\|\s*([-\d.]+)\s*\|\s*([-\d.]+)\s*\|\s*$",
                         section, re.M):
        rows.append((int(m.group(1)),) + tuple(float(m.group(k)) for k in range(2, 6)))
    ids = [r[0] for r in rows]
    if ids != list(range(1, 27)):
        raise SystemExit("expected tags 1-26 in order in VISION-GUIDE.md §3, found %s" % ids)
    return rows


def num(v):
    """Shortest float text, with the unit-quaternion components 0, ±1 and ±√½ exact."""
    for snap in (0.0, 1.0, -1.0, math.sqrt(0.5), -math.sqrt(0.5)):
        if abs(v - snap) < 1e-12:
            v = snap
    return repr(v + 0.0)


def render(rows):
    out = ['{', '  "tags": [']
    for k, (tid, x, y, z, yaw) in enumerate(rows):
        half = math.radians(yaw) / 2
        t = [round(c * IN, 6) for c in (x, y, z)]
        out += ['    {',
                '      "ID": %d,' % tid,
                '      "pose": {',
                '        "translation": { "x": %s, "y": %s, "z": %s },' % tuple(num(c) for c in t),
                '        "rotation": {',
                '          "quaternion": { "W": %s, "X": 0.0, "Y": 0.0, "Z": %s }' % (num(math.cos(half)), num(math.sin(half))),
                '        }',
                '      }',
                '    }' + (',' if k < len(rows) - 1 else '')]
    out += ['  ],', '  "field": {', '    "length": %s,' % num(round(FIELD_L * IN, 6)),
            '    "width": %s' % num(round(FIELD_W * IN, 6)), '  }', '}', '']
    return "\n".join(out)


def main():
    text = render(tag_rows())
    if "--check" in sys.argv:
        same = open(OUT, encoding="utf-8").read() == text
        print("apriltag-field-layout.json %s VISION-GUIDE.md §3" % ("matches" if same else "DIFFERS FROM"))
        sys.exit(0 if same else 1)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote %s (26 tags)" % os.path.relpath(OUT))


if __name__ == "__main__":
    main()
