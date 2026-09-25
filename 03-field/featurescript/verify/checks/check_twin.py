# -*- coding: utf-8 -*-
"""
TWIN FIDELITY AUDIT: does the off-line build (verify/fs2py.py + verify/kernel_occ.py) mean what
Onshape will do with SummitPushField.fs?

run(f) -> [(label, ok, detail)], one group per question:

  [src]    the FeatureScript kernel text (src/10_kernel.fs), the FeatureScript standard library
           text (v2960) and the OpenCascade twin agree on a convention
  [conv]   a tiny part built by the twin matches an independent numpy model of Onshape's
           conventions (written from the std library, not from kernel_occ)
  [twin]   a latent twin/FeatureScript divergence demonstrated with a runnable example.
           FAIL = for the same (lint-clean) code the twin gives a different answer from Onshape
  [guard]  measured on an instrumented rebuild: the real build does not exercise that divergence
  [static] static analysis of the real part code for FeatureScript-vs-Python semantic traps
  [decal]  tagDecal, the one kernel function the twin does not execute, emulated in OCC on the
           built panels using the kernel's own FeatureScript expressions
  [style]  styleFacesAt: every styled point selects exactly one face (as qContainsPoint would)

Expected values come from the std library source and the package documents, never from the
part code or the ledger.  The std library path is taken from $FS_STD or the scratchpad checkout;
the [src] checks that need it are skipped (and say so) when it is absent.
"""
import ast
import glob
import inspect
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY = os.path.dirname(HERE)
FSROOT = os.path.dirname(VERIFY)
PKG = os.path.dirname(os.path.dirname(FSROOT))
if VERIFY not in sys.path:
    sys.path.insert(0, VERIFY)

import fs2py  # noqa: E402
import kernel_occ as K  # noqa: E402
import run as R  # noqa: E402

from OCP.BRep import BRep_Tool  # noqa: E402
from OCP.BRepAdaptor import BRepAdaptor_Surface  # noqa: E402
from OCP.BRepAlgoAPI import BRepAlgoAPI_Splitter  # noqa: E402
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeVertex  # noqa: E402
from OCP.BRepClass import BRepClass_FaceClassifier  # noqa: E402
from OCP.BRepClass3d import BRepClass3d_SolidClassifier  # noqa: E402
from OCP.BRepExtrema import BRepExtrema_DistShapeShape  # noqa: E402
from OCP.GeomAbs import GeomAbs_BezierSurface  # noqa: E402
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_IN, TopAbs_ON, TopAbs_VERTEX  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopoDS import TopoDS  # noqa: E402

KERNEL_FS = os.path.join(FSROOT, "src", "10_kernel.fs")
LAYOUT_JSON = os.path.join(PKG, "04-vision", "apriltag-field-layout.json")
SCRATCH_STD = "/tmp/claude-0/-home-user-SUMMIT-PUSH/2d3069ce-8855-52b5-8721-54e54f71c127/scratchpad/std"


# ======================================================================================
# helpers
# ======================================================================================
def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _std_dir():
    cands = [os.environ.get("FS_STD"), SCRATCH_STD] + sorted(glob.glob("/tmp/claude-*/*/*/scratchpad/std"))
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "geomOperations.fs")):
            return c
    return None


def _fs_functions(text):
    """name -> (params, body) for every top-level `function` in a FeatureScript file."""
    out = {}
    for m in re.finditer(r"^function\s+(\w+)\s*\(([^)]*)\)[^\n]*\n\{\n(.*?)^\}", text, re.M | re.S):
        out[m.group(1)] = (m.group(2), m.group(3))
    return out


def _squash(s):
    s = re.sub(r"\n[ \t]*\*+(?!/)[ \t]?", "\n", s)      # join /** ... */ doc-comment continuation lines
    return re.sub(r"\s+", " ", s)


def _vertices(shape):
    out = []
    exp = TopExp_Explorer(shape, TopAbs_VERTEX)
    while exp.More():
        p = BRep_Tool.Pnt_s(TopoDS.Vertex(exp.Current()))
        out.append((p.X(), p.Y(), p.Z()))
        exp.Next()
    return np.unique(np.round(np.array(out), 9), axis=0)


def _subshapes(shape, kind):
    """Distinct sub-shapes (an explorer visits a shared edge once per adjacent face)."""
    out = []
    exp = TopExp_Explorer(shape, kind)
    while exp.More():
        c = exp.Current()
        if not any(c.IsSame(o) for o in out):
            out.append(c)
        exp.Next()
    return out


def _dist(a, b):
    d = BRepExtrema_DistShapeShape(a, b)
    return d.Value() if d.IsDone() else float("inf")


def _vtx(p):
    return BRepBuilderAPI_MakeVertex(K._gp(p)).Vertex()


def _same_points(a, b, tol=1e-7):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if a.shape != b.shape:
        return False, "vertex count %d vs reference %d" % (len(a), len(b))
    worst = 0.0
    for p in b:
        worst = max(worst, float(np.min(np.linalg.norm(a - p, axis=1))))
    return worst < tol, "worst vertex offset %.2e in" % worst


def _inside(solids, p):
    for s in solids:
        st = BRepClass3d_SolidClassifier(s, K._gp(p), 1e-7).State()
        if st in (TopAbs_IN, TopAbs_ON):
            return True
    return False


class Ref:
    """Onshape conventions, written from the std library and the kernel's FeatureScript text:
    toWorld / CoordSystem: y = cross(zAxis, xAxis)            (std coordSystem.fs)
    kPlane: plane(kPt(F, o) + n * offset, n, kDir(F, x))      (src/10_kernel.fs)
    sketch on a Plane: planeToCSys -> (u, v) along (x, cross(normal, x))   (std surfaceGeometry.fs)
    opExtrude from the sketch plane along `direction` by endDepth (std geomOperations.fs)."""

    @staticmethod
    def frame(o, x, z):
        x = np.asarray(x, float) / np.linalg.norm(x)
        z = np.asarray(z, float) / np.linalg.norm(z)
        return np.asarray(o, float), x, np.cross(z, x), z

    @staticmethod
    def pt(Fr, p):
        o, x, y, z = Fr
        return o + x * p[0] + y * p[1] + z * p[2]

    @staticmethod
    def dir(Fr, d):
        o, x, y, z = Fr
        v = x * d[0] + y * d[1] + z * d[2]
        return v / np.linalg.norm(v)

    @staticmethod
    def plane(Fr, pl, off):
        n = Ref.dir(Fr, pl[1])
        x = Ref.dir(Fr, pl[2])
        return Ref.pt(Fr, pl[0]) + n * off, x, np.cross(n, x), n

    @staticmethod
    def prism_vertices(Fr, pl, pts, d0, d1):
        o, x, v, n = Ref.plane(Fr, pl, d0)
        out = []
        for (a, b) in pts:
            for t in (0.0, d1 - d0):
                out.append(o + x * a + v * b + n * t)
        return np.unique(np.round(np.array(out), 9), axis=0)


def _kf(o, x, z):
    return K.frameMake(o, x, z)


