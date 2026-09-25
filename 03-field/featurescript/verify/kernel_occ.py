# -*- coding: utf-8 -*-
"""
OpenCascade twin of src/10_kernel.fs.

Every function here has the same name, arguments and semantics as its FeatureScript
counterpart, so the transpiled part code (src/2x_*.fs .. 4x_*.fs -> Python) builds the same
geometry off-line.  Units: inches and degrees, plain floats.

The "context" is a Registry: a dict of body records keyed by the Id tuple of the operation
that created them.  Like Onshape's qCreatedBy, looking up an Id returns every body whose key
starts with that Id.
"""
import math

import numpy as np
from OCP.Standard import Standard_Failure
from OCP.BRep import BRep_Tool
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace,
                                BRepBuilderAPI_MakeWire, BRepBuilderAPI_Sewing,
                                BRepBuilderAPI_MakeSolid, BRepBuilderAPI_Transform,
                                BRepBuilderAPI_MakeVertex)
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepGProp import BRepGProp
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeThickSolid
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCP.Bnd import Bnd_Box
from OCP.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCP.GProp import GProp_GProps
from OCP.Geom import Geom_BezierSurface
from OCP.ShapeFix import ShapeFix_Face, ShapeFix_Solid, ShapeFix_Shape
from OCP.OCP.collections import Array2_gp_Pnt as TColgp_Array2OfPnt, List_TopoDS_Shape as TopTools_ListOfShape
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_IN, TopAbs_ON, TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Compound
from OCP.BRep import BRep_Builder
from OCP.gp import gp_Ax1, gp_Ax2, gp_Circ, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec, gp_GTrsf, gp_Ax3

PI = math.pi
TOL = 1e-6


class KernelError(Exception):
    pass


# ---------------------------------------------------------------------------------------
# Id — mirrors FeatureScript's hierarchical Id (`id + "name"`)
# ---------------------------------------------------------------------------------------
class Id(tuple):
    def __add__(self, other):
        if isinstance(other, str):
            return Id(tuple(self) + (other,))
        raise TypeError("Id + %r" % (other,))

    def __str__(self):
        return "/".join(self)


# ---------------------------------------------------------------------------------------
# plain-number helpers shared with the part code
# ---------------------------------------------------------------------------------------
def vector(*a):
    return np.array([float(x) for x in a])


def size(a):
    return len(a)


def append(a, x):
    return list(a) + [x]


def concatenateArrays(arrs):
    out = []
    for a in arrs:
        out += list(a)
    return out


def sqrt(x):
    return math.sqrt(x)


def floor(x):
    return math.floor(x)


def dot(a, b):
    return float(np.dot(np.asarray(a, float), np.asarray(b, float)))


def cross(a, b):
    return np.cross(np.asarray(a, float), np.asarray(b, float))


def norm(a):
    return float(np.linalg.norm(np.asarray(a, float)))


def normalize(a):
    a = np.asarray(a, float)
    return a / np.linalg.norm(a)


def sind(a):
    return math.sin(math.radians(a))


def cosd(a):
    return math.cos(math.radians(a))


def tand(a):
    return math.tan(math.radians(a))


def atan2d(y, x):
    return math.degrees(math.atan2(y, x))


def nm(s, i):
    if isinstance(i, float) and i.is_integer():
        i = int(i)
    return s + str(i)


def msg(parts):
    out = ""
    for p in parts:
        if isinstance(p, float) and p.is_integer():
            p = int(p)
        out += str(p)
    return out


