# -*- coding: utf-8 -*-
"""
Assemble the final Game Manual PDF.

    python organizers/source/typesetting/pdf/postprocess.py <manual.pdf> <plates.pdf> <pages.json> <out.pdf>

Appends the drawing plates to the paginated manual, sets the print boxes (the manual is
rendered with 0.125-in bleed: MediaBox and BleedBox keep it, TrimBox and CropBox are the
Letter page, so viewers and office printers show the trimmed page while a print shop still
gets the bleed), adds a two-level bookmark outline and the document metadata.
"""
import json
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

BLEED = 9.0   # 0.125 in, in points


def main():
    manual, plates, pages_json, out = sys.argv[1:5]
    with open(pages_json, encoding="utf-8") as fh:
        info = json.load(fh)
    w = PdfWriter()
    w.append(PdfReader(manual))
    nbody = len(w.pages)
    for pg in w.pages:
        mb = pg.mediabox
        trim = RectangleObject([mb.left + BLEED, mb.bottom + BLEED, mb.right - BLEED, mb.top - BLEED])
        pg.bleedbox = RectangleObject(mb)
        pg.trimbox = trim
        pg.cropbox = trim
    w.append(PdfReader(plates))
    for pg in w.pages[nbody:]:
        pg.trimbox = RectangleObject(pg.mediabox)
        pg.bleedbox = RectangleObject(pg.mediabox)

    # bookmarks: front matter, the sections with their subsections, the appendix and plates
    for item in info["outline"]:
        parent = w.add_outline_item(item["title"], item["page"] - 1)
        for sub in item.get("children", []):
            w.add_outline_item(sub["title"], sub["page"] - 1, parent=parent)
    plates_parent = w.add_outline_item("Drawing plates", nbody)
    for k, name in enumerate(info["plates"]):
        w.add_outline_item("Plate %d  %s" % (k + 1, name), nbody + k, parent=plates_parent)
    w.page_mode = "/UseOutlines"
    w.add_metadata({
        "/Title": "%s, Version %s" % (info["title"], info["version"]),
        "/Author": "SUMMIT PUSH",
        "/Subject": "Official game manual for SUMMIT PUSH, an original offseason robotics design game",
        "/Keywords": "SUMMIT PUSH; game manual; robotics; revision %s" % info["revision"],
        "/Creator": "organizers/source/typesetting/pdf (Paged.js, Chromium)",
    })
    w.compress_identical_objects()
    with open(out, "wb") as fh:
        w.write(fh)
    print("wrote %s: %d pages (%d manual + %d plates)" % (out, len(w.pages), nbody, len(w.pages) - nbody))


if __name__ == "__main__":
    main()