# ======================================================================================
# [src] conformance of kernel text, std text and twin
# ======================================================================================
def _src_checks(out, std):
    ktxt = _read(KERNEL_FS)
    kf = _fs_functions(ktxt)

    def body(name):
        return _squash(kf.get(name, ("", ""))[1])

    # frames: y = z x x in the kernel, the twin and the std toWorld
    ok_k = body("kPt").count("cross(F.zAxis, F.xAxis)") == 1 and body("kDir").count("cross(F.zAxis, F.xAxis)") == 1
    Fr = K.frameMake([1, 2, 3], [math.cos(0.3), math.sin(0.3), 0.2], [-0.2 * math.cos(0.3), -0.2 * math.sin(0.3), 1])
    ok_t = np.allclose(Fr.y, np.cross(Fr.z, Fr.x), atol=1e-15)
    detail = "kernel kPt/kDir yAxis = cross(F.zAxis, F.xAxis): %s; twin Frame.y = cross(z, x): %s" % (ok_k, ok_t)
    ok_s = True
    if std:
        cs = _squash(_read(os.path.join(std, "coordSystem.fs")))
        ok_s = "matrix([cSys.xAxis, cross(cSys.zAxis, cSys.xAxis), cSys.zAxis])" in cs
        detail += "; std toWorld uses cross(cSys.zAxis, cSys.xAxis): %s" % ok_s
        # twin toWorld (copyBody / measureBox frame) columns are x, z x x, z and origin
        t = Fr.trsf()
        m = np.array([[t.Value(r, c) for c in range(1, 5)] for r in range(1, 4)])
        ok_s = ok_s and np.allclose(m[:, 0], Fr.x) and np.allclose(m[:, 1], np.cross(Fr.z, Fr.x)) and np.allclose(m[:, 3], Fr.o)
    out.append(("[src] frame handedness y = z x x (kernel kPt/kDir, std toWorld, twin Frame/trsf)", ok_k and ok_t and ok_s, detail))

    # sketch plane (u, v) = (x, normal x x)
    kp = body("kPlane")
    ok_k = "plane(kPt(F, pl[0]) + n * offset * inch, n, kDir(F, pl[2]))" in kp and "kDir(F, pl[1])" in kp
    P = K._Plane(Fr, [[1, 1, 1], [0, 0, 1], [1, 0, 0]], 2.5)
    ok_t = np.allclose(P.y, np.cross(P.n, P.x)) and np.allclose(P.o, Fr.pt([1, 1, 1]) + Fr.dir([0, 0, 1]) * 2.5)
    detail = "kernel kPlane offset along the normal: %s; twin _Plane v = n x x and offset: %s" % (ok_k, ok_t)
    ok_s = True
    if std:
        sg = _squash(_read(os.path.join(std, "surfaceGeometry.fs")))
        sk = _squash(_read(os.path.join(std, "sketch.fs")))
        ok_s = ("return coordSystem(plane.origin, plane.x, plane.normal);" in sg
                and "The sketch coordinate system will match the coordinate system of the plane" in sk)
        detail += "; std planeToCSys(origin, x, normal) and newSketchOnPlane 'matches the plane': %s" % ok_s
    out.append(("[src] sketch coordinates on plane(origin, normal, x): u = x, v = normal x x", ok_k and ok_t and ok_s, detail))

    # extrude
    mp = body("mkPrismProfile")
    need = ["const P = kPlane(F, pl, d0);", '"direction" : P.normal', '"endDepth" : (d1 - d0) * inch',
            "qSketchRegion(skId, true)", '"endBound" : BoundingType.BLIND']
    miss = [n for n in need if n not in mp]
    tw = _squash(inspect.getsource(K.mkPrismProfile))
    ok_t = "P = _Plane(F, pl, d0)" in tw and "gp_Vec(*(P.n * (d1 - d0)))" in tw
    out.append(("[src] mkPrismProfile: sketch plane at d0, extrude along +normal by d1 - d0 (kernel and twin)",
                not miss and ok_t, "kernel missing %s; twin prism vector P.n*(d1-d0): %s" % (miss or "nothing", ok_t)))

    # revolve
    rv = body("mkRevolve")
    need = ["const P = kPlane(F, pl, 0);", '"axis" : line(P.origin, cross(P.normal, P.x))', '"endBoundAngle" : 2 * PI * radian',
            '"startBoundAngle" : 0 * radian', '"endBound" : RevolveBoundingType.BLIND', '"startBound" : RevolveBoundingType.BLIND']
    miss = [n for n in need if n not in rv]
    tw = _squash(inspect.getsource(K.mkRevolve))
    ok_t = "gp_Ax1(_gp(P.o), _gd(P.y))" in tw and "2 * PI" in tw
    detail = "kernel missing %s; twin axis = (P.o, P.y = n x x), 2*PI: %s" % (miss or "nothing", ok_t)
    ok_s = True
    if std:
        rs = _squash(_read(os.path.join(std, "revolve.fs")))
        ok_s = ("definition.endBound = RevolveBoundingType.BLIND; definition.endBoundAngle = 2 * PI * radian; "
                "definition.startBound = RevolveBoundingType.BLIND; definition.startBoundAngle = 0 * radian;") in rs
        detail += "; std revolve.fs full-revolve branch passes the same bounds to opRevolve: %s" % ok_s
    out.append(("[src] mkRevolve: full 360 about the sketch v axis through the plane origin", not miss and ok_t and ok_s, detail))

    if not std:
        out.append(("[src] std-library conformance (opShell sign, B-spline knots, opPattern properties, union identity, "
                    "qCreatedBy split rule)", True, "SKIPPED: FeatureScript std library not found (set FS_STD)"))
        return
    geo = _squash(_read(os.path.join(std, "geomOperations.fs")))
    sgf = _squash(_read(os.path.join(std, "surfaceGeometry.fs")))
    qry = _squash(_read(os.path.join(std, "query.fs")))
    ok = "Positive means shell outward, and negative means shell inward" in geo and '"thickness" : -t * inch' in body("shellHollow")
    out.append(("[src] shellHollow: opShell thickness -t is inward (std doc) = twin inward offset", ok,
                "std: 'negative means shell inward'; kernel passes -t * inch; twin MakeThickSolidByJoin(-t)"))
    ok = ("If knots are not provided a uniform parameterization will be created" in sgf
          and "definition.uKnots is undefined ||" in sgf and "uKnots" not in body("mkPillowBox")
          and '"uDegree" : 2' in body("mkPillowBox"))
    out.append(("[src] mkPillowBox: degree-2 3x3 net with default (clamped uniform) knots = the twin's Bezier patch", ok,
                "std bSplineSurface pads missing knots to [0,0,0,1,1,1]; kernel passes none; twin Geom_BezierSurface"))
    ok = "copyPropertiesAndAttributes {boolean} : If true (default), copies properties and attributes" in geo \
        and "copyPropertiesAndAttributes" not in body("copyBody")
    out.append(("[src] copyBody: opPattern copies name/appearance/material/face styles by default = twin copies them", ok,
                "std opPattern copyPropertiesAndAttributes defaults to true; kernel leaves it unset"))
    ok = "the identity of the tool that appears earliest in the query is preserved" in geo
    out.append(("[src] bUnion survivor: std keeps the earliest tool in the query = twin keeps keys[0]", ok,
                "std opBoolean UNION doc; twin bUnion keeps context.bodies[keys[0]]"))
    ok = ('If an entity is split (as in a split part operation), the resulting entities are "created by" both the '
          "original entity's creator and the split part operation.") in qry
    out.append(("[src] split bodies: std qCreatedBy keeps every piece under the original creator = twin keeps all "
                "pieces under the target key", ok, "std query.fs qCreatedBy doc"))

    # warnings on sub-feature ids never reach the feature's status in Onshape
    err = _squash(_read(os.path.join(std, "error.fs")))
    boo = _squash(_read(os.path.join(std, "boolean.fs")))
    std_needs_propagation = ("Propagate the status of a subfeature to a feature" in err
                             and "if (id != topLevelId) { processSubfeatureStatus(context, topLevelId" in boo)
    sub_id_reports = []
    for fn in ("softFilletAt", "tagDecal"):
        b = body(fn)
        if "reportFeatureWarning(context, id," in b:
            sub_id_reports.append(fn)
    ok = not (std_needs_propagation and sub_id_reports)
    out.append(("[src] kernel warnings reach the SUMMIT PUSH Field feature status", ok,
                "%s call reportFeatureWarning(context, id, ...) with the operation sub-id they were given "
                "(e.g. F/wallBlue/sill0, F/tags/decal7); std attaches a status to exactly that id and only "
                "processSubfeatureStatus lifts it to the feature (boolean.fs:1410), so in Onshape the skipped-"
                "roundover / missing-decal warnings are invisible, and the top-level self-check info "
                "'all N dimension checks pass' is what the user sees. The twin instead collects them in "
                "ctx.warnings and run.py prints them." % (", ".join(sub_id_reports) or "no kernel function")))


