# -*- coding: utf-8 -*-
"""
Export an off-line build to binary glTF 2.0 (.glb) for the WebGL renderer and the web viewer.

    python 03-field/featurescript/verify/export_glb.py [--out FILE] [--lit]

One glTF node per body (named with the body's part name), one primitive per face colour.
Coordinates are converted from the field frame (inches, Z up) to glTF (metres, Y up):
    (x, y, z) field  ->  (x, z, -y) * 0.0254
Face-colour overrides, faceDecal rectangles and AprilTag cells are carried over; decals become
thin coplanar quads 0.02 in proud of their face.  Materials are PBR: metals get metalness,
glazing and the lantern keep their alpha, lit LEDs / the lit beacon / screens are emissive.

export(ctx, path, extra_nodes=None) is importable: the robot, arena and scene runners use it.
"""
import argparse
import json
import math
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from OCP.BRep import BRep_Tool  # noqa: E402
from OCP.BRepMesh import BRepMesh_IncrementalMesh  # noqa: E402
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopLoc import TopLoc_Location  # noqa: E402
from OCP.TopoDS import TopoDS  # noqa: E402

import kernel_occ as K  # noqa: E402

IN = 0.0254
METAL = re.compile(r"steel|alumin|metal", re.I)
EMISSIVE_NAME = re.compile(r"\(lit\)|screen|display|\bLEDs?\b|stack light|lamp|lens", re.I)


def to_gltf(p):
    p = np.asarray(p, dtype=np.float64)
    return np.stack([p[..., 0], p[..., 2], -p[..., 1]], axis=-1) * IN