# ---------------------------------------------------------------------------------------
# frames
# ---------------------------------------------------------------------------------------
class Frame:
    def __init__(self, o, x, z):
        self.o = np.asarray(o, float)
        x = np.asarray(x, float)
        z = np.asarray(z, float)
        # std coordSystem(): perpendicularVectors, dot^2 < |a|^2 |b|^2 1e-22
        if np.dot(x, z) ** 2 >= 1e-22 * np.dot(x, x) * np.dot(z, z):
            raise KernelError("frameMake: axes not perpendicular")
        self.x = x / np.linalg.norm(x)
        self.z = z / np.linalg.norm(z)
        self.y = np.cross(self.z, self.x)

    def pt(self, p):
        return self.o + self.x * p[0] + self.y * p[1] + self.z * p[2]

    def dir(self, d):
        v = self.x * d[0] + self.y * d[1] + self.z * d[2]
        return v / np.linalg.norm(v)

    def trsf(self):
        """gp_Trsf mapping world-origin geometry into this frame (FeatureScript toWorld)."""
        t = gp_Trsf()
        t.SetValues(self.x[0], self.y[0], self.z[0], self.o[0],
                    self.x[1], self.y[1], self.z[1], self.o[1],
                    self.x[2], self.y[2], self.z[2], self.o[2])
        return t

    def to_local(self, p):
        d = np.asarray(p, float) - self.o
        return np.array([d @ self.x, d @ self.y, d @ self.z])


def frameMake(o, x, z):
    return Frame(o, x, z)


def frameIn(F, o, x, z):
    return Frame(F.pt(o), F.dir(x), F.dir(z))


class _Plane:
    def __init__(self, F, pl, offset):
        self.n = F.dir(pl[1])
        self.x = F.dir(pl[2])
        # std plane(): abs(dot) < TOLERANCE.zeroAngle (1e-11) on the normalised vectors
        if abs(np.dot(self.n, self.x)) >= 1e-11:
            raise KernelError("plane x not perpendicular to normal")
        self.y = np.cross(self.n, self.x)
        self.o = F.pt(pl[0]) + self.n * offset

    def p3(self, uv):
        return self.o + self.x * uv[0] + self.y * uv[1]


def _gp(p):
    return gp_Pnt(float(p[0]), float(p[1]), float(p[2]))


def _gd(d):
    return gp_Dir(float(d[0]), float(d[1]), float(d[2]))


# ---------------------------------------------------------------------------------------
# registry (the "context")
# ---------------------------------------------------------------------------------------
class Registry:
    def __init__(self):
        self.bodies = {}      # Id -> record
        self.warnings = []
        self.log = []         # operation log for diagnostics

    def add(self, key, shape, kind="solid"):
        key = Id(key)
        for k in self.bodies:
            if k[:len(key)] == key or key[:len(k)] == k:
                raise KernelError("Id prefix collision: %s vs %s" % (key, k))
        solids = _solids(shape)
        if not solids:
            raise KernelError("operation %s produced no solid" % key)
        self.bodies[key] = {"solids": solids, "name": None, "rgb": None, "alpha": 1.0,
                            "mat": None, "faces": [], "decal": None, "id": key}
        return key

    def keys_for(self, ids):
        out = []
        for i in ids:
            i = tuple(i)
            hit = [k for k in self.bodies if k[:len(i)] == i]
            out += [k for k in hit if k not in out]
        return out

    def solids_for(self, ids):
        out = []
        for k in self.keys_for(ids):
            out += self.bodies[k]["solids"]
        return out

    def shape_for(self, ids):
        return _compound(self.solids_for(ids))


def _solids(shape):
    out = []
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    while exp.More():
        out.append(TopoDS.Solid(exp.Current()))
        exp.Next()
    return out


def _compound(shapes):
    comp = TopoDS_Compound()
    b = BRep_Builder()
    b.MakeCompound(comp)
    for s in shapes:
        b.Add(comp, s)
    return comp


def _check(shape, what):
    if not BRepCheck_Analyzer(shape).IsValid():
        raise KernelError("invalid shape from " + what)