# ======================================================================================
# [conv] tiny parts: twin vs the independent Onshape-convention model
# ======================================================================================
def _conv_checks(out):
    s30, c30 = math.sin(math.radians(30)), math.cos(math.radians(30))
    s15, c15 = math.sin(math.radians(15)), math.cos(math.radians(15))
    frames = {
        "world": ([0, 0, 0], [1, 0, 0], [0, 0, 1]),
        "red alliance": ([648, 324, 0], [-1, 0, 0], [0, 0, 1]),
        "yawed 30": ([10, -5, 3], [c30, s30, 0], [0, 0, 1]),
        "x up": ([1, 2, 3], [0, 0, 1], [1, 0, 0]),
        "tilted 15": ([48, 0, 0], [c15, 0, s15], [-s15, 0, c15]),
    }
    planes = {
        "plXY(2)": [[0, 0, 2], [0, 0, 1], [1, 0, 0]],
        "plYZ(-1)": [[-1, 0, 0], [1, 0, 0], [0, 1, 0]],
        "plXZ(3)": [[0, 3, 0], [0, -1, 0], [1, 0, 0]],
        "ramp 30": [[1, 2, 3], [s30, 0, c30], [-c30, 0, s30]],
        "plAxis": [[0.5, 0, 0], [0, -1, 0], [0, 0, 1]],
    }
    pts = [[0, 0], [3, 0], [3, 1], [1, 2.5], [-0.5, 1.5]]     # asymmetric: a mirror shows up
    bad = []
    n = 0
    for fname, fr in frames.items():
        for pname, pl in planes.items():
            reg = K.Registry()
            K.mkPrism(reg, K.Id(("T", "p")), _kf(*fr), pl, pts, -0.75, 1.25)
            got = _vertices(K._compound(reg.solids_for([K.Id(("T",))])))
            ref = Ref.prism_vertices(Ref.frame(*fr), pl, pts, -0.75, 1.25)
            ok, why = _same_points(got, ref)
            n += 1
            if not ok:
                bad.append("%s/%s: %s" % (fname, pname, why))
    out.append(("[conv] mkPrism vertices = Onshape model (5 frames x 5 planes, asymmetric profile, d0 < 0 < d1)",
                not bad, "%d cases; %s" % (n, "; ".join(bad) or "all vertices within 1e-7 in")))

    # revolve: rectangle profile u 1..2, v 0.5..3 about the v axis
    fr = ([1, 2, 3], [c30, s30, 0], [0, 0, 1])
    Fr = Ref.frame(*fr)
    pl = [[2, -1, 0.5], [0, -1, 0], [1, 0, 0]]              # normal -y, u = +x, v = z
    o, ux, vv, nn = Ref.plane(Fr, pl, 0)
    reg = K.Registry()
    loop = [["L", [1, 0.5], [2, 0.5]], ["L", [2, 0.5], [2, 3]], ["L", [2, 3], [1, 3]], ["L", [1, 3], [1, 0.5]]]
    K.mkRevolve(reg, K.Id(("T", "r")), _kf(*fr), pl, loop)
    sol = reg.solids_for([K.Id(("T", "r"))])
    vol = K._volume(sol)
    want = math.pi * (4 - 1) * 2.5
    side = np.cross(vv, ux)                                  # 90 degrees round the axis
    probes = {"r1.5 h1.75 @90deg": (o + side * 1.5 + vv * 1.75, True), "r0.5 h1.75": (o + ux * 0.5 + vv * 1.75, False),
              "r1.5 h-1.75 (mirror)": (o - ux * 1.5 - vv * 1.75, False), "r1.5 h2.9 @180": (o - ux * 1.5 + vv * 2.9, True)}
    wrong = [k for k, (p, w) in probes.items() if _inside(sol, p) != w]
    bb = K.measureBox(reg, [K.Id(("T", "r"))], K.Frame(o, ux, vv))
    okb = np.allclose(bb, [-2, -2, 0.5, 2, 2, 3], atol=1e-6)
    out.append(("[conv] mkRevolve: 360 deg about the sketch v axis through the plane origin", abs(vol - want) < 1e-6 and not wrong and okb,
                "volume %.6f vs pi*(2^2-1^2)*2.5 = %.6f; wrong probes %s; box in axis frame %s" % (vol, want, wrong or "none", np.round(bb, 6).tolist())))

    # revolve of a single circle (the twin's torus special case)
    reg = K.Registry()
    K.mkRevolve(reg, K.Id(("T", "t")), _kf(*fr), pl, [["C", [3, 1], 0.5]])
    sol = reg.solids_for([K.Id(("T", "t"))])
    vol = K._volume(sol)
    want = 2 * math.pi ** 2 * 3 * 0.25
    bb = K.measureBox(reg, [K.Id(("T", "t"))], K.Frame(o, ux, vv))
    okp = _inside(sol, o + side * 3 + vv * 1) and not _inside(sol, o + side * 3 - vv * 1)
    out.append(("[conv] mkRevolve single-circle profile (twin builds the torus directly) = revolve of the circle",
                abs(vol - want) < 1e-6 and np.allclose(bb, [-3.5, -3.5, 0.5, 3.5, 3.5, 1.5], atol=1e-5) and okp,
                "volume %.6f vs 2 pi^2 R r^2 = %.6f; box %s; tube centre on +v side: %s" % (vol, want, np.round(bb, 6).tolist(), okp)))

    # pillow box: volume and extents, and the net against the kernel's own expressions
    h, crown = 6.0, 0.5
    fr = ([5, -3, 7], [c30, 0, s30], [-s30, 0, c30])
    reg = K.Registry()
    K.mkPillowBox(reg, K.Id(("T", "b")), _kf(*fr), h, crown)
    sol = reg.solids_for([K.Id(("T", "b"))])
    vol = K._volume(sol)
    want = 8 * h ** 3 + 6 * (2 * h) ** 2 * (4 * crown) / 9.0     # biquadratic bump: centre pole 4*crown, mean 4*crown/9
    bb = K.measureBox(reg, [K.Id(("T", "b"))], _kf(*fr))
    okb = np.allclose(bb, [-h - crown, -h - crown, -h - crown, h + crown, h + crown, h + crown], atol=1e-6)
    edge_mid = Ref.pt(Ref.frame(*fr), [h, h, 0])
    d_edge = _dist(_vtx(edge_mid), sol[0])
    out.append(("[conv] mkPillowBox: flat on the cube edges, crown at each face centre, volume 8h^3 + 32 h^2 crown / 3",
                abs(vol - want) < 1e-6 and okb and d_edge < 1e-9,
                "volume %.6f vs %.6f; box %s vs +/-%.3f; cube-edge midpoint on the surface: %.1e" % (vol, want, np.round(bb, 6).tolist(), h + crown, d_edge)))
    ok, why = _pillow_net_vs_kernel(reg, K.Id(("T", "b")), fr, h, crown)
    out.append(("[conv] mkPillowBox control nets: twin Bezier poles = nets from the kernel's FeatureScript expressions", ok, why))

    # shell (no faces removed) = inward hollow
    fr = ([2, 3, 4], [0, 1, 0], [0, 0, 1])
    reg = K.Registry()
    K.mkPrism(reg, K.Id(("T", "s")), _kf(*fr), [[0, 0, 0], [0, 0, 1], [1, 0, 0]], [[0, 0], [10, 0], [10, 8], [0, 8]], 0, 6)
    K.shellHollow(reg, K.Id(("T", "sh")), [K.Id(("T", "s"))], 1.0)
    vol = K.measureVolume(reg, [K.Id(("T", "s"))])
    dcen = K.measureDistToPoint(reg, [K.Id(("T", "s"))], _kf(*fr), [5, 4, 3])
    bb = K.measureBox(reg, [K.Id(("T", "s"))], _kf(*fr))
    out.append(("[conv] shellHollow: opShell of a body, thickness -t = walls grown inward, closed void",
                abs(vol - (480 - 8 * 6 * 4)) < 1e-6 and abs(dcen - 2) < 1e-9 and np.allclose(bb, [0, 0, 0, 10, 8, 6], atol=1e-6),
                "volume %.6f vs 480 - 192 = 288; centre-to-wall %.6f vs 2; outer box %s" % (vol, dcen, np.round(bb, 6).tolist())))

    # booleans
    W = _kf([0, 0, 0], [1, 0, 0], [0, 0, 1])
    pz = [[0, 0, 0], [0, 0, 1], [1, 0, 0]]

    def box(reg, key, x0, y0, z0, x1, y1, z1):
        K.mkPrism(reg, K.Id(key), W, pz, [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], z0, z1)

    reg = K.Registry()
    box(reg, ("T", "a"), 0, 0, 0, 4, 4, 4)
    box(reg, ("T", "k"), 1, 1, -1, 2, 2, 5)
    box(reg, ("T", "c"), 0, 0, 10, 4, 4, 14)
    box(reg, ("T", "d"), 1, 1, 9, 2, 2, 15)
    K.bSubtract(reg, K.Id(("T", "s1")), [K.Id(("T", "a"))], [K.Id(("T", "k"))], True)
    K.bSubtract(reg, K.Id(("T", "s2")), [K.Id(("T", "c"))], [K.Id(("T", "d"))], False)
    ok = (abs(K.measureVolume(reg, [K.Id(("T", "a"))]) - 60) < 1e-9 and K.countBodies(reg, [K.Id(("T", "k"))]) == 1
          and K.countBodies(reg, [K.Id(("T", "d"))]) == 0 and abs(K.measureVolume(reg, [K.Id(("T", "c"))]) - 60) < 1e-9)
    out.append(("[conv] bSubtract: union of tools removed from every target; keepTools keeps / consumes the tools", ok,
                "through-hole volumes 60/60; kept tool %d body, consumed tool %d bodies" % (
                    K.countBodies(reg, [K.Id(("T", "k"))]), K.countBodies(reg, [K.Id(("T", "d"))]))))
    box(reg, ("T", "bar"), 0, 20, 0, 10, 21, 1)
    box(reg, ("T", "slab"), 4, 19, -1, 6, 22, 2)
    K.bSubtract(reg, K.Id(("T", "split")), [K.Id(("T", "bar"))], [K.Id(("T", "slab"))], False)
    nb = K.countBodies(reg, [K.Id(("T", "bar"))])
    out.append(("[conv] a subtraction that splits a body: every piece still answers to the original creator's Id",
                nb == 2, "pieces under the bar's Id: %d (std qCreatedBy: 2)" % nb))

    reg = K.Registry()
    box(reg, ("T", "u1"), 0, 0, 0, 2, 2, 2)
    box(reg, ("T", "u2"), 1, 1, 1, 3, 3, 3)
    K.styleBody(reg, [K.Id(("T", "u1"))], "first", [1, 2, 3], 1, {"name": "m1", "density": 1})
    K.styleBody(reg, [K.Id(("T", "u2"))], "second", [4, 5, 6], 1, {"name": "m2", "density": 2})
    K.bUnion(reg, K.Id(("T", "join")), [K.Id(("T", "u1")), K.Id(("T", "u2"))])
    recs = list(reg.bodies.values())
    ok = len(recs) == 1 and recs[0]["name"] == "first" and abs(K._volume(recs[0]["solids"]) - 15) < 1e-9
    out.append(("[conv] bUnion: one body, name and colour of the earliest tool (std opBoolean UNION)", ok,
                "bodies %d, name %r, volume %.6f (8 + 8 - 1 = 15)" % (len(recs), recs[0]["name"] if recs else None,
                                                                         K._volume(recs[0]["solids"]) if recs else float("nan"))))

    # qCreatedBy prefix semantics vs the Registry lookup
    reg = K.Registry()
    box(reg, ("a", "b", "ex"), 0, 0, 0, 1, 1, 1)
    box(reg, ("a", "bc", "ex"), 5, 0, 0, 6, 1, 1)
    ok = reg.keys_for([K.Id(("a", "b"))]) == [K.Id(("a", "b", "ex", "ex"))] and len(reg.keys_for([K.Id(("a",))])) == 2
    out.append(("[conv] Registry lookup = qCreatedBy: whole-component Id prefix ('b' does not match 'bc')", ok,
                "keys for a/b: %s" % [str(k) for k in reg.keys_for([K.Id(("a", "b"))])]))

    # copyBody = opPattern with toWorld(F)
    reg = K.Registry()
    box(reg, ("T", "m"), 0, 0, 0, 1, 2, 3)
    fr = ([10, 20, 30], [c30, s30, 0], [0, 0, 1])
    K.copyBody(reg, K.Id(("T", "cp")), [K.Id(("T", "m"))], _kf(*fr))
    got = _vertices(K._compound(reg.solids_for([K.Id(("T", "cp"))])))
    Fr = Ref.frame(*fr)
    ref = np.unique(np.round(np.array([Ref.pt(Fr, [x, y, z]) for x in (0, 1) for y in (0, 2) for z in (0, 3)]), 9), axis=0)
    ok, why = _same_points(got, ref)
    out.append(("[conv] copyBody places the world-origin master by toWorld(F) (origin + x, z x x, z columns)", ok, why))

    # measureBox in a frame
    reg = K.Registry()
    K.mkPrism(reg, K.Id(("T", "q")), _kf(*fr), pz, [[1, 2], [4, 2], [4, 6], [1, 6]], 3, 7)
    bb = K.measureBox(reg, [K.Id(("T", "q"))], _kf(*fr))
    out.append(("[conv] measureBox(F) = evBox3d with cSys F: the box in F's own coordinates", np.allclose(bb, [1, 2, 3, 4, 6, 7], atol=1e-7),
                "got %s" % np.round(bb, 7).tolist()))

    # massBody density
    reg = K.Registry()
    box(reg, ("T", "w"), 0, 0, 0, 2, 3, 4)
    rho = K.massBody(reg, [K.Id(("T", "w"))], "x", 1.0)
    want = 0.45359237 / (24 * 0.0254 ** 3)
    out.append(("[conv] massBody: density = massLb * pound / evVolume (kg/m^3)", abs(rho - want) < 1e-9 * want,
                "%.6f vs 1 lb / 24 in^3 = %.6f kg/m^3" % (rho, want)))

    # fillet edge selection by point (qContainsPoint semantics) and a real fillet
    reg = K.Registry()
    box(reg, ("T", "f"), 0, 0, 0, 4, 4, 4)
    s = reg.solids_for([K.Id(("T", "f"))])[0]
    n_mid = len(K._edges_through(s, [np.array([2.0, 0, 0])]))
    n_vtx = len(K._edges_through(s, [np.array([0.0, 0, 0])]))
    K.filletAt(reg, K.Id(("T", "fr")), [K.Id(("T", "f"))], W, [[2, 0, 0]], 0.5)
    dv = 64 - K.measureVolume(reg, [K.Id(("T", "f"))])
    want = (1 - math.pi / 4) * 0.25 * 4
    out.append(("[conv] filletAt selects edges by point like qContainsPoint (midpoint: 1 edge, vertex: 3) and fillets them",
                n_mid == 1 and n_vtx == 3 and abs(dv - want) < 1e-6,
                "edges through a midpoint %d, through a vertex %d; R0.5 x 4 in edge removes %.6f vs %.6f in^3" % (n_mid, n_vtx, dv, want)))


