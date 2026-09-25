# -*- coding: utf-8 -*-
"""Example of the check-module format (kept tiny; the element checks live alongside it)."""


def run(f):
    out = []
    bb = f.bbox(f.find("Field carpet"))
    want = [0, 0, None, 648, 324, 0]   # FIELD-CAD-PACKAGE §0: carpet 648 x 324, top at Z = 0
    for got, w, ax in zip(bb, want, ("xmin", "ymin", "zmin", "xmax", "ymax", "zmax")):
        if w is not None:
            out.append(("carpet " + ax, abs(got - w) < 1e-6, "got %.6f want %s" % (got, w)))
    return out