# ---------------------------------------------------------------------------------------
# sketch profiles -> faces
# ---------------------------------------------------------------------------------------
def _edges_for_loop(P, loop):
    edges = []
    for s in loop:
        if s[0] == "L":
            a, b = P.p3(s[1]), P.p3(s[2])
            if np.linalg.norm(a - b) < 1e-9:
                raise KernelError("zero-length line")
            edges.append(BRepBuilderAPI_MakeEdge(GC_MakeSegment(_gp(a), _gp(b)).Value()).Edge())
        elif s[0] == "A":
            a, m, b = P.p3(s[1]), P.p3(s[2]), P.p3(s[3])
            edges.append(BRepBuilderAPI_MakeEdge(GC_MakeArcOfCircle(_gp(a), _gp(m), _gp(b)).Value()).Edge())
        elif s[0] == "C":
            c = P.p3(s[1])
            circ = gp_Circ(gp_Ax2(_gp(c), _gd(P.n), _gd(P.x)), float(s[2]))
            edges.append(BRepBuilderAPI_MakeEdge(circ).Edge())
        else:
            raise KernelError("bad segment " + str(s[0]))
    return edges


def _wire(P, loop):
    mw = BRepBuilderAPI_MakeWire()
    for e in _edges_for_loop(P, loop):
        mw.Add(e)
    if not mw.IsDone():
        raise KernelError("profile loop is not connected")
    w = mw.Wire()
    if not BRep_Tool.IsClosed_s(w):
        raise KernelError("profile loop is not closed")
    return w


def _face(P, loops):
    outer = _wire(P, loops[0])
    mf = BRepBuilderAPI_MakeFace(outer, True)
    if not mf.IsDone():
        raise KernelError("cannot make planar face")
    for hole in loops[1:]:
        mf.Add(_wire(P, hole))
    fix = ShapeFix_Face(mf.Face())
    fix.FixOrientation()
    fix.Perform()
    return fix.Face()


def _kPolyLoop(pts):
    return [["L", pts[i], pts[(i + 1) % len(pts)]] for i in range(len(pts))]


# ---------------------------------------------------------------------------------------
# shape creation
# ---------------------------------------------------------------------------------------
def mkPrismProfile(context, id, F, pl, loops, d0, d1):
    if not d1 > d0:
        raise KernelError("mkPrismProfile needs d1 > d0 (%s, %s) at %s" % (d0, d1, id))
    P = _Plane(F, pl, d0)
    face = _face(P, loops)
    shape = BRepPrimAPI_MakePrism(face, gp_Vec(*(P.n * (d1 - d0)))).Shape()
    _check(shape, "mkPrismProfile " + str(id))
    context.add(id + "ex", shape)


def mkPrism(context, id, F, pl, pts, d0, d1):
    mkPrismProfile(context, id, F, pl, [_kPolyLoop(pts)], d0, d1)


def mkPrismHoles(context, id, F, pl, outer, holes, d0, d1):
    mkPrismProfile(context, id, F, pl, [_kPolyLoop(outer)] + [_kPolyLoop(h) for h in holes], d0, d1)


def mkCyl(context, id, F, pl, c, r, d0, d1):
    mkPrismProfile(context, id, F, pl, [[["C", c, r]]], d0, d1)


def mkTube(context, id, F, pl, c, ro, ri, d0, d1):
    mkPrismProfile(context, id, F, pl, [[["C", c, ro]], [["C", c, ri]]], d0, d1)


def mkRevolve(context, id, F, pl, loop):
    P = _Plane(F, pl, 0)
    for s in loop:
        for p in s[1:]:
            if isinstance(p, (list, tuple, np.ndarray)) and p[0] < -1e-9:
                raise KernelError("revolve profile crosses the axis at " + str(id))
    if len(loop) == 1 and loop[0][0] == "C":
        # full-circle profile: OpenCascade's revolve leaves a degenerate seam here, so build
        # the identical torus directly (Onshape's revolve of the same sketch is exact)
        from OCP.BRepPrimAPI import BRepPrimAPI_MakeTorus
        cu, cv = loop[0][1]
        if cu - loop[0][2] < -1e-9:
            raise KernelError("revolve profile crosses the axis at " + str(id))
        centre = P.o + P.y * cv
        shape = BRepPrimAPI_MakeTorus(gp_Ax2(_gp(centre), _gd(P.y), _gd(P.x)), float(cu), float(loop[0][2])).Shape()
        _check(shape, "mkRevolve " + str(id))
        context.add(id + "rv", shape)
        return
    face = _face(P, [loop])
    axis = gp_Ax1(_gp(P.o), _gd(P.y))
    shape = BRepPrimAPI_MakeRevol(face, axis, 2 * PI).Shape()
    fix = ShapeFix_Shape(shape)
    fix.Perform()
    shape = fix.Shape()
    _check(shape, "mkRevolve " + str(id))
    context.add(id + "rv", shape)