def _fs_expr_to_py(e):
    e = e.replace("&&", " and ").replace("||", " or ")
    # (COND) ? A : B  ->  (A if COND else B)   (the only ternary shape the kernel uses)
    m = re.search(r"\(\(([^()]*)\)\s*\?\s*([^:()]+?)\s*:\s*([^()]+?)\)", e)
    if m:
        e = e[:m.start()] + "((%s) if (%s) else (%s))" % (m.group(2), m.group(1), m.group(3)) + e[m.end():]
    return e


def _pillow_net_vs_kernel(reg, key, fr, h, crown):
    kb = _squash(_fs_functions(_read(KERNEL_FS))["mkPillowBox"][1])
    try:
        ea = re.search(r"const a = (.+?);", kb).group(1)
        eb = re.search(r"const b = (.+?);", kb).group(1)
        ec = re.search(r"const c = (.+?);", kb).group(1)
        assign = re.findall(r"p\[([^\]]+)\] = (\w+);", kb)
        loops = ("for (var ax = 0; ax < 3; ax += 1)" in kb and "for (var sgn in [-1, 1])" in kb
                 and "for (var i = 0; i < 3; i += 1)" in kb and "for (var j = 0; j < 3; j += 1)" in kb)
    except AttributeError:
        return False, "could not parse the kernel's mkPillowBox expressions"
    if len(assign) != 3 or not loops:
        return False, "kernel mkPillowBox loop/assignment shape changed: %s" % assign
    Fr = Ref.frame(*fr)
    fs_nets = []
    for ax in range(3):
        for sgn in (-1, 1):
            net = []
            for i in range(3):
                for j in range(3):
                    env = {"i": i, "j": j, "h": h, "sgn": sgn, "crown": crown, "ax": ax}
                    env["a"] = eval(_fs_expr_to_py(ea), {}, dict(env))
                    env["b"] = eval(_fs_expr_to_py(eb), {}, dict(env))
                    env["c"] = eval(_fs_expr_to_py(ec), {}, dict(env))
                    p = [0.0, 0.0, 0.0]
                    for idx, var in assign:
                        p[int(eval(idx, {}, dict(env)))] = env[var]
                    net.append(Ref.pt(Fr, p))
            fs_nets.append(np.array(net))
    tw_nets = []
    for s in reg.solids_for([key]):
        for fc in _subshapes(s, TopAbs_FACE):
            ad = BRepAdaptor_Surface(TopoDS.Face(fc))
            if ad.GetType() != GeomAbs_BezierSurface:
                return False, "twin face is not a Bezier patch"
            bz = ad.Bezier()
            tw_nets.append(np.array([[bz.Pole(i, j).X(), bz.Pole(i, j).Y(), bz.Pole(i, j).Z()]
                                     for i in range(1, bz.NbUPoles() + 1) for j in range(1, bz.NbVPoles() + 1)]))
    if len(tw_nets) != 6:
        return False, "twin pillow has %d faces" % len(tw_nets)
    worst = 0.0
    for fn in fs_nets:
        best = min(max(float(np.min(np.linalg.norm(tn - q, axis=1))) for q in fn) for tn in tw_nets)
        worst = max(worst, best)
    return worst < 1e-9, "6 nets from the kernel text (a, b, c, p[...] assignments) vs twin poles: worst pole offset %.1e in" % worst


# ======================================================================================
# [twin] latent divergences, each demonstrated
# ======================================================================================
def _run_fs(snippet, fname="<demo>"):
    """Lint + transpile a part-code snippet exactly as run.py does and return its namespace."""
    errs = fs2py.lint(snippet, fname)
    ns = {}
    for name in dir(K):
        if not name.startswith("_"):
            ns[name] = getattr(K, name)
    exec(fs2py.PRELUDE, ns)
    exec(compile(fs2py.transpile(snippet, fname), fname, "exec"), ns)
    return errs, ns


def _import_build():
    if FSROOT not in sys.path:
        sys.path.insert(0, FSROOT)
    import build as B  # noqa: E402
    return B


def _twin_checks(out, std):
    tol = 1e-11
    if std:
        m = re.search(r'"zeroAngle"\s*:\s*([0-9.eE+-]+)', _read(os.path.join(std, "math.fs")))
        if m:
            tol = float(m.group(1))
    # perpendicularity tolerance
    acc_p = acc_f = True
    try:
        K._Plane(_kf([0, 0, 0], [1, 0, 0], [0, 0, 1]), [[0, 0, 0], [0, 0, 1], [1, 0, 1e-10]], 0)
    except K.KernelError:
        acc_p = False
    try:
        K.frameMake([0, 0, 0], [1, 0, 1e-10], [0, 0, 1])
    except K.KernelError:
        acc_f = False
    out.append(("[twin] plane()/coordSystem() perpendicularity tolerance = std TOLERANCE.zeroAngle", not acc_p and not acc_f,
                "std: plane() is cast `as Plane` requiring |x.n| < %g and coordSystem() has precondition "
                "perpendicularVectors (|x.z| < %g); twin _Plane/Frame reject only above 1e-9, so a plane with "
                "|x.n| = 1e-10 %s and a frame with |x.z| = 1e-10 %s in the twin but throw in Onshape "
                "(kernel_occ.py:149, :187)" % (tol, tol, "is accepted" if acc_p else "is rejected",
                                                 "is accepted" if acc_f else "is rejected")))

    # softFilletAt all-or-nothing
    W = _kf([0, 0, 0], [1, 0, 0], [0, 0, 1])
    reg = K.Registry()
    K.mkPrism(reg, K.Id(("T", "f")), W, [[0, 0, 0], [0, 0, 1], [1, 0, 0]], [[0, 0], [4, 0], [4, 4], [0, 4]], 0, 4)
    K.softFilletAt(reg, K.Id(("T", "r")), [K.Id(("T", "f"))], W, [[2, 0, 0], [9, 9, 9]], 0.5, "demo")
    dv = 64 - K.measureVolume(reg, [K.Id(("T", "f"))])
    out.append(("[twin] softFilletAt with one point off every edge still fillets the matched edges (as in Onshape)",
                dv > 1e-6, "FS filletAt unions one qContainsPoint query per point, so an unmatched point adds "
                           "nothing and the edge at (2,0,0) is filleted; the twin's filletAt raises on the unmatched "
                           "point, softFilletAt swallows it and skips the whole roundover (volume change %.6f, "
                           "warning %r) - kernel_occ.py:536-538, :556-559" % (dv, reg.warnings[-1][:60] if reg.warnings else None)))

    # union: consumed id no longer answers
    reg = K.Registry()
    for key, x0 in (("u1", 0), ("u2", 1)):
        K.mkPrism(reg, K.Id(("T", key)), W, [[0, 0, 0], [0, 0, 1], [1, 0, 0]], [[x0, 0], [x0 + 2, 0], [x0 + 2, 2], [x0, 2]], 0, 2)
    K.bUnion(reg, K.Id(("T", "join")), [K.Id(("T", "u1")), K.Id(("T", "u2"))])
    n2 = K.countBodies(reg, [K.Id(("T", "u2"))])
    nj = K.countBodies(reg, [K.Id(("T", "join"))])
    out.append(("[twin] after bUnion every merged creator and the union op still resolve to the merged body",
                n2 == 1 and nj == 1, "std qCreatedBy: a merged entity is 'created by' the creators of each merged entity "
                                     "and the merging operation; twin: qCreatedBy(u2) -> %d bodies, qCreatedBy(join) -> %d "
                                     "(kernel_occ.py:469-471 keeps only keys[0])" % (n2, nj)))

    # split: the splitting op is also a creator
    reg = K.Registry()
    K.mkPrism(reg, K.Id(("T", "bar")), W, [[0, 0, 0], [0, 0, 1], [1, 0, 0]], [[0, 0], [10, 0], [10, 1], [0, 1]], 0, 1)
    K.mkPrism(reg, K.Id(("T", "slab")), W, [[0, 0, 0], [0, 0, 1], [1, 0, 0]], [[4, -1], [6, -1], [6, 2], [4, 2]], -1, 2)
    K.bSubtract(reg, K.Id(("T", "cut")), [K.Id(("T", "bar"))], [K.Id(("T", "slab"))], False)
    nc = K.countBodies(reg, [K.Id(("T", "cut"))])
    out.append(("[twin] pieces of a split body also answer to the splitting operation's Id", nc == 2,
                "std qCreatedBy: split pieces are 'created by' both the original creator and the splitting "
                "operation; twin qCreatedBy(T/cut) -> %d bodies (expected 2)" % nc))

    # ---- fs2py: expression semantics ----
    errs, ns = _run_fs("function twA(a, b)\n{\n    return a + b;\n}\n\nfunction twS(a)\n{\n    return 2 * a;\n}\n")
    ra, rs = ns["twA"]([1, 2], [3, 4]), ns["twS"]([1, 2])
    out.append(("[twin] fs2py: array arithmetic means what it means in FeatureScript", ra == [4, 6] and rs == [2, 4],
                "std vector.fs: every non-empty array is a Vector, `[1,2] + [3,4]` = [4, 6] and `2 * [1,2]` = [2, 4]; "
                "the lint-clean (%d errors) snippet runs in the twin as list concatenation/repetition: %r, %r" % (len(errs), ra, rs)))

    errs, ns = _run_fs("function twC(a, b, c)\n{\n    if (a == b == c)\n    {\n        return 1;\n    }\n    return 0;\n}\n")
    r = ns["twC"](2, 2, 2)
    out.append(("[twin] fs2py/lint: chained comparisons are rejected (FeatureScript evaluates them pairwise)", bool(errs) or r == 0,
                "lint errors %d; FeatureScript has no chained comparisons - `a == b == c` is either rejected or read "
                "as (a == b) == c (2, 2, 2: true == 2 -> false), and `a < b < c` compares a boolean with a number - "
                "but the twin runs Python's chain a == b and b == c -> %r (fs2py.py:92-97 passes comparisons "
                "through unchanged)" % (len(errs), bool(r))))

    errs, ns = _run_fs("function twL()\n{\n    var n = 3;\n    var count = 0;\n    for (var i = 0; i < n; i += 1)\n    {\n"
                       "        n = 2;\n        count += 1;\n    }\n    return count;\n}\n\n"
                       "function twV()\n{\n    var count = 0;\n    for (var i = 0; i < 4; i += 1)\n    {\n        i += 1;\n"
                       "        count += 1;\n    }\n    return count;\n}\n")
    rl, rv = ns["twL"](), ns["twV"]()
    out.append(("[twin] fs2py: C-style for re-evaluates its bound and sees body writes to the loop variable", rl == 2 and rv == 2,
                "FS re-tests `i < n` each pass (bound shrinks 3 -> 2: 2 passes) and `i += 1` in the body skips "
                "(2 passes); _frange evaluates the bound once and ignores body writes: %d and %d passes" % (rl, rv)))

    def fs_loop(a, b, st, incl):
        x, n = a, 0
        while (x <= b) if incl else (x < b):
            n += 1
            x += st
        return n
    errs, ns = _run_fs("function twF(b, st)\n{\n    var n = 0;\n    for (var x = 0; x < b; x += st)\n    {\n        n += 1;\n"
                       "    }\n    return n;\n}\n\nfunction twG(b, st)\n{\n    var n = 0;\n    for (var x = 0; x <= b; x += st)\n"
                       "    {\n        n += 1;\n    }\n    return n;\n}\n")
    cases = [(1, 0.1), (1, 0.2), (0.3, 0.1), (5.5, 0.5), (84, 6)]
    bad = [(b, st, ns["twF"](b, st), fs_loop(0, b, st, False), ns["twG"](b, st), fs_loop(0, b, st, True))
           for b, st in cases if ns["twF"](b, st) != fs_loop(0, b, st, False) or ns["twG"](b, st) != fs_loop(0, b, st, True)]
    out.append(("[conv] fs2py float-step loops accumulate exactly like FeatureScript (same IEEE sums, < and <=)", not bad,
                "cases %s; mismatches %s" % (cases, bad or "none")))

    errs, ns = _run_fs("function twI(a, i)\n{\n    return a[i - 1];\n}\n")
    r = ns["twI"]([10, 20, 30], 0)
    out.append(("[twin] fs2py: a negative array index fails as it does in FeatureScript", False if r == 30 else True,
                "FS a[-1] throws (index out of range); the lint-clean snippet returns %r in the twin (Python wraps)" % r))

    errs, ns = _run_fs("function twB(n)\n{\n    if (n)\n    {\n        return 1;\n    }\n    return 0;\n}\n")
    r = ns["twB"](3)
    out.append(("[twin] fs2py: a non-boolean if-condition fails as it does in FeatureScript", r != 1,
                "FS requires a boolean condition; `if (n)` with n = 3 returns %r in the twin (lint errors %d)" % (r, len(errs))))

    snip = ("function twE(c)\n{\n    if (c)\n    {\n        var a = 1;\n    }\n    else\n    {\n        var a = 2;\n    }\n"
            "    return a;\n}\n")
    errs, ns = _run_fs(snip)
    r = ns["twE"](True)
    out.append(("[twin] fs2py/lint: a variable used outside the block that declared it is rejected", bool(errs),
                "FS variables are block-scoped (`a` is undefined at `return a`); lint errors %d, twin returns %r" % (len(errs), r)))

    errs, ns = _run_fs("function twK()\n{\n    const a = 1;\n    a = 2;\n    return a;\n}\n")
    r = ns["twK"]()
    out.append(("[twin] fs2py/lint: assignment to a const is rejected", bool(errs),
                "FS rejects `const a = 1; a = 2;`; lint errors %d, twin returns %r" % (len(errs), r)))

    errs, ns = _run_fs("function twM()\n{\n    var a = [1, 2];\n    var b = a;\n    b[0] = 5;\n    return a[0];\n}\n")
    r = ns["twM"]()
    out.append(("[twin] fs2py: arrays have value semantics (assignment copies)", r == 1,
                "FS arrays are values (std vector.fs operators write into their own copy); `var b = a; b[0] = 5;` "
                "leaves a[0] == 1 in FS; twin (aliased Python list) returns a[0] = %r; lint errors %d" % (r, len(errs))))

    errs, ns = _run_fs("function twT()\n{\n    return LB;\n}\n\nfunction twP()\n{\n    return \"a\" + \"b\";\n}\n")
    r1, r2 = ns["twT"](), ns["twP"]()
    api = None
    if std:
        api = _import_build().api_check("function twT()\n{\n    return LB;\n}\n", std)
    out.append(("[twin] lint/api_check reject names that exist only in the Python twin, and `+` on strings",
                bool(errs) or (api is not None and any("LB" in e for e in api)),
                "`return LB;` (a kernel_occ constant) and `\"a\" + \"b\"` are lint-clean (%d errors), run in the twin "
                "(%r, %r) and are errors in FS (undefined variable; no string +); build.py api_check only checks "
                "called names: %s" % (len(errs), r1, r2, api)))


