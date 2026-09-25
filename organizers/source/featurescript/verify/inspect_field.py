# -*- coding: utf-8 -*-
"""
A small measuring API over the off-line build, for the element check scripts in checks/.

    from inspect_field import Field
    f = Field()                          # builds the whole field (default options)
    f.names()                            # every distinct body name
    rs = f.find("BLUE CRAG Summit Socket")  # records named exactly that, " n" suffix allowed (or f.find(r"re:..."))
    f.bbox(rs)                           # world bounding box [x0, y0, z0, x1, y1, z1] (inches)
    F = f.crag_frame("BLUE")             # CRAG-local frame (+x = SHELF FACE normal)
    f.bbox(rs, F)                        # bounding box in that frame
    f.dist_point(rs, (x, y, z))          # distance from a world point (0 inside/on)
    f.dist_point(rs, (x, y, z), F)       # ... from a point given in frame F
    f.dist(rs_a, rs_b)                   # minimum distance between two sets
    f.inside(rs, p) / f.volume(rs) / f.mass_lb(rs) / f.solids(rs)
    f.frame(o, x, z)                     # a world frame
    f.color(rs) -> (rgb, alpha); f.material(rs) -> {"name", "density"}

Everything is in inches.  Records are the kernel's body records (see kernel_occ.Registry).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import kernel_occ as K  # noqa: E402
import run as R  # noqa: E402


class Field:
    def __init__(self, **opts):
        o = dict(R.DEFAULT_OPTS)
        o.update(opts)
        self.opts = o
        self.ns, self.code = R.load_part_code()
        self.ctx = K.Registry()
        self.id = K.Id(("F",))
        self.ns["buildField"](self.ctx, self.id, o)

    # ---- lookup -----------------------------------------------------------------------
    def records(self):
        return list(self.ctx.bodies.values())

    def names(self):
        return sorted({r["name"] for r in self.ctx.bodies.values()})

    def find(self, name):
        if name.startswith("re:"):
            rx = re.compile(name[3:])
            out = [r for r in self.ctx.bodies.values() if rx.search(r["name"] or "")]
        else:
            # a name shared by several parts is numbered " 1", " 2", ... by numberSharedNames
            rx = re.compile(re.escape(name) + r"( \d+)?$")
            out = [r for r in self.ctx.bodies.values() if rx.match(r["name"] or "")]
        if not out:
            raise KeyError("no body named %r" % name)
        return out

    def by_id(self, *path):
        key = tuple(path)
        out = [r for k, r in self.ctx.bodies.items() if k[1:1 + len(key)] == key]
        if not out:
            raise KeyError("no body under id %r" % (key,))
        return out

    def solids(self, rs):
        out = []
        for r in rs:
            out += r["solids"]
        return out

    # ---- frames -----------------------------------------------------------------------
    def frame(self, o, x, z):
        return K.Frame(o, x, z)

    def crag_frame(self, side):
        return self.ns["cragFrame"](side.upper() == "RED")

    def alliance_frame(self, side):
        return self.ns["allianceFrame"](side.upper() == "RED")

    # ---- measurement --------------------------------------------------------------------
    def bbox(self, rs, F=None):
        sh = K._compound(self.solids(rs))
        if F is not None:
            sh = K.BRepBuilderAPI_Transform(sh, F.trsf().Inverted(), True).Shape()
        b = K.Bnd_Box()
        K.BRepBndLib.AddOptimal_s(sh, b, False, False)
        return K._box6(b)

    def _wp(self, p, F):
        return np.asarray(p, float) if F is None else F.pt(p)

    def inside(self, rs, p, F=None):
        wp = self._wp(p, F)
        for s in self.solids(rs):
            cl = K.BRepClass3d_SolidClassifier(s, K._gp(wp), 1e-7)
            if cl.State() in (K.TopAbs_IN, K.TopAbs_ON):
                return True
        return False

    def dist_point(self, rs, p, F=None):
        wp = self._wp(p, F)
        if self.inside(rs, wp):
            return 0.0
        v = K.BRepBuilderAPI_MakeVertex(K._gp(wp)).Vertex()
        return K.BRepExtrema_DistShapeShape(v, K._compound(self.solids(rs))).Value()

    def dist(self, a, b):
        return K.BRepExtrema_DistShapeShape(K._compound(self.solids(a)), K._compound(self.solids(b))).Value()

    def volume(self, rs):
        return K._volume(self.solids(rs))

    def mass_lb(self, rs):
        tot = 0.0
        for r in rs:
            tot += r["mat"]["density"] * K._volume(r["solids"]) * K.IN3 / K.LB
        return tot

    def color(self, rs):
        return rs[0]["rgb"], rs[0]["alpha"]

    def material(self, rs):
        return rs[0]["mat"]

    def common_volume(self, a, b):
        tot = 0.0
        for x in self.solids(a):
            for y in self.solids(b):
                c = K.BRepAlgoAPI_Common(x, y)
                tot += K._volume(K._solids(c.Shape()))
        return tot