def mkPillowBox(context, id, F, h, crown):
    faces = []
    for ax in range(3):
        for sgn in (-1, 1):
            arr = TColgp_Array2OfPnt(1, 3, 1, 3)
            for i in range(3):
                for j in range(3):
                    a = (i - 1) * h
                    b = (j - 1) * h * sgn
                    c = sgn * (h + (4 * crown if (i == 1 and j == 1) else 0))
                    p = [0.0, 0.0, 0.0]
                    p[ax] = c
                    p[(ax + 1) % 3] = a
                    p[(ax + 2) % 3] = b
                    arr.SetValue(i + 1, j + 1, _gp(F.pt(p)))
            surf = Geom_BezierSurface(arr)
            faces.append(BRepBuilderAPI_MakeFace(surf, 1e-7).Face())
    sew = BRepBuilderAPI_Sewing(1e-6)
    for f in faces:
        sew.Add(f)
    sew.Perform()
    shell = sew.SewedShape()
    exp = TopExp_Explorer(shell, TopAbs_SHELL)
    solid = BRepBuilderAPI_MakeSolid(TopoDS.Shell(exp.Current())).Solid()
    fix = ShapeFix_Solid(solid)
    fix.Perform()
    shape = fix.Solid()
    _check(shape, "mkPillowBox")
    context.add(id + "ex", shape)


# ---------------------------------------------------------------------------------------
# booleans and body operations
# ---------------------------------------------------------------------------------------
def _replace(context, key, shape):
    rec = context.bodies[key]
    sol = _solids(shape)
    if not sol:
        raise KernelError("boolean consumed body " + str(key))
    rec["solids"] = sol


def _lst(shapes):
    out = TopTools_ListOfShape()
    for x in shapes:
        out.Append(x)
    return out


def _cut(target, tools):
    op = BRepAlgoAPI_Cut()
    op.SetArguments(_lst([target]))
    op.SetTools(_lst(tools))
    op.Build()
    if not op.IsDone():
        raise KernelError("cut failed")
    return op.Shape()


def bSubtract(context, id, targets, tools, keepTools):
    tkeys = context.keys_for(targets)
    if not tkeys:
        raise KernelError("bSubtract %s: no targets" % (id,))
    if not context.keys_for(tools):
        raise KernelError("bSubtract %s: no tools" % (id,))
    tool_solids = context.solids_for(tools)
    for k in tkeys:
        new = []
        for s in context.bodies[k]["solids"]:
            new += _solids(_cut(s, tool_solids))
        if not new:
            raise KernelError("bSubtract %s consumed %s" % (id, k))
        for s in new:
            _check(s, "bSubtract " + str(id))
        context.bodies[k]["solids"] = new
    if not keepTools:
        for k in context.keys_for(tools):
            del context.bodies[k]


def bUnion(context, id, bodies):
    keys = context.keys_for(bodies)
    if len(keys) < 1:
        raise KernelError("bUnion: nothing to merge")
    solids = context.solids_for(bodies)
    op = BRepAlgoAPI_Fuse()
    op.SetArguments(_lst(solids[:1]))
    op.SetTools(_lst(solids[1:]))
    op.Build()
    if not op.IsDone():
        raise KernelError("fuse failed " + str(id))
    sol = _solids(op.Shape())
    for x in sol:
        _check(x, "bUnion " + str(id))
    context.bodies[keys[0]]["solids"] = sol
    for k in keys[1:]:
        del context.bodies[k]