# ======================================================================================
# [guard] instrumented rebuild: does the real build exercise any divergence?
# ======================================================================================
class _Instr(ast.NodeTransformer):
    OPS = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}
    CMP = {ast.Lt: "<", ast.Gt: ">", ast.LtE: "<=", ast.GtE: ">="}

    def _call(self, fn, args, node):
        return ast.copy_location(ast.Call(ast.Name(fn, ast.Load()), args, []), node)

    def visit_BinOp(self, node):
        self.generic_visit(node)
        op = self.OPS.get(type(node.op))
        if op is None:
            return node
        return self._call("_tw_bin", [ast.Constant(op), node.left, node.right, ast.Constant(node.lineno)], node)

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        op = self.OPS.get(type(node.op))
        if op is None or not isinstance(node.target, ast.Name):
            return node
        val = self._call("_tw_bin", [ast.Constant(op), ast.Name(node.target.id, ast.Load()), node.value, ast.Constant(node.lineno)], node)
        return ast.copy_location(ast.Assign([ast.Name(node.target.id, ast.Store())], val), node)

    def visit_If(self, node):
        self.generic_visit(node)
        node.test = self._call("_tw_bool", [node.test, ast.Constant(node.lineno)], node)
        return node

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        node.values = [self._call("_tw_bool", [v, ast.Constant(node.lineno)], node) for v in node.values]
        return node

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Not):
            node.operand = self._call("_tw_bool", [node.operand, ast.Constant(node.lineno)], node)
        return node

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if isinstance(node.ctx, ast.Load):
            return self._call("_tw_idx", [node.value, node.slice, ast.Constant(node.lineno)], node)
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if len(node.ops) == 1 and type(node.ops[0]) in self.CMP:
            return self._call("_tw_cmp", [ast.Constant(self.CMP[type(node.ops[0])]), node.left, node.comparators[0],
                                          ast.Constant(node.lineno)], node)
        return node


def _isnum(v):
    return isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, (bool, np.bool_))


FS_OPIDS = {   # sub-ids each kernel entry point hands to Onshape operations (checked against the kernel text)
    "mkPrismProfile": ["sk", "ex", "dl"], "mkPrism": ["sk", "ex", "dl"], "mkPrismHoles": ["sk", "ex", "dl"],
    "mkCyl": ["sk", "ex", "dl"], "mkTube": ["sk", "ex", "dl"], "mkRevolve": ["sk", "rv", "dl"],
    "mkPillowBox": ["face0n", "face0p", "face1n", "face1p", "face2n", "face2p", "ex", "dl"],
    "bSubtract": [None], "bUnion": [None], "bDelete": [None], "shellHollow": [None], "filletAt": [None],
    "softFilletAt": [None], "copyBody": [None], "tagDecal": ["sk", "sp", "dl"],
}
QUERY_PARAMS = ("bodies", "targets", "tools", "src", "a", "b")


def _opid_model_matches_kernel():
    kf = _fs_functions(_read(KERNEL_FS))
    bad = []
    for fn, subs in FS_OPIDS.items():
        b = kf.get(fn, ("", ""))[1]
        lits = set(re.findall(r'\bid \+ "(\w+)"', b))
        direct = bool(re.search(r"\((context, )?id,", b)) or bool(re.search(r"\bop\w+\(context, id,", b))
        want = set(s for s in subs if s and not s.startswith("face"))
        if fn == "mkPillowBox":
            if 'id + ("face" ~ ax ~ (sgn > 0 ? "p" : "n"))' not in _squash(b):
                bad.append(fn)
        if fn in ("mkPrism", "mkPrismHoles", "mkCyl", "mkTube"):
            if "mkPrismProfile(context, id," not in b:
                bad.append(fn)
            continue
        if fn == "softFilletAt":
            if "filletAt(context, id," not in b:
                bad.append(fn)
            continue
        if None in subs and not direct:
            bad.append(fn)
        if lits - {"dl2"} != want:
            bad.append("%s %s vs %s" % (fn, sorted(lits), sorted(want)))
    return bad


