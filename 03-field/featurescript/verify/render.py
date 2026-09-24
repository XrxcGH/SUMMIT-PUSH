# -*- coding: utf-8 -*-
"""
Render the off-line build to PNG so the geometry can be inspected by eye.

    python 03-field/featurescript/verify/render.py [--out DIR] [--lit]

Views: whole field, Blue CRAG from the shelf/socket and peg sides, Blue HEADWALL, a Blue
OUTFITTER, the three SUPPLIES, and a 2-D sheet of all 26 AprilTag decals.  Bodies are drawn in
their assigned appearance (face overrides included), with simple Lambert shading.
Requires matplotlib in addition to cadquery-ocp.
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402
from OCP.BRep import BRep_Tool  # noqa: E402
from OCP.BRepMesh import BRepMesh_IncrementalMesh  # noqa: E402
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopLoc import TopLoc_Location  # noqa: E402
from OCP.TopoDS import TopoDS  # noqa: E402

import kernel_occ as K  # noqa: E402
from inspect_field import Field  # noqa: E402


def mesh_record(rec, defl=0.08):
    """Triangles and per-triangle colours for one body record."""
    tris, cols = [], []
    base = np.array(rec["rgb"] or (200, 0, 200)) / 255.0
    overrides = [(np.array(p), np.array(c) / 255.0) for (p, c, a) in rec["faces"]]
    for s in rec["solids"]:
        BRepMesh_IncrementalMesh(s, defl, False, 0.3, True)
        exp = TopExp_Explorer(s, TopAbs_FACE)
        while exp.More():
            face = TopoDS.Face(exp.Current())
            loc = TopLoc_Location()
            tri = BRep_Tool.Triangulation_s(face, loc)
            if tri is not None:
                trsf = loc.Transformation()
                pts = []
                for i in range(1, tri.NbNodes() + 1):
                    p = tri.Node(i).Transformed(trsf)
                    pts.append((p.X(), p.Y(), p.Z()))
                pts = np.array(pts)
                col = base
                if overrides:
                    v = K.BRepBuilderAPI_MakeVertex(K._gp(pts[len(pts) // 2])).Vertex()
                    for (op, oc) in overrides:
                        vv = K.BRepBuilderAPI_MakeVertex(K._gp(op)).Vertex()
                        if K.BRepExtrema_DistShapeShape(vv, face).Value() < 1e-4:
                            col = oc
                            break
                rev = face.Orientation() == TopAbs_REVERSED
                for i in range(1, tri.NbTriangles() + 1):
                    a, b, c = tri.Triangle(i).Get()
                    t = [pts[a - 1], pts[b - 1], pts[c - 1]]
                    if rev:
                        t = [t[0], t[2], t[1]]
                    tris.append(t)
                    cols.append(col)
            exp.Next()
    return tris, cols, rec["alpha"]


def shade(tris, cols, light=(0.35, -0.55, 0.75)):
    L = np.array(light) / np.linalg.norm(light)
    out = []
    for t, c in zip(tris, cols):
        n = np.cross(t[1] - t[0], t[2] - t[0])
        nn = np.linalg.norm(n)
        k = 0.55 + 0.45 * abs(np.dot(n / nn, L)) if nn > 0 else 0.8
        out.append(np.clip(np.array(c) * k, 0, 1))
    return out


def draw(f, recs, fname, elev, azim, lims=None, title=None, size=(12, 8)):
    """One depth-sorted triangle collection (matplotlib has no z-buffer, so every triangle of
    every body is sorted together), clipped to `lims`, true aspect ratio."""
    fig = plt.figure(figsize=size, dpi=110)
    ax = fig.add_subplot(111, projection="3d")
    T, C = [], []
    for rec in recs:
        tris, cols, alpha = mesh_record(rec)
        if not tris:
            continue
        fc = shade(tris, cols)
        for t, c in zip(tris, fc):
            if lims is not None:
                ctr = np.mean(t, axis=0)
                if np.any(ctr < np.array(lims[0]) - 1) or np.any(ctr > np.array(lims[1]) + 1):
                    continue
            T.append(t)
            C.append((c[0], c[1], c[2], alpha))
    pc = Poly3DCollection(T, facecolors=C, edgecolors="none", linewidths=0)
    ax.add_collection3d(pc)
    pts = np.array(T).reshape(-1, 3)
    lo, hi = pts.min(0), pts.max(0)
    if lims:
        lo, hi = np.maximum(lo, lims[0]), np.minimum(hi, lims[1])
    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect(tuple(np.maximum(hi - lo, 1e-3)))
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel("X (in)")
    ax.set_ylabel("Y (in)")
    ax.set_zlabel("Z (in)")
    if title:
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)


def within(rec, lo, hi):
    b = K.Bnd_Box()
    for s in rec["solids"]:
        K.BRepBndLib.Add_s(s, b)
    bb = K._box6(b)
    return all(bb[i] < hi[i] and bb[i + 3] > lo[i] for i in range(3))


def tag_sheet(f, fname):
    fig, axs = plt.subplots(3, 9, figsize=(18, 6.5), dpi=110)
    recs = sorted([r for r in f.records() if r.get("decal")], key=lambda r: int(r["name"].split()[1]))
    for ax in axs.flat:
        ax.axis("off")
    for ax, rec in zip(axs.flat, recs):
        d = rec["decal"]
        img = np.ones((10, 10))
        for (r, c) in d["black"]:
            img[r, c] = 0
        ax.imshow(img, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(rec["name"].split(" - ")[0], fontsize=9)
    fig.suptitle("36h11 decals as built (viewer facing the tag; row 0 at top)")
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(HERE), "renders"))
    ap.add_argument("--lit", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    f = Field(lit=a.lit, fieldLed="ROUTE" if a.lit else "DARK")
    recs = f.records()
    sfx = "-lit" if a.lit else ""
    field_lims = ((-100, -60, -0.3), (748, 384, 100))
    draw(f, recs, os.path.join(a.out, "field%s.png" % sfx), 38, -58, lims=field_lims, title="SUMMIT PUSH field (off-line build)", size=(15, 9))
    L = ((262, 192, -0.3), (386, 288, 92))
    draw(f, recs, os.path.join(a.out, "crag-blue-shelf-side%s.png" % sfx), 16, 205, lims=L, title="BLUE CRAG - SHELF FACE and +Y SOCKET FACE", size=(11, 11))
    draw(f, recs, os.path.join(a.out, "crag-blue-peg-side%s.png" % sfx), 16, 35, lims=L, title="BLUE CRAG - PEG FACE and -Y SOCKET FACE", size=(11, 11))
    draw(f, recs, os.path.join(a.out, "headwall-blue%s.png" % sfx), 14, -38, lims=((-3, 84, -0.3), (62, 240, 88)), title="BLUE HEADWALL and BASECAMP", size=(13, 9))
    draw(f, recs, os.path.join(a.out, "outfitter-blue-1%s.png" % sfx), 20, -140, lims=((-100, 0, -0.3), (52, 64, 80)), title="BLUE OUTFITTER 1 (chute at Y 30)", size=(13, 9))
    if not a.lit:
        draw(f, recs, os.path.join(a.out, "center-cache.png"), 40, -60, lims=((284, 110, -0.3), (364, 214, 16)), title="CENTER CACHE (Latin square)", size=(11, 11))
        tag_sheet(f, os.path.join(a.out, "apriltag-decals.png"))
    print("renders written to", a.out)


if __name__ == "__main__":
    main()