def bDelete(context, id, bodies):
    for k in context.keys_for(bodies):
        del context.bodies[k]


def removeSlivers(context, id, bodies, minVolume):
    for k in context.keys_for(bodies):
        keep = [x for x in context.bodies[k]["solids"] if _volume([x]) >= minVolume]
        if keep:
            context.bodies[k]["solids"] = keep
        else:
            del context.bodies[k]


def shellHollow(context, id, bodies, t):
    """Hollow each solid inward by t with no faces removed (Onshape opShell, negative
    thickness): the solid minus its inward offset, leaving an internal void."""
    for k in context.keys_for(bodies):
        new = []
        for s in context.bodies[k]["solids"]:
            mk = BRepOffsetAPI_MakeThickSolid()
            mk.MakeThickSolidByJoin(s, TopTools_ListOfShape(), -t, 1e-6)
            mk.Build()
            if not mk.IsDone():
                raise KernelError("shell failed " + str(id))
            inner = _solids(mk.Shape())
            if len(inner) != 1 or _volume(inner) >= _volume([s]):
                raise KernelError("shell offset unexpected at " + str(id))
            new += _solids(_cut(s, inner))
        for s in new:
            _check(s, "shellHollow " + str(id))
        context.bodies[k]["solids"] = new


def _edges_through(shape, points, tol=1e-5):
    found = []
    for p in points:
        v = BRepBuilderAPI_MakeVertex(_gp(p)).Vertex()
        exp = TopExp_Explorer(shape, TopAbs_EDGE)
        hit = False
        while exp.More():
            e = TopoDS.Edge(exp.Current())
            d = BRepExtrema_DistShapeShape(v, e)
            if d.IsDone() and d.Value() < tol:
                if not any(e.IsSame(f) for f in found):
                    found.append(e)
                hit = True
            exp.Next()
        if not hit:
            raise KernelError("no edge through point %s" % (list(p),))
    return found


def filletAt(context, id, bodies, F, pts, r, strict=True):
    wp = [F.pt(p) for p in pts]
    keys = context.keys_for(bodies)
    # every requested point must lie on an edge of one of the bodies (as in FeatureScript,
    # where an unmatched point contributes nothing; here it is an error, to catch mistakes)
    found = [False] * len(wp)
    plan = []
    for k in keys:
        for si, s in enumerate(context.bodies[k]["solids"]):
            edges = []
            for pi, p in enumerate(wp):
                try:
                    e = _edges_through(s, [p])
                except KernelError:
                    continue
                found[pi] = True
                edges += [x for x in e if not any(x.IsSame(y) for y in edges)]
            plan.append((k, si, edges))
    missing = [list(wp[i]) for i in range(len(wp)) if not found[i]]
    if missing:
        if strict:
            raise KernelError("filletAt %s: no edge through %s" % (id, missing))
        # FeatureScript: an unmatched point contributes nothing; the matched edges still round
        context.warnings.append("roundover %s: no edge through %s" % (id, missing))
    # one opFillet in FeatureScript: build every result first, commit only if all succeed
    results = []
    for k, si, edges in plan:
        if not edges:
            continue
        s = context.bodies[k]["solids"][si]
        mk = BRepFilletAPI_MakeFillet(s)
        for e in edges:
            mk.Add(float(r), e)
        mk.Build()
        if not mk.IsDone():
            raise KernelError("fillet failed " + str(id))
        out = _solids(mk.Shape())
        for x in out:
            _check(x, "filletAt " + str(id))
        results.append((k, si, out))
    for k, si, out in reversed(results):
        context.bodies[k]["solids"][si:si + 1] = out