def _instr_exec(code, rec, tag="<twin-instrumented>"):
    """exec transpiled part code with every operator, condition, index and ordering comparison routed
    through a checker that records where Python and FeatureScript semantics would part ways."""
    ns = {}
    for name in dir(K):
        if not name.startswith("_"):
            ns[name] = getattr(K, name)
    exec(fs2py.PRELUDE, ns)
    lines = code.splitlines()

    def where(ln):
        if 0 < ln <= len(lines):
            m = re.search(r"# (\S+:\d+)$", lines[ln - 1])
            if m:
                return m.group(1)
        return "line %d" % ln

    def viol(kind, ln, what):
        if len(rec["viol"]) < 200:
            rec["viol"].append("%s at %s: %s" % (kind, where(ln), what))

    def tw_bin(op, a, b, ln):
        ok = (_isnum(a) and _isnum(b)) \
            or (op in "+-" and isinstance(a, np.ndarray) and isinstance(b, np.ndarray)) \
            or (op in "*/" and isinstance(a, np.ndarray) and _isnum(b)) \
            or (op == "*" and _isnum(a) and isinstance(b, np.ndarray)) \
            or (op == "+" and isinstance(a, K.Id) and isinstance(b, str))
        if not ok:
            viol("operator %s on %s, %s" % (op, type(a).__name__, type(b).__name__), ln, "%r %s %r" % (a, op, b))
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        return a / b

    def tw_bool(v, ln):
        if not isinstance(v, (bool, np.bool_)):
            viol("non-boolean condition", ln, repr(v)[:60])
        return v

    def tw_idx(a, i, ln):
        if isinstance(a, dict):
            if i not in a:
                viol("missing map key", ln, repr(i))
        elif isinstance(a, (list, tuple, np.ndarray, str)):
            if not _isnum(i) or float(i) != int(i) or not (0 <= i < len(a)):
                viol("array index", ln, "%r of size %d" % (i, len(a)))
        return a[i]

    def tw_cmp(op, a, b, ln):
        if not (_isnum(a) and _isnum(b)):
            viol("ordering comparison %s on %s, %s" % (op, type(a).__name__, type(b).__name__), ln, "")
        return {"<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b}[op]

    tree = _Instr().visit(ast.parse(code))
    ast.fix_missing_locations(tree)
    ns.update({"_tw_bin": tw_bin, "_tw_bool": tw_bool, "_tw_idx": tw_idx, "_tw_cmp": tw_cmp})
    exec(compile(tree, tag, "exec"), ns)
    return ns


def _instrumented_build(f):
    rec = {"viol": [], "plane_dot": [], "frame_dot": [], "fillet": [], "style": [], "opids": [], "unions": [],
           "splits": [], "div_union": [], "div_split": [], "inside": [], "holes": [], "nm": [], "calls": 0,
           "loops": 0, "bad_loops": []}
    files = sorted(fp for fp in glob.glob(os.path.join(FSROOT, "src", "*.fs")) if re.match(r"^[2-4]\d_", os.path.basename(fp)))
    code = "\n".join(fs2py.transpile(_read(fp), os.path.relpath(fp, FSROOT)) for fp in files)
    ns = _instr_exec(code, rec)

    ctx_box = {}

    def note_query(ids):
        ctx = ctx_box["ctx"]
        ids = [K.Id(tuple(i)) for i in ids]
        twin_keys = set(ctx.keys_for(ids))
        for (consumed, survivor, opid) in rec["unions"]:
            hits = [i for i in ids if consumed[:len(i)] == i or opid[:len(i)] == i]
            if hits and survivor in ctx.bodies and survivor not in twin_keys:
                rec["div_union"].append("%s resolves the merged body in Onshape but nothing in the twin" % [str(h) for h in hits])
        for (opid, target) in rec["splits"]:
            hits = [i for i in ids if opid[:len(i)] == i and target[:len(i)] != i]
            if hits and target in ctx.bodies:
                rec["div_split"].append("%s also resolves the pieces of %s in Onshape" % ([str(h) for h in hits], target))

    def wrap(name):
        orig = getattr(K, name)
        params = list(inspect.signature(orig).parameters)

        def w(*args):
            rec["calls"] += 1
            a = dict(zip(params, args))
            ctx = a["context"]
            ctx_box["ctx"] = ctx
            for qp in QUERY_PARAMS:
                if qp in a and isinstance(a[qp], (list, tuple)) and a[qp] and isinstance(a[qp][0], K.Id):
                    note_query(a[qp])
            if "id" in a and name in FS_OPIDS:
                for s in FS_OPIDS[name]:
                    rec["opids"].append(tuple(a["id"]) if s is None else tuple(a["id"]) + (s,))
            before = None
            if name == "bSubtract":
                before = {k: len(ctx.bodies[k]["solids"]) for k in ctx.keys_for(a["targets"])}
            if name == "bUnion":
                ukeys = ctx.keys_for(a["bodies"])
            if name in ("filletAt", "softFilletAt", "styleFacesAt"):
                kind = TopAbs_FACE if name == "styleFacesAt" else TopAbs_EDGE
                subs = []
                for s in ctx.solids_for(a["bodies"]):
                    subs += _subshapes(s, kind)
                for p in a["pts"]:
                    v = _vtx(a["F"].pt(p))
                    ds = [_dist(v, e) for e in subs]
                    rec["style" if kind == TopAbs_FACE else "fillet"].append(
                        (str(a.get("id", "")) or str(a["bodies"][0]), min(ds), sum(1 for d in ds if d < 1e-7)))
            if name == "measureDistToPoint":
                wp = a["F"].pt(a["p"])
                if _inside(ctx.solids_for(a["bodies"]), wp):
                    rec["inside"].append("%s at %s" % ([str(i) for i in a["bodies"]], np.round(wp, 3).tolist()))
            if name in ("mkPrismProfile", "mkPrism", "mkPrismHoles", "mkTube", "mkCyl", "mkRevolve"):
                if name == "mkPrismHoles":
                    loops = [K._kPolyLoop(a["outer"])] + [K._kPolyLoop(hh) for hh in a["holes"]]
                elif name == "mkPrism":
                    loops = [K._kPolyLoop(a["pts"])]
                elif name == "mkTube":
                    loops = [[["C", a["c"], a["ro"]]], [["C", a["c"], a["ri"]]]]
                elif name == "mkCyl":
                    loops = [[["C", a["c"], a["r"]]]]
                elif name == "mkRevolve":
                    loops = [a["loop"]]
                else:
                    loops = a["loops"]
                if len(loops) > 1:
                    rec["holes"].append((str(a["id"]), _hole_clearance(loops)))
                for lp in loops:
                    okl, why = _simple_loop(lp)
                    rec["loops"] += 1
                    if not okl:
                        rec["bad_loops"].append("%s: %s" % (a["id"], why))
            res = orig(*args)
            if name == "bSubtract":
                for k, n0 in before.items():
                    if k in ctx.bodies and len(ctx.bodies[k]["solids"]) > n0:
                        rec["splits"].append((K.Id(tuple(a["id"])), k))
            if name == "bUnion" and len(ukeys) > 1:
                for k in ukeys[1:]:
                    rec["unions"].append((k, ukeys[0], K.Id(tuple(a["id"]))))
            return res
        return w

    for name in list(FS_OPIDS) + ["styleBody", "nameBody", "styleFacesAt", "massBody", "measureBox", "measureVolume",
                                  "measureDistToPoint", "measureDist", "countBodies"]:
        ns[name] = wrap(name)

    def fmt_ok(v):     # str(v) in Python == `"" ~ v` in FeatureScript only for strings and whole numbers
        return isinstance(v, str) or (_isnum(v) and float(v) == int(v))

    def wnm(s, i):
        if not (fmt_ok(s) and fmt_ok(i)):
            rec["nm"].append("nm(%r, %r)" % (s, i))
        return K.nm(s, i)

    def wmsg(parts):
        for p in parts:
            if not fmt_ok(p) and len(rec["nm"]) < 50:
                rec["nm"].append("msg(... %r ...)" % (p,))
        return K.msg(parts)
    ns["nm"], ns["msg"] = wnm, wmsg

    orig_frame, orig_plane = K.Frame, K._Plane

    class RecFrame(orig_frame):
        def __init__(self, o, x, z):
            super().__init__(o, x, z)
            rec["frame_dot"].append(abs(float(np.dot(self.x, self.z))))

    class RecPlane(orig_plane):
        def __init__(self, F, pl, offset):
            super().__init__(F, pl, offset)
            rec["plane_dot"].append(abs(float(np.dot(self.n, self.x))))

    K.Frame, K._Plane = RecFrame, RecPlane
    try:
        ctx = K.Registry()
        ctx_box["ctx"] = ctx
        fid = K.Id(("F",))
        ns["buildField"](ctx, fid, dict(f.opts))
        checks = ns["selfCheck"](ctx, fid, dict(f.opts))
    finally:
        K.Frame, K._Plane = orig_frame, orig_plane
    return rec, ctx, checks


def _loop_polyline(loop):
    """2-D polyline of a sketch loop; 3-point arcs sampled on their circle."""
    pts = []
    for sgm in loop:
        if sgm[0] == "L":
            pts.append(np.array(sgm[1], float))
        elif sgm[0] == "A":
            a, m, b = (np.array(x, float) for x in sgm[1:4])
            d = 2 * (a[0] * (m[1] - b[1]) + m[0] * (b[1] - a[1]) + b[0] * (a[1] - m[1]))
            if abs(d) < 1e-12:
                return None
            ux = ((a @ a) * (m[1] - b[1]) + (m @ m) * (b[1] - a[1]) + (b @ b) * (a[1] - m[1])) / d
            uy = ((a @ a) * (b[0] - m[0]) + (m @ m) * (a[0] - b[0]) + (b @ b) * (m[0] - a[0])) / d
            c = np.array([ux, uy])
            r = np.linalg.norm(a - c)
            ta, tm, tb = (math.atan2(*(x - c)[::-1]) for x in (a, m, b))
            sweep = (tb - ta) % (2 * math.pi)
            if (tm - ta) % (2 * math.pi) > sweep:
                sweep -= 2 * math.pi
            for k in range(12):
                t = ta + sweep * k / 12.0
                pts.append(c + r * np.array([math.cos(t), math.sin(t)]))
        else:
            return None
    return pts


def _simple_loop(loop):
    pts = _loop_polyline(loop)
    if pts is None or len(pts) < 3:
        return True, ""
    n = len(pts)
    area = 0.5 * sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    if abs(area) < 1e-9:
        return False, "zero area"

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def hit(p1, p2, q1, q2):
        d1, d2, d3, d4 = cr(q1, q2, p1), cr(q1, q2, p2), cr(p1, p2, q1), cr(p1, p2, q2)
        if ((d1 > 1e-12 and d2 < -1e-12) or (d1 < -1e-12 and d2 > 1e-12)) and \
                ((d3 > 1e-12 and d4 < -1e-12) or (d3 < -1e-12 and d4 > 1e-12)):
            return True

        def on(p, a, b):
            return abs(cr(a, b, p)) < 1e-12 and min(a[0], b[0]) - 1e-12 <= p[0] <= max(a[0], b[0]) + 1e-12 \
                and min(a[1], b[1]) - 1e-12 <= p[1] <= max(a[1], b[1]) + 1e-12
        return on(p1, q1, q2) or on(p2, q1, q2) or on(q1, p1, p2) or on(q2, p1, p2)
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                a, b, c = (pts[i], pts[i + 1], pts[(i + 2) % n]) if j == i + 1 else (pts[n - 1], pts[0], pts[1])
                if abs(cr(a, b, c)) < 1e-12 and (c - b) @ (b - a) < 0:
                    return False, "segment %d doubles back" % i
                continue
            if hit(pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n]):
                return False, "segments %d and %d intersect" % (i, j)
    return True, ""