def srgb_to_linear(c):
    c = np.asarray(c, dtype=np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _face_mesh(face):
    loc = TopLoc_Location()
    tri = BRep_Tool.Triangulation_s(face, loc)
    if tri is None:
        return None, None
    trsf = loc.Transformation()
    pts = np.array([[q.X(), q.Y(), q.Z()] for q in (tri.Node(i).Transformed(trsf) for i in range(1, tri.NbNodes() + 1))])
    idx = np.array([tri.Triangle(i).Get() for i in range(1, tri.NbTriangles() + 1)], dtype=np.int64) - 1
    if face.Orientation() == TopAbs_REVERSED:
        idx = idx[:, [0, 2, 1]]
    return pts, idx


def _vertex_normals(pts, idx):
    n = np.zeros_like(pts)
    fn = np.cross(pts[idx[:, 1]] - pts[idx[:, 0]], pts[idx[:, 2]] - pts[idx[:, 0]])
    for k in range(3):
        np.add.at(n, idx[:, k], fn)
    ln = np.linalg.norm(n, axis=1)
    ln[ln == 0] = 1
    return n / ln[:, None]


def body_primitives(rec, defl=0.05, ang=0.25):
    """{(rgb, alpha): [positions, normals, indices]} for one body record (field inches)."""
    out = {}
    base = tuple(rec["rgb"] or (200, 0, 200))
    alpha = float(rec["alpha"] if rec["alpha"] is not None else 1)
    overrides = [(np.array(p), tuple(c), a) for (p, c, a) in rec.get("faces") or []]

    def add(key, pts, nrm, idx):
        slot = out.setdefault(key, [[], [], [], 0])
        slot[0].append(pts)
        slot[1].append(nrm)
        slot[2].append(idx + slot[3])
        slot[3] += len(pts)

    for s in rec["solids"]:
        BRepMesh_IncrementalMesh(s, defl, False, ang, True)
        exp = TopExp_Explorer(s, TopAbs_FACE)
        while exp.More():
            face = TopoDS.Face(exp.Current())
            pts, idx = _face_mesh(face)
            exp.Next()
            if pts is None or not len(idx):
                continue
            key = (base, alpha)
            if overrides:
                probe = pts[idx[len(idx) // 2]].mean(axis=0)
                v = K.BRepBuilderAPI_MakeVertex(K._gp(probe)).Vertex()
                if K.BRepExtrema_DistShapeShape(v, face).Value() > 1e-3:
                    probe = pts[0]
                for (op, oc, oa) in overrides:
                    vv = K.BRepBuilderAPI_MakeVertex(K._gp(op)).Vertex()
                    if K.BRepExtrema_DistShapeShape(vv, face).Value() < 1e-4:
                        key = (oc, float(oa))
                        break
            add(key, pts, _vertex_normals(pts, idx), idx)

    def quads(rects, o, n, x, rgb, a=1.0):
        y = np.cross(n, x)
        for (u0, v0, u1, v1) in rects:
            q = np.array([o + x * u + y * v + n * 0.02 for (u, v) in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))])
            add((tuple(rgb), a), q, np.tile(n, (4, 1)), np.array([[0, 1, 2], [0, 2, 3]]))

    for d in rec.get("decals") or []:
        quads(d["rects"], np.array(d["origin"]), np.array(d["normal"]), np.array(d["x"]), d["rgb"])
    t = rec.get("decal")
    if t:
        h, s = t["cells"] / 2.0, t["s"]
        rects = [((c - h) * s, (h - r - 1) * s, (c - h + 1) * s, (h - r) * s) for (r, c) in t["black"]]
        quads(rects, np.array(t["origin"]), np.array(t["normal"]), np.array(t["x"]), (17, 17, 17))
    return {k: (np.concatenate(v[0]), np.concatenate(v[1]), np.concatenate(v[2])) for k, v in out.items()}


def material_for(rgb, alpha, rec):
    name = rec.get("name") or ""
    matname = (rec.get("mat") or {}).get("name", "")
    lin = srgb_to_linear(rgb)
    m = {"pbrMetallicRoughness": {"baseColorFactor": [float(lin[0]), float(lin[1]), float(lin[2]), float(alpha)],
                                  "metallicFactor": 0.0, "roughnessFactor": 0.72},
         "doubleSided": alpha < 1}
    if METAL.search(matname):
        m["pbrMetallicRoughness"]["metallicFactor"] = 0.55
        m["pbrMetallicRoughness"]["roughnessFactor"] = 0.42
    if re.search(r"polycarbonate|acrylic|glaz", matname + name, re.I):
        m["pbrMetallicRoughness"]["roughnessFactor"] = 0.08
    if alpha < 1:
        m["alphaMode"] = "BLEND"
    bright = max(rgb) > 60
    if (EMISSIVE_NAME.search(name) and bright and "dark" not in name.lower()) or re.search(r"beacon.*lit", name, re.I):
        m["emissiveFactor"] = [float(lin[0]), float(lin[1]), float(lin[2])]
    return m


class _Glb:
    def __init__(self):
        self.bin = bytearray()
        self.views, self.accessors, self.meshes, self.nodes, self.materials = [], [], [], [], []
        self.matkey = {}

    def _view(self, data, target):
        while len(self.bin) % 4:
            self.bin.append(0)
        off = len(self.bin)
        self.bin += data
        self.views.append({"buffer": 0, "byteOffset": off, "byteLength": len(data), "target": target})
        return len(self.views) - 1

    def accessor(self, arr, comp, typ, target, minmax=False):
        v = self._view(arr.tobytes(), target)
        a = {"bufferView": v, "componentType": comp, "count": int(arr.shape[0]), "type": typ}
        if minmax:
            a["min"] = [float(x) for x in arr.min(axis=0)]
            a["max"] = [float(x) for x in arr.max(axis=0)]
        self.accessors.append(a)
        return len(self.accessors) - 1

    def material(self, rgb, alpha, rec):
        m = material_for(rgb, alpha, rec)
        key = json.dumps(m, sort_keys=True)
        if key not in self.matkey:
            self.materials.append(dict(m, name="%02x%02x%02x-%.2f" % (tuple(int(c) for c in rgb) + (alpha,))))
            self.matkey[key] = len(self.materials) - 1
        return self.matkey[key]

    def add_body(self, rec, name, parent=None):
        prims = []
        for (rgb, alpha), (pts, nrm, idx) in body_primitives(rec).items():
            P = to_gltf(pts).astype(np.float32)
            N = to_gltf(nrm).astype(np.float32) / IN
            I = idx.astype(np.uint32).reshape(-1)
            prims.append({"attributes": {"POSITION": self.accessor(P, 5126, "VEC3", 34962, True),
                                         "NORMAL": self.accessor(N, 5126, "VEC3", 34962)},
                          "indices": self.accessor(I, 5125, "SCALAR", 34963),
                          "material": self.material(rgb, alpha, rec)})
        if not prims:
            return None
        self.meshes.append({"name": name, "primitives": prims})
        node = {"name": name, "mesh": len(self.meshes) - 1, "extras": {"material": (rec.get("mat") or {}).get("name", "")}}
        self.nodes.append(node)
        return len(self.nodes) - 1

    def write(self, path, roots, extras=None):
        scene = {"nodes": roots}
        doc = {"asset": {"version": "2.0", "generator": "SUMMIT PUSH off-line twin"},
               "scene": 0, "scenes": [scene], "nodes": self.nodes, "meshes": self.meshes,
               "materials": self.materials, "accessors": self.accessors, "bufferViews": self.views,
               "buffers": [{"byteLength": len(self.bin)}]}
        if extras:
            doc["extras"] = extras
        js = json.dumps(doc, separators=(",", ":")).encode()
        js += b" " * ((4 - len(js) % 4) % 4)
        while len(self.bin) % 4:
            self.bin.append(0)
        total = 12 + 8 + len(js) + 8 + len(self.bin)
        with open(path, "wb") as fh:
            fh.write(struct.pack("<III", 0x46546C67, 2, total))
            fh.write(struct.pack("<II", len(js), 0x4E4F534A))
            fh.write(js)
            fh.write(struct.pack("<II", len(self.bin), 0x004E4942))
            fh.write(self.bin)


def part_label(rec, i):
    names = rec.get("solid_names")
    return names[i] if names else rec["name"]


def export(ctx, path, extras=None, keys=None):
    """Write every body of the registry (or the given keys) to `path`; returns the node count."""
    g = _Glb()
    roots = []
    for k, rec in ctx.bodies.items():
        if keys is not None and k not in keys:
            continue
        if rec.get("solid_names"):
            for i, s in enumerate(rec["solids"]):
                sub = dict(rec, solids=[s], decals=None, decal=None)
                n = g.add_body(sub, part_label(rec, i))
                if n is not None:
                    roots.append(n)
        else:
            n = g.add_body(rec, rec["name"] or "/".join(k))
            if n is not None:
                roots.append(n)
    g.write(path, roots, extras)
    return len(roots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(HERE), "renders", "field.glb"))
    ap.add_argument("--lit", action="store_true")
    a = ap.parse_args()
    from inspect_field import Field
    f = Field(lit=a.lit, fieldLed="ROUTE" if a.lit else "DARK")
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    n = export(f.ctx, a.out)
    print("wrote %s: %d nodes, %.1f MB" % (a.out, n, os.path.getsize(a.out) / 1e6))


if __name__ == "__main__":
    main()