def softFilletAt(context, id, bodies, F, pts, r, label):
    # as `try silent` around one opFillet: unmatched points are dropped, and a failed fillet
    # leaves every body unchanged; only kernel/OCC failures become warnings
    try:
        filletAt(context, id, bodies, F, pts, r, strict=False)
    except (KernelError, RuntimeError, Standard_Failure) as e:
        context.warnings.append("reference roundover skipped - %s (%s)" % (label, e))


def copyBody(context, id, src, F):
    keys = context.keys_for(src)
    if not keys:
        raise KernelError("copyBody: no source")
    shapes = []
    for k in keys:
        for s in context.bodies[k]["solids"]:
            shapes.append(BRepBuilderAPI_Transform(s, F.trsf(), True).Shape())
    newk = context.add(id + "c", _compound(shapes))
    rec0 = context.bodies[keys[0]]
    rec = context.bodies[newk]
    for f in ("name", "rgb", "alpha", "mat", "decal"):
        rec[f] = rec0[f]
    # face styles were recorded at world points on the source; the copy carries them along
    rec["faces"] = [(tuple(F.pt(p)), rgb, a) for (p, rgb, a) in rec0["faces"]]
    rec["copied_from"] = keys[0]


# ---------------------------------------------------------------------------------------
# properties
# ---------------------------------------------------------------------------------------
def styleBody(context, bodies, name, rgb, alpha, mat):
    keys = context.keys_for(bodies)
    if not keys:
        raise KernelError("styleBody %r: no bodies" % name)
    for k in keys:
        rec = context.bodies[k]
        rec["name"] = name
        rec["rgb"] = tuple(rgb)
        rec["alpha"] = alpha
        rec["mat"] = dict(mat)


def nameBody(context, bodies, name):
    keys = context.keys_for(bodies)
    if not keys:
        raise KernelError("nameBody %r: no bodies" % name)
    for k in keys:
        context.bodies[k]["name"] = name


def numberSharedNames(context, bodies):
    """Every part (solid) gets a unique name; parts sharing a name get " 1", " 2", ... in
    creation order.  A record holding several solids keeps its base name and lists the
    per-solid names in rec["solid_names"]."""
    keys = context.keys_for(bodies)
    total = {}
    for k in keys:
        rec = context.bodies[k]
        total[rec["name"]] = total.get(rec["name"], 0) + len(rec["solids"])
    seen = {}
    for k in keys:
        rec = context.bodies[k]
        n = rec["name"]
        if total[n] < 2:
            continue
        names = []
        for _ in rec["solids"]:
            seen[n] = seen.get(n, 0) + 1
            names.append("%s %d" % (n, seen[n]))
        if len(names) == 1:
            rec["name"] = names[0]
        else:
            rec["solid_names"] = names


def part_names(context):
    """Name of every part (solid) the field would show in Onshape's parts list."""
    out = []
    for rec in context.bodies.values():
        out += rec.get("solid_names") or [rec["name"]] * len(rec["solids"])
    return out


def styleFacesAt(context, bodies, F, pts, rgb, alpha):
    keys = context.keys_for(bodies)
    for p in pts:
        wp = F.pt(p)
        v = BRepBuilderAPI_MakeVertex(_gp(wp)).Vertex()
        hit = False
        for k in keys:
            for s in context.bodies[k]["solids"]:
                exp = TopExp_Explorer(s, TopAbs_FACE)
                while exp.More():
                    d = BRepExtrema_DistShapeShape(v, exp.Current())
                    if d.IsDone() and d.Value() < 1e-5:
                        hit = True
                    exp.Next()
            if hit:
                context.bodies[k]["faces"].append((tuple(wp), tuple(rgb), alpha))
                break
        if not hit:
            raise KernelError("styleFacesAt: no face through %s" % (list(wp),))


def _volume(shapes):
    tot = 0.0
    for s in shapes:
        g = GProp_GProps()
        BRepGProp.VolumeProperties_s(s, g)
        tot += g.Mass()
    return tot


LB = 0.45359237           # kg
IN3 = 0.0254 ** 3         # m^3