def _hole_clearance(loops):
    """Smallest distance between the outer loop and any hole loop, and whether every hole lies inside the
    outer loop (qSketchRegion(.., filterInnerLoops = true) only drops a region that does not touch the
    outer boundary; the twin always makes a hole)."""
    P = K._Plane(K.frameMake([0, 0, 0], [1, 0, 0], [0, 0, 1]), [[0, 0, 0], [0, 0, 1], [1, 0, 0]], 0)
    outer = K._wire(P, loops[0])
    face = BRepBuilderAPI_MakeFace(outer, True).Face()
    worst, inside = float("inf"), True
    for hl in loops[1:]:
        w = K._wire(P, hl)
        worst = min(worst, _dist(outer, w))
        seg = hl[0]
        p0 = seg[1] if seg[0] != "C" else [seg[1][0] + seg[2], seg[1][1]]
        st = BRepClass_FaceClassifier(face, K._gp(P.p3(p0)), 1e-7).State()
        inside = inside and st == TopAbs_IN
    return worst, inside


def _guard_checks(out, f):
    rec, ctx, checks = _instrumented_build(f)
    ref = f.ns["selfCheck"](f.ctx, f.id, f.opts)
    same = len(ref) == len(checks) and all(a[0] == b[0] and abs(a[1] - b[1]) < 1e-12 for a, b in zip(ref, checks))
    out.append(("[guard] the instrumented rebuild reproduces the plain build (same self-check, same bodies)",
                same and len(ctx.bodies) == len(f.ctx.bodies),
                "%d kernel calls; %d self-check values identical: %s; bodies %d vs %d" % (
                    rec["calls"], len(checks), same, len(ctx.bodies), len(f.ctx.bodies))))
    mp, mf = max(rec["plane_dot"] or [0]), max(rec["frame_dot"] or [0])
    out.append(("[guard] every sketch plane and frame is perpendicular within std TOLERANCE.zeroAngle (1e-11)",
                mp < 1e-11 and mf < 1e-11, "%d planes, max |x.n| %.1e; %d frames, max |x.z| %.1e" % (
                    len(rec["plane_dot"]), mp, len(rec["frame_dot"]), mf)))
    fl = rec["fillet"]
    far = [x for x in fl if x[1] > 1e-9]
    multi = sorted({x[0] for x in fl if x[2] > 1})
    out.append(("[guard] every filletAt / softFilletAt point lies exactly on an edge (any qContainsPoint tolerance agrees)",
                not far and bool(fl), "%d points, worst offset %.1e in (twin accepts 1e-5); points on >1 edge "
                                      "(vertex hits, both edges filleted in either kernel): %s" % (
                                          len(fl), max([x[1] for x in fl] or [0]), multi or "none")))
    st = rec["style"]
    bad = [x for x in st if x[1] > 1e-9 or x[2] != 1]
    out.append(("[guard] every styleFacesAt point lies on exactly one face (Onshape paints every face containing it)",
                not bad and bool(st), "%d points; off-face or multi-face: %s" % (len(st), bad or "none")))
    out.append(("[guard] no soft roundover was skipped, so the twin's all-or-nothing softFilletAt never diverged",
                not ctx.warnings, "warnings: %s" % (ctx.warnings or "none")))
    out.append(("[guard] no query after a bUnion depends on the twin dropping the merged creators' Ids",
                not rec["div_union"], "%d unions %s; divergent queries: %s" % (
                    len(rec["unions"]), [(str(c), str(s)) for c, s, _ in rec["unions"]], rec["div_union"][:5] or "none")))
    out.append(("[guard] no query Id is a prefix of a splitting subtraction's Id (Onshape would add the pieces)",
                not rec["div_split"], "%d splitting subtractions; divergent queries: %s" % (
                    len({str(o) for o, _ in rec["splits"]}), rec["div_split"][:5] or "none")))
    out.append(("[guard] no self-check distance is measured from a point inside a body (evDistance semantics for "
                "inside points are not documented)", not rec["inside"], "inside: %s" % (rec["inside"] or "none")))
    ids = rec["opids"]
    comp_re = re.compile(r"^\*?[a-zA-Z0-9_.+/\-]+$")      # std string.fs REGEX_ID_COMPONENT
    badc = sorted({c for i in ids for c in i if not comp_re.match(c) or c.startswith(".")})
    dups = sorted({str(K.Id(i)) for i in ids if ids.count(i) > 1}) if len(ids) < 20000 else []
    model = _opid_model_matches_kernel()
    out.append(("[guard] Onshape operation Ids are unique and every component is a legal Id component",
                not badc and not dups and not model, "%d operation Ids; illegal components %s; duplicates %s; "
                                                     "kernel op-id model mismatches %s" % (len(ids), badc or "none", dups[:5] or "none", model or "none")))
    hl = rec["holes"]
    badh = [h for h in hl if not (h[1][0] > 1e-6 and h[1][1])]
    out.append(("[guard] every hole loop lies strictly inside its outer loop (qSketchRegion filterInnerLoops = the "
                "twin's face-with-holes)", not badh, "%d multi-loop profiles, min clearance %.4f in; bad %s" % (
                    len(hl), min([h[1][0] for h in hl] or [0]), badh or "none")))
    out.append(("[guard] every sketch loop is a simple closed curve (Onshape would extrude each region of a "
                "self-crossing loop; the twin builds one face of undefined shape)", not rec["bad_loops"] and rec["loops"] > 0,
                "%d loops (arcs sampled); bad: %s" % (rec["loops"], rec["bad_loops"][:6] or "none")))
    out.append(("[guard] fs2py runtime semantics: no array/string arithmetic, non-boolean condition, bad index or "
                "mixed-type ordering in the real build", not rec["viol"], "%s" % (rec["viol"][:8] or "none")))
    out.append(("[guard] Ids and names format only strings and whole numbers (Python str() = FeatureScript ~ there; "
                "booleans, fractions and arrays would print differently)", not rec["nm"], "%s" % (rec["nm"][:8] or "none")))


# ======================================================================================
# [static] scope and dialect analysis of the real part code
# ======================================================================================
def _analyze(sources, std):
    """Scope/dialect analysis of part-code sources [(name, text)] under FeatureScript rules
    (verify/scope_lint.py, which build.py also runs)."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import scope_lint
    std_names = None
    if std:
        names, enums = _import_build().std_index(std)
        std_names = set(names) | set(enums)
    return scope_lint.analyze(sources, _read(KERNEL_FS), std_names, [n for n in dir(K) if not n.startswith("_")])


PLANTED = """function plA(c)
{
    var q = 1;
    var q = 2;
    if (c)
    {
        var a = 1;
    }
    return a;
}