def massBody(context, bodies, matName, massLb):
    keys = context.keys_for(bodies)
    vol = _volume(context.solids_for(bodies))
    rho = massLb * LB / (vol * IN3)
    for k in keys:
        context.bodies[k]["mat"] = {"name": matName, "density": rho}
    return rho


def tagDecal(context, id, bodies, F, pl, black, cells, s, rgb):
    P = _Plane(F, pl, 0)
    keys = context.keys_for(bodies)
    # the decal face must exist: the plane origin lies on a face of the panel
    v = BRepBuilderAPI_MakeVertex(_gp(P.o)).Vertex()
    d = BRepExtrema_DistShapeShape(v, context.shape_for(bodies))
    if d.Value() > 1e-6:
        raise KernelError("tagDecal: plane origin is not on the panel")
    for k in keys:
        context.bodies[k]["decal"] = {"origin": tuple(P.o), "normal": tuple(P.n), "x": tuple(P.x),
                                      "black": [tuple(c) for c in black], "cells": cells, "s": s}


# ---------------------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------------------
def measureBox(context, bodies, F):
    if not context.keys_for(bodies):
        raise KernelError("measureBox: no bodies for %s" % ([str(b) for b in bodies],))
    sh = context.shape_for(bodies)
    # bounding box in frame F: transform the shape into F's coordinates first
    inv = F.trsf().Inverted()
    local = BRepBuilderAPI_Transform(sh, inv, True).Shape()
    b = Bnd_Box()
    BRepBndLib.AddOptimal_s(local, b, False, False)
    return _box6(b)


def _box6(b):
    lo, hi = b.CornerMin(), b.CornerMax()
    return [lo.X(), lo.Y(), lo.Z(), hi.X(), hi.Y(), hi.Z()]


def measureVolume(context, bodies):
    return _volume(context.solids_for(bodies))


def measureDistToPoint(context, bodies, F, p):
    sh = context.shape_for(bodies)
    wp = F.pt(p)
    for s in context.solids_for(bodies):
        cl = BRepClass3d_SolidClassifier(s, _gp(wp), 1e-7)
        if cl.State() in (TopAbs_IN, TopAbs_ON):
            return 0.0
    v = BRepBuilderAPI_MakeVertex(_gp(wp)).Vertex()
    return BRepExtrema_DistShapeShape(v, sh).Value()


def measureDist(context, a, b):
    return BRepExtrema_DistShapeShape(context.shape_for(a), context.shape_for(b)).Value()


# ---------------------------------------------------------------------------------------
# decoration and grouping (twins of chamferAt / softChamferAt / mkLoft / faceDecal /
# compositePart in src/10_kernel.fs)
# ---------------------------------------------------------------------------------------
def kWarn(context, id, message):
    context.warnings.append(message)


def chamferAt(context, id, bodies, F, pts, d, strict=True):
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeChamfer
    wp = [F.pt(p) for p in pts]
    keys = context.keys_for(bodies)
    found = [False] * len(wp)
    plan = []
    for k in keys:
        for si, s in enumerate(context.bodies[k]["solids"]):
            edges = []
            for pi, p in enumerate(wp):
                try:
                    e = _edges_through(s, [p])
                except KernelError:
                    continue
                found[pi] = True
                edges += [x for x in e if not any(x.IsSame(y) for y in edges)]
            plan.append((k, si, edges))
    missing = [list(wp[i]) for i in range(len(wp)) if not found[i]]
    if missing:
        if strict:
            raise KernelError("chamferAt %s: no edge through %s" % (id, missing))
        context.warnings.append("chamfer %s: no edge through %s" % (id, missing))
    results = []
    for k, si, edges in plan:
        if not edges:
            continue
        s = context.bodies[k]["solids"][si]
        mk = BRepFilletAPI_MakeChamfer(s)
        for e in edges:
            mk.Add(float(d), e)
        mk.Build()
        if not mk.IsDone():
            raise KernelError("chamfer failed " + str(id))
        out = _solids(mk.Shape())
        for x in out:
            _check(x, "chamferAt " + str(id))
        results.append((k, si, out))
    for k, si, out in reversed(results):
        context.bodies[k]["solids"][si:si + 1] = out


def softChamferAt(context, id, bodies, F, pts, d, label):
    try:
        chamferAt(context, id, bodies, F, pts, d, strict=False)
    except (KernelError, RuntimeError, Standard_Failure) as e:
        context.warnings.append("decorative chamfer skipped - %s (%s)" % (label, e))


def mkLoft(context, id, F, profiles):
    from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections
    if len(profiles) < 2:
        raise KernelError("mkLoft needs two or more profiles at " + str(id))
    ts = BRepOffsetAPI_ThruSections(True, False, 1e-6)
    for pl, loop in profiles:
        P = _Plane(F, pl, 0)
        ts.AddWire(_wire(P, loop))
    ts.CheckCompatibility(False)
    ts.Build()
    if not ts.IsDone():
        raise KernelError("loft failed " + str(id))
    shape = ts.Shape()
    fix = ShapeFix_Shape(shape)
    fix.Perform()
    shape = fix.Shape()
    _check(shape, "mkLoft " + str(id))
    context.add(id + "lf", shape)


def faceDecal(context, id, bodies, F, pl, rects, rgb):
    """Records the painted rectangles; checks each lies on a planar face of the bodies in pl
    (the off-line twin does not split faces — the split is exact and coplanar in Onshape)."""
    P = _Plane(F, pl, 0)
    keys = context.keys_for(bodies)
    sh = context.shape_for(bodies)
    for r in rects:
        u0, v0, u1, v1 = r
        if not (u1 > u0 and v1 > v0):
            raise KernelError("faceDecal %s: degenerate rectangle %s" % (id, r))
        for uv in ((u0, v0), (u1, v0), (u1, v1), (u0, v1), ((u0 + u1) / 2, (v0 + v1) / 2)):
            p = P.p3(uv)
            v = BRepBuilderAPI_MakeVertex(_gp(p)).Vertex()
            if BRepExtrema_DistShapeShape(v, sh).Value() > 1e-6:
                raise KernelError("faceDecal %s: rectangle %s leaves the face" % (id, r))
            # and the point is on the surface, not inside: a point just outside along the
            # normal must be off the body
            q = p + P.n * 1e-3
            for s in context.solids_for(bodies):
                cl = BRepClass3d_SolidClassifier(s, _gp(q), 1e-7)
                if cl.State() == TopAbs_IN:
                    raise KernelError("faceDecal %s: plane is not an outer face" % (id,))
    for i, a in enumerate(rects):
        for b in rects[i + 1:]:
            if a[0] < b[2] - 1e-9 and b[0] < a[2] - 1e-9 and a[1] < b[3] - 1e-9 and b[1] < a[3] - 1e-9:
                raise KernelError("faceDecal %s: rectangles overlap %s %s" % (id, a, b))
    for k in keys:
        context.bodies[k].setdefault("decals", []).append(
            {"origin": tuple(P.o), "normal": tuple(P.n), "x": tuple(P.x), "rects": [tuple(r) for r in rects], "rgb": tuple(rgb)})


def groupParts(context, id, bodies, name):
    keys = context.keys_for(bodies)
    if not keys:
        raise KernelError("groupParts %r: no bodies" % name)
    comps = context.__dict__.setdefault("composites", {})
    for c in comps.values():
        overlap = set(c["members"]) & set(keys)
        if overlap:
            raise KernelError("groupParts %r: body already grouped in %r" % (name, c["name"]))
    comps[tuple(id)] = {"name": name, "members": keys}


def decalApplied(context, bodies):
    return 1 if any(r.get("decal") for r in (context.bodies[k] for k in context.keys_for(bodies))) else 0


def countBodies(context, bodies):
    return len(context.solids_for(bodies))