function plB()
{
    const k = 1;
    k = 2;
    var n = 3;
    for (var i = 0; i < n; i += 1)
    {
        n = 2;
    }
    var arr = [1, 2];
    arr[0] = 5;
    if (1 < 2 < 3)
    {
        return LB;
    }
    for (var j in arr)
    {
        var n = j;
    }
    var size = 4;
    return size;
}
"""


def _static_checks(out, std):
    part_files = sorted(fp for fp in glob.glob(os.path.join(FSROOT, "src", "*.fs")) if re.match(r"^[2-4]\d_", os.path.basename(fp)))
    # self-test: every category must fire on the planted defects (all lint-clean, all run in the twin)
    pi, _, _, _ = _analyze([("planted.fs", PLANTED)], std)
    want = ["undeclared", "after_block", "dup", "const_assign", "shadow_local", "shadow_global", "loop_mut", "sub_store", "chain"]
    silent = [k for k in want if not pi[k]]
    lint = fs2py.lint(PLANTED, "planted.fs")
    out.append(("[static] self-test: the scope analyzer flags each planted FS-invalid / divergent construct that "
                "fs2py.lint passes", not silent, "fs2py.lint on the planted file reports only %s; analyzer categories silent: %s; "
                "flagged: %s" % (lint, silent or "none", {k: len(pi[k]) for k in want})))
    rec = {"viol": []}
    code = fs2py.transpile("function rtA(a, b)\n{\n    return a + b;\n}\n\nfunction rtB(n)\n{\n    if (n)\n    {\n"
                           "        return n[0 - 1];\n    }\n    return 0;\n}\n", "rt.fs")
    ns = _instr_exec(code, rec, "<rt>")
    ns["rtA"]([1, 2], [3, 4])
    ns["rtB"]([7, 8])
    kinds = [k for k in ("operator +", "non-boolean", "array index") if not any(v.startswith(k) for v in rec["viol"])]
    out.append(("[static] self-test: the runtime instrumentation flags list '+', a non-boolean condition and a "
                "negative index", not kinds, "recorded %s; missed %s" % (rec["viol"], kinds or "none")))
    issues, stats, top, std_names = _analyze([(os.path.relpath(fp, FSROOT), _read(fp)) for fp in part_files], std)
    out.append(("[static] every name the part code uses is declared in FeatureScript scope (local, part-code top "
                "level, kernel or std) - nothing resolves only in the Python twin", not issues["undeclared"],
                "%d part files, %d statements, %d local declarations, %d name uses, %d top-level names, %d std names%s; "
                "undeclared: %s" % (len(part_files), stats["stmts"], stats["decl"], stats["uses"], len(top), len(std_names),
                                    "" if std else " (fallback list: std not found)", issues["undeclared"][:8] or "none")))
    out.append(("[static] no variable is used after the block that declared it (FS block scope vs Python function scope)",
                not issues["after_block"], "%s" % (issues["after_block"][:8] or "none")))
    out.append(("[static] no const (local or top-level) is assigned", not issues["const_assign"], "%s" % (issues["const_assign"][:8] or "none")))
    out.append(("[static] no name is declared twice in one block", not issues["dup"], "%s" % (issues["dup"][:8] or "none")))
    out.append(("[static] no local re-declares a name of an enclosing block (std never does this; FS rejects it)",
                not issues["shadow_local"], "%s" % (issues["shadow_local"][:8] or "none")))
    out.append(("[static] no local takes the name of a global (FS resolves it block-wise, Python function-wide)",
                not issues["shadow_global"], "%s" % (issues["shadow_global"][:8] or "none")))
    out.append(("[static] no C-style for-loop body writes its loop variable, bound or step", not issues["loop_mut"],
                "%d C-style loops; %s" % (stats["loops"], issues["loop_mut"][:8] or "none")))
    out.append(("[static] no indexed assignment (FS arrays are values, Python lists alias)", not issues["sub_store"],
                "%s" % (issues["sub_store"][:8] or "none")))
    out.append(("[static] no chained comparison", not issues["chain"], "%s" % (issues["chain"][:8] or "none")))
    out.append(("[static] part-code top-level names are unique, do not redefine kernel functions and are not "
                "twin-only helpers, Python keywords or Python builtins", not issues["top_dup"] and not issues["twin_clash"],
                "duplicates %s; twin clashes %s" % (issues["top_dup"][:5] or "none", issues["twin_clash"][:5] or "none")))


# ======================================================================================
# [decal] tagDecal emulated with the kernel's own FeatureScript expressions
# ======================================================================================
def _decal_exprs():
    b = _squash(_fs_functions(_read(KERNEL_FS))["tagDecal"][1])
    need = ["const h = cells / 2;", "for (var i = 0; i <= cells; i += 1)", "for (var j = 0; j < cells; j += 1)",
            "P.origin + (P.x * c[0] + cross(P.normal, P.x) * c[1]) * inch",
            '"faceTargets" : qContainsPoint(qOwnedByBody(kQ(bodies), EntityType.FACE), P.origin)']
    miss = [x for x in need if x not in b]
    hl = re.search(r'skLineSegment\(sk, "h" ~ i ~ "_" ~ j, \{ "start" : k2\(\[(.+?)\]\), "end" : k2\(\[(.+?)\]\) \}\);', b)
    vl = re.search(r'skLineSegment\(sk, "v" ~ i ~ "_" ~ j, \{ "start" : k2\(\[(.+?)\]\), "end" : k2\(\[(.+?)\]\) \}\);', b)
    cc = re.search(r"const c = \[(.+?)\];", b)
    if miss or not (hl and vl and cc):
        return None, "kernel tagDecal text changed: missing %s" % (miss or "segment/cell expressions")

    def split2(e):
        depth = 0
        for k, ch in enumerate(e):
            depth += ch in "([" and 1 or 0
            depth -= ch in ")]" and 1 or 0
            if ch == "," and depth == 0:
                return e[:k].strip(), e[k + 1:].strip()
        raise ValueError(e)
    return {"h": [split2(hl.group(1)), split2(hl.group(2))], "v": [split2(vl.group(1)), split2(vl.group(2))],
            "c": split2(cc.group(1))}, ""


def _decal_checks(out, f):
    ex, why = _decal_exprs()
    if ex is None:
        out.append(("[decal] kernel tagDecal expressions parsed", False, why))
        return
    with open(LAYOUT_JSON) as fh:
        lay = {t["ID"]: t["pose"] for t in json.load(fh)["tags"]}
    n_tags, bad_target, bad_split, bad_hit, bad_pattern, bad_plane = 0, [], [], [], [], []
    for key, rec in f.ctx.bodies.items():
        dec = rec.get("decal")
        m = re.match(r"^AprilTag (\d+) - ", rec.get("name") or "")
        if dec is None or not m:
            continue
        tid = int(m.group(1))
        n_tags += 1
        O, N, X = (np.array(dec[k], float) for k in ("origin", "normal", "x"))
        V = np.cross(N, X)
        cells, s = dec["cells"], dec["s"]
        solid = rec["solids"][0]
        faces = _subshapes(solid, TopAbs_FACE)
        tgt = [fc for fc in faces if _dist(_vtx(O), fc) < 1e-7]
        if len(tgt) != 1:
            bad_target.append("%d: %d faces contain the plane origin" % (tid, len(tgt)))
            continue
        h = cells / 2.0
        edges = []
        for i in range(0, int(cells) + 1):
            for j in range(0, int(cells)):
                env = {"i": i, "j": j, "h": h, "s": s}
                for kind in ("h", "v"):
                    (a0, a1), (b0, b1) = ex[kind]
                    pa = O + X * eval(a0, {}, env) + V * eval(a1, {}, env)
                    pb = O + X * eval(b0, {}, env) + V * eval(b1, {}, env)
                    edges.append(BRepBuilderAPI_MakeEdge(K._gp(pa), K._gp(pb)).Edge())
        off = max(_dist(tgt[0], e) for e in edges[::7])
        if off > 1e-9:
            bad_plane.append("%d: grid %.1e off the face" % (tid, off))
        sp = BRepAlgoAPI_Splitter()
        sp.SetArguments(K._lst([solid]))
        sp.SetTools(K._lst(edges))
        sp.Build()
        if not sp.IsDone():
            bad_split.append("%d: split failed" % tid)
            continue
        cellsq, ring = [], []
        for fc in _subshapes(sp.Shape(), TopAbs_FACE):
            vs = _vertices(fc)
            loc = np.array([[(p - O) @ X, (p - O) @ V, (p - O) @ N] for p in vs])
            if np.max(np.abs(loc[:, 2])) > 1e-7:
                continue
            lo, hi = loc[:, :2].min(axis=0), loc[:, :2].max(axis=0)
            (cellsq if np.allclose(hi - lo, [s, s], atol=1e-7) else ring).append((lo, hi))
        if len(cellsq) != cells * cells or len(ring) != 1:
            bad_split.append("%d: %d cells + %d other faces in the tag plane" % (tid, len(cellsq), len(ring)))
            continue
        painted = set()
        for rc in dec["black"]:
            env = {"rc": list(rc), "h": h, "s": s}
            cu, cv = eval(ex["c"][0], {}, env), eval(ex["c"][1], {}, env)
            hits = [k for k, (lo, hi) in enumerate(cellsq) if lo[0] - 1e-9 <= cu <= hi[0] + 1e-9 and lo[1] - 1e-9 <= cv <= hi[1] + 1e-9]
            if len(hits) != 1:
                bad_hit.append("%d: cell %s selects %d faces" % (tid, rc, len(hits)))
            painted |= set(hits)
        # read the painted target back as a camera facing the tag sees it (JSON pose, not the part code):
        # facing normal n from the yaw, up = +Z, viewer's right = up x n; row 0 at the top, col 0 at the left
        pose = lay[tid]
        T = np.array([pose["translation"][a] for a in ("x", "y", "z")]) / 0.0254
        q = pose["rotation"]["quaternion"]
        yaw = 2 * math.atan2(q["Z"], q["W"])
        n_ = np.array([math.cos(yaw), math.sin(yaw), 0.0])
        up = np.array([0.0, 0.0, 1.0])
        right = np.cross(up, n_)
        seen = set()
        for r in range(int(cells)):
            for c in range(int(cells)):
                p = T + right * ((c + 0.5 - h) * s) + up * ((h - r - 0.5) * s)
                u, v = (p - O) @ X, (p - O) @ V
                hit = [k for k, (lo, hi) in enumerate(cellsq) if lo[0] < u < hi[0] and lo[1] < v < hi[1]]
                if hit and hit[0] in painted:
                    seen.add((r, c))
        want = R.reference_black_cells(tid)
        if seen != want:
            bad_pattern.append("%d: %d black seen, %d expected, %d differ" % (tid, len(seen), len(want), len(seen ^ want)))
    out.append(("[decal] 26 tag panels carry a decal whose plane origin lies on exactly one panel face (faceTargets)",
                n_tags == 26 and not bad_target, "%d panels; %s" % (n_tags, bad_target or "all single-face")))
    out.append(("[decal] the kernel's sketch grid lies in that face and splits it into 100 cells + the white ring",
                not bad_split and not bad_plane, "%s %s" % (bad_split[:4] or "", bad_plane[:4] or "all 26 split into 101 faces")))
    out.append(("[decal] each black cell's query point (kernel expression) selects exactly one cell face",
                not bad_hit, "%s" % (bad_hit[:4] or "all selections unique")))
    out.append(("[decal] painted cells, read facing the tag (JSON pose, row 0 top / col 0 left), = WPILib 36h11 artwork",
                not bad_pattern and n_tags == 26, "%s" % (bad_pattern[:4] or "all 26 patterns match tag36h11 (AprilRobotics codes)")))


# ======================================================================================
# [style] styleFacesAt on the copies
# ======================================================================================
def _style_checks(out, f):
    n, bad = 0, []
    for rec in f.ctx.bodies.values():
        for (p, rgb, a) in rec.get("faces") or []:
            n += 1
            v = _vtx(p)
            k = 0
            for s in rec["solids"]:
                k += sum(1 for fc in _subshapes(s, TopAbs_FACE) if _dist(v, fc) < 1e-7)
            if k != 1:
                bad.append("%s: %d faces at %s" % (rec["name"], k, np.round(p, 3).tolist()))
    out.append(("[style] every face-style point carried to the copies selects exactly one face of its copy",
                n > 0 and not bad, "%d styled points on %d bodies; %s" % (
                    n, sum(1 for r in f.ctx.bodies.values() if r.get("faces")), bad[:4] or "all single-face")))


# ======================================================================================
def run(f):
    out = []
    std = _std_dir()
    for fn in (lambda: _src_checks(out, std), lambda: _conv_checks(out), lambda: _twin_checks(out, std),
               lambda: _guard_checks(out, f), lambda: _static_checks(out, std), lambda: _decal_checks(out, f),
               lambda: _style_checks(out, f)):
        try:
            fn()
        except Exception as e:  # noqa: BLE001 - one broken section must not hide the others
            import traceback
            out.append(("[error] check section raised", False, "%s: %s | %s" % (
                type(e).__name__, e, traceback.format_exc().splitlines()[-3:])))
    return out
