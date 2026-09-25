# -*- coding: utf-8 -*-
"""
Independent checks of the CRAG body: tower, spire, SUMMIT BEACON lantern, tier rings, kick-guard,
High Peg root bosses and the flush AprilTag pockets -- both CRAGS.

Every expected value below is taken from the package documents, never from src/:
  FIELD-CAD-PACKAGE.md  §0 (frame, angle rule, (ref) tolerance), §1.1 (placement, face orientation),
                        §2.1 (envelope), §2.5 (High Peg roots / bosses), §2.6, §2.7, §7 (tags), §8 (LEDs)
  MATERIALS-AND-COLORS.md §1.2 palette, §2 rows (tower, spire, lantern, tier ring, kick-guard, boss),
                        §3 appearance rules
  02-manual/sections/02-arena.md §3.3 (face planes), §3.7 tag table (tag centres)

The CRAG-local frame used here is built from the documents (not taken from the generator):
origin at the CRAG centre on the carpet, +x = SHELF FACE outward normal (Blue: world -X, Red: +X,
§1.1), +z up, +y = z x x.  So the SHELF FACE is x = +24, the PEG FACE x = -24, SOCKET FACES y = +/-24.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import kernel_occ as K  # noqa: E402
from OCP.BRepAdaptor import BRepAdaptor_Surface  # noqa: E402
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform  # noqa: E402
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox  # noqa: E402
from OCP.GeomAbs import GeomAbs_Plane  # noqa: E402
from OCP.TopAbs import TopAbs_FACE  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopoDS import TopoDS  # noqa: E402
from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf  # noqa: E402

# ------------------------------------------------------------------------------------------
# Document values
# ------------------------------------------------------------------------------------------
FIELD_CTR = (324.0, 162.0)                         # §0: 180-degree rotation centre
CRAG_CTR = {"BLUE": (324.0, 240.0), "RED": (324.0, 84.0)}   # §1.1 / ledger #3
SHELF_NX = {"BLUE": -1.0, "RED": +1.0}             # §1.1: shelf-face normal Blue -X, Red +X
OPP = {"BLUE": "RED", "RED": "BLUE"}

H = 48.0 / 2                  # §2.1 tower 48 x 48 footprint
TOWER_TOP = 60.0              # §2.1 tower body to 60 (top plate)
SH = 20.0 / 2                 # §2.1 spire 20 x 20 prism
SPIRE_BASE = 60.0
SPIRE_TOP = 90.0              # §2.1 overall height 90
LANTERN_LO = SPIRE_TOP - 12.0  # §2.1 top 12 in translucent: Z 78 -> 90
LUMINOUS_C = 84.0             # §2.1 / §8 luminous centre

RING_W = 1.0                  # §8 band 1.0 wide
RING_D = 0.25                 # §8 0.25 deep, let flush into the face
RINGS = {                     # name -> (z0, z1, half-size of the body it wraps, peg-station lateral)
    "30": (30.0 - RING_W / 2, 30.0 + RING_W / 2, H, 14.0),       # §8 centred on 30, wraps the tower
    "54": (54.0 - RING_W / 2, 54.0 + RING_W / 2, H, 14.0),       # §8 centred on 54, wraps the tower
    "78": (77.0, 78.0, SH, 7.0),                                   # §8 hung Z 77.0-78.0 on the spire
}
PEG_OD = 1.5                  # §2.5
PEG_LAT = 14.0                # §2.5 low/mid peg roots +/-14
HPEG_LAT = 7.0                # §2.5 high peg roots +/-7 on the spire peg face
HPEG_Z = 78.0
ROOT_HALF_H = PEG_OD / 2 / math.sin(math.radians(45))   # §2.5 ellipse 2.12 tall -> Z 76.94-79.06
BOSS_W = 3.0                  # §2.5 "the 3.0 in of face width at each peg"
BOSS_T = 0.25                 # MATERIALS: boss 0.25 in
BOSS_Z = (74.0, 80.0)         # MATERIALS: spanning Z 74-80
KICK_LEG = 2.0                # MATERIALS: 2 x 2 x 0.125 angle
KICK_T = 0.125
TOWER_PANEL = 0.75            # MATERIALS: tower faces 0.75 panel
SPIRE_PANEL = 0.75            # MATERIALS: spire faces 0.75 panel
LANTERN_T = 0.25              # MATERIALS: lantern 0.25
TAG_PANEL = 9.0               # §7 panel 9.0 sq x 0.25
TAG_T = 0.25
TAG_TARGET = 8.125
TAG_Z = 17.5
TAG_LAT = 14.0

# Blue CRAG tags (manual §3.7 table / FIELD-CAD-PACKAGE §7): id -> (x, y, outward normal)
BLUE_TAGS = {6: (300, 226, (-1, 0)), 7: (300, 254, (-1, 0)), 8: (310, 264, (0, 1)), 9: (338, 264, (0, 1)),
             10: (310, 216, (0, -1)), 11: (338, 216, (0, -1)), 12: (348, 226, (1, 0)), 13: (348, 254, (1, 0))}


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


COL = {  # MATERIALS-AND-COLORS §1
    "crag-body": _hex("#E9E2D4"), "crag-spire": _hex("#DDD3C0"), "crag-accent": _hex("#4A3B22"),
    "beacon-lantern": _hex("#FFF3D0"), "alliance-blue": _hex("#1D63C8"), "alliance-red": _hex("#CC3333"),
}
ALLIANCE_RGB = {"BLUE": COL["alliance-blue"], "RED": COL["alliance-red"]}
LANTERN_ALPHA = 0.35
# plausible densities (kg/m^3) for the named materials
DENS = {"plywood": (400, 800), "polycarbonate": (1150, 1250), "acrylic": (1150, 1250),
        "aluminum": (2600, 2800), "steel": (7750, 8050)}
MATWORD = {"plywood": "plywood", "polycarbonate": "polycarbonate", "acrylic": "acrylic",
           "aluminum": "alumin", "steel": "steel"}

TOL = 1e-3


# ------------------------------------------------------------------------------------------
# geometry helpers (OCC, independent of the part code)
# ------------------------------------------------------------------------------------------
def doc_frame(f, A):
    cx, cy = CRAG_CTR[A]
    return f.frame((cx, cy, 0.0), (SHELF_NX[A], 0.0, 0.0), (0.0, 0.0, 1.0))


def box_world(F, p0, p1):
    lo = [min(a, b) for a, b in zip(p0, p1)]
    hi = [max(a, b) for a, b in zip(p0, p1)]
    b = BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape()
    return BRepBuilderAPI_Transform(b, F.trsf(), True).Shape()


def common_box(f, rs, F, p0, p1):
    tool = box_world(F, p0, p1)
    out = []
    for s in f.solids(rs):
        out += K._solids(K.BRepAlgoAPI_Common(s, tool).Shape())
    return out


def bbox_solids(sol, F):
    sh = K._compound(sol)
    if F is not None:
        sh = BRepBuilderAPI_Transform(sh, F.trsf().Inverted(), True).Shape()
    b = K.Bnd_Box()
    K.BRepBndLib.AddOptimal_s(sh, b, False, False)
    return K._box6(b)


def outline(f, rs, F, z, dz=0.02):
    sol = common_box(f, rs, F, (-300, -300, z - dz / 2), (300, 300, z + dz / 2))
    return bbox_solids(sol, F) if sol else None


def section_area(f, rs, F, z, dz=0.02):
    return K._volume(common_box(f, rs, F, (-300, -300, z - dz / 2), (300, 300, z + dz / 2))) / dz


def transformed(sol, trsf):
    return [BRepBuilderAPI_Transform(s, trsf, True).Shape() for s in sol]


def common_vol_solids(a, b):
    tot = 0.0
    for x in a:
        for y in b:
            tot += K._volume(K._solids(K.BRepAlgoAPI_Common(x, y).Shape()))
    return tot


def rot180_trsf():
    t = gp_Trsf()
    t.SetRotation(gp_Ax1(gp_Pnt(FIELD_CTR[0], FIELD_CTR[1], 0), gp_Dir(0, 0, 1)), math.pi)
    return t


def mirror_y_trsf(cy):
    t = gp_Trsf()
    t.SetMirror(gp_Ax2(gp_Pnt(0, cy, 0), gp_Dir(0, 1, 0)))
    return t


def face_normals(sol):
    """(n_planar, n_other, [unit normals of planar faces])"""
    npl, nother, ns = 0, 0, []
    for s in sol:
        exp = TopExp_Explorer(s, TopAbs_FACE)
        while exp.More():
            ad = BRepAdaptor_Surface(TopoDS.Face(exp.Current()))
            if ad.GetType() == GeomAbs_Plane:
                d = ad.Plane().Axis().Direction()
                ns.append(np.array([d.X(), d.Y(), d.Z()]))
                npl += 1
            else:
                nother += 1
            exp.Next()
    return npl, nother, ns


def intervals_gaps(ivs, lo, hi, eps=1e-6):
    """Merge [a, b] intervals and return the gaps inside [lo, hi]."""
    ivs = sorted(ivs)
    merged = []
    for a, b in ivs:
        if merged and a <= merged[-1][1] + eps:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    gaps = []
    cur = lo
    for a, b in merged:
        if a > cur + eps:
            gaps.append((cur, a))
        cur = max(cur, b)
    if cur < hi - eps:
        gaps.append((cur, hi))
    return gaps


def bb_overlap(a, b, pad=0.0):
    return all(a[i] - pad <= b[i + 3] and b[i] - pad <= a[i + 3] for i in range(3))


def fmt(v):
    if v is None:
        return "None"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(fmt(x) for x in v) + "]"
    if isinstance(v, float):
        return "%.4f" % v
    return str(v)


# ------------------------------------------------------------------------------------------
def run(f):
    out = []

    def ck(label, ok, detail):
        out.append((label, bool(ok), detail))

    def near(label, got, want, tol=TOL):
        ok = got is not None and abs(got - want) <= tol
        ck(label, ok, "measured %s, expected %s +/- %g" % (fmt(got), fmt(want), tol))

    def box_is(label, got, want, tol=TOL):
        axes = ("xmin", "ymin", "zmin", "xmax", "ymax", "zmax")
        if got is None:
            ck(label, False, "no geometry")
            return
        bad = [(axes[i], got[i], want[i]) for i in range(6) if want[i] is not None and abs(got[i] - want[i]) > tol]
        ck(label, not bad, "measured %s, expected %s%s" % (fmt(got), fmt(list(want)),
                                                           ("; off: " + fmt(bad)) if bad else ""))

    def find(name):
        try:
            return f.find(name)
        except KeyError:
            return []

    def material_ok(label, rs, key):
        m = f.material(rs)
        lo, hi = DENS[key]
        ok = MATWORD[key] in m["name"].lower() and lo <= m["density"] <= hi
        ck(label, ok, "material %r density %.0f kg/m^3, expected %s (%d-%d)" % (m["name"], m["density"], key, lo, hi))

    def colour_ok(label, rs, rgb, alpha=1.0, atol=1e-6):
        got, a = f.color(rs)
        ok = tuple(got) == tuple(rgb) and abs(a - alpha) <= atol
        ck(label, ok, "rgb %s alpha %.3f, expected %s alpha %.3f" % (tuple(got), a, tuple(rgb), alpha))

    all_recs = f.records()
    _bbc = {}

    def rbox(r):
        k = r["id"]
        if k not in _bbc:
            _bbc[k] = f.bbox([r])
        return _bbc[k]

    for A in ("BLUE", "RED"):
        F = doc_frame(f, A)
        cx, cy = CRAG_CTR[A]
        pre = A + " CRAG "

        tower = find(pre + "tower")
        spire = find(pre + "spire")
        lantern = find(pre + "SUMMIT BEACON")
        rings = {k: find(pre + "tier ring " + k) for k in RINGS}
        kick = find(pre + "kick-guard")
        boss = find(pre + "High Peg root boss")
        hpeg = find(pre + "High Peg")
        lpeg = find(pre + "Low Peg") + find(pre + "Mid Peg")

        # ---------------- existence / body structure -----------------------------------
        for nm_, rs, nb in (("tower", tower, 1), ("spire", spire, 1), ("SUMMIT BEACON lantern", lantern, 1),
                            ("kick-guard", kick, 1), ("High Peg root boss", boss, 2), ("High Peg", hpeg, 2)):
            ck(pre + nm_ + ": body count", len(rs) == nb, "found %d bodies named %r, expected %d" % (len(rs), pre + nm_, nb))
        for k, rs in rings.items():
            ck(pre + "tier ring %s exists" % k, len(rs) >= 1, "found %d bodies" % len(rs))
        if not (tower and spire and lantern and kick and boss and all(rings.values())):
            continue
        ck(pre + "lantern is a separate body from the spire (§2.7)",
           not any(r["id"] == s["id"] for r in lantern for s in spire), "lantern ids %s, spire ids %s" %
           ([r["id"][1:] for r in lantern], [r["id"][1:] for r in spire]))

        # ---------------- placement and envelope (world) --------------------------------
        box_is(pre + "tower world bbox = (%g..%g, %g..%g, 0..60) (§1.1, §2.1)" % (cx - H, cx + H, cy - H, cy + H),
               f.bbox(tower), (cx - H, cy - H, 0, cx + H, cy + H, TOWER_TOP))
        box_is(pre + "tower + kick-guard footprint at carpet 48 x 48 (§2.1)",
               outline(f, tower + kick, F, 0.05), (-H, -H, None, H, H, None))
        box_is(pre + "spire + lantern world bbox 20 x 20, Z 60..90, centred on the tower axis (§2.1)",
               f.bbox(spire + lantern), (cx - SH, cy - SH, SPIRE_BASE, cx + SH, cy + SH, SPIRE_TOP))
        box_is(pre + "spire (opaque) local bbox Z 60..78", f.bbox(spire, F), (-SH, -SH, SPIRE_BASE, SH, SH, LANTERN_LO))
        box_is(pre + "lantern local bbox Z 78..90 (top 12 in)", f.bbox(lantern, F), (-SH, -SH, LANTERN_LO, SH, SH, SPIRE_TOP))
        lb = f.bbox(lantern, F)
        near(pre + "SUMMIT BEACON luminous centre Z (§2.1/§8)", (lb[2] + lb[5]) / 2, LUMINOUS_C)
        # the spire stands on the top plate: contact, no gap, no overlap
        near(pre + "spire rests on the tower top plate (distance)", f.dist(spire, tower), 0.0, 1e-6)
        near(pre + "spire / tower common volume", f.common_volume(spire, tower), 0.0, 1e-6)
        near(pre + "lantern / spire common volume", f.common_volume(lantern, spire), 0.0, 1e-6)
        near(pre + "lantern sits on the spire (distance)", f.dist(lantern, spire), 0.0, 1e-6)
        crag_all = [r for r in all_recs if (r["name"] or "").startswith(pre)]
        near(pre + "overall height: highest CRAG point Z = 90 (§2.1)", f.bbox(crag_all)[5], SPIRE_TOP)

        # straight prisms at every height: the outline of the structure (with its flush inserts)
        tower_set = tower + kick + rings["30"] + rings["54"]
        spire_set = spire + lantern + rings["78"] + boss
        for z in (0.05, 1.0, 2.5, 10.0, 17.5, 25.0, 30.0, 42.0, 54.0, 59.9):
            box_is(pre + "tower outline at Z %.2f is 48 x 48 (straight prism)" % z, outline(f, tower_set, F, z),
                   (-H, -H, None, H, H, None))
        for z in (60.1, 63.0, 66.0, 69.0, 72.0, 75.0, 77.5, 78.1, 79.5, 81.0, 84.0, 87.0, 89.9):
            box_is(pre + "spire outline at Z %.2f is 20 x 20 (straight prism, not tapered)" % z,
                   outline(f, spire_set, F, z), (-SH, -SH, None, SH, SH, None))

        # rock is texture, never geometry: planar faces only, every normal on a local axis
        for nm_, rs in (("tower", tower), ("spire", spire), ("lantern", lantern), ("kick-guard", kick),
                        ("High Peg root boss", boss), ("tier rings", rings["30"] + rings["54"] + rings["78"])):
            npl, nother, ns = face_normals(f.solids(rs))
            axes = [F.x, F.y, F.z]
            off = [n for n in ns if max(abs(float(np.dot(n, a))) for a in axes) < 1 - 1e-9]
            ck(pre + nm_ + ": planar faces only, all square to the CRAG axes (no taper/facets, §0 angle rule, M&C §3.1)",
               nother == 0 and not off, "%d planar faces, %d non-planar, %d off-axis normals" % (npl, nother, len(off)))

        # hollow panel construction (MATERIALS: tower 0.75 panel, spire 0.75, lantern 0.25)
        near(pre + "tower wall section at Z 40 = 48^2 - 46.5^2 (0.75 panel)", section_area(f, tower, F, 40.0),
             48.0 ** 2 - (48.0 - 2 * TOWER_PANEL) ** 2, 0.05)
        near(pre + "tower top plate present at Z 59.6 (full 48 x 48 section)", section_area(f, tower, F, 59.6),
             48.0 ** 2, 0.05)
        near(pre + "spire wall section at Z 70 = 20^2 - 18.5^2 (0.75 panel)", section_area(f, spire, F, 70.0),
             20.0 ** 2 - (20.0 - 2 * SPIRE_PANEL) ** 2, 0.05)
        near(pre + "lantern wall section at Z 84 = 20^2 - 19.5^2 (0.25 polycarbonate)", section_area(f, lantern, F, 84.0),
             20.0 ** 2 - (20.0 - 2 * LANTERN_T) ** 2, 0.05)

        # ---------------- SUMMIT BEACON lantern presents on all four spire faces --------------
        for lab, p, q in (("SHELF", (SH, 0, LUMINOUS_C), (SH + 0.01, 0, LUMINOUS_C)),
                          ("PEG", (-SH, 0, LUMINOUS_C), (-SH - 0.01, 0, LUMINOUS_C)),
                          ("+y SOCKET", (0, SH, LUMINOUS_C), (0, SH + 0.01, LUMINOUS_C)),
                          ("-y SOCKET", (0, -SH, LUMINOUS_C), (0, -SH - 0.01, LUMINOUS_C))):
            d0 = f.dist_point(lantern, p, F)
            d1 = f.dist_point(lantern, q, F)
            ck(pre + "lantern presents on the %s spire face at Z 84, flush" % lab, d0 < 1e-6 and abs(d1 - 0.01) < 1e-6,
               "distance on the face plane %.6f (want 0), 0.01 outside %.6f (want 0.01)" % (d0, d1))
        # nothing but the High Pegs stands in front of the lantern faces (Z 78..90, 6 in out)
        blockers = []
        band = [box_world(F, (SH, -SH - 6, LANTERN_LO), (SH + 6, SH + 6, SPIRE_TOP)),
                box_world(F, (-SH - 6, -SH - 6, LANTERN_LO), (-SH, SH + 6, SPIRE_TOP)),
                box_world(F, (-SH, SH, LANTERN_LO), (SH, SH + 6, SPIRE_TOP)),
                box_world(F, (-SH, -SH - 6, LANTERN_LO), (SH, -SH, SPIRE_TOP))]
        skip_ids = {r["id"] for r in hpeg + lantern}
        for r in all_recs:
            if r["id"] in skip_ids:
                continue
            bb = rbox(r)
            if bb[5] <= LANTERN_LO + 1e-6 or not bb_overlap(bb, (cx - 20, cy - 20, LANTERN_LO, cx + 20, cy + 20, SPIRE_TOP)):
                continue
            v = common_vol_solids(r["solids"], band)
            if v > 1e-6:
                blockers.append((r["name"], round(v, 4)))
        ck(pre + "nothing but the High Pegs stands in front of the lantern (Z 78-90, 6 in out)", not blockers,
           "blocking bodies: %s" % blockers)

        # ---------------- appearance --------------------------------------------------------
        colour_ok(pre + "tower colour crag-body #E9E2D4 (M&C §2)", tower, COL["crag-body"])
        material_ok(pre + "tower material painted plywood", tower, "plywood")
        colour_ok(pre + "spire colour crag-spire #DDD3C0", spire, COL["crag-spire"])
        material_ok(pre + "spire material painted plywood", spire, "plywood")
        colour_ok(pre + "lantern unlit colour beacon-lantern #FFF3D0 at 35%", lantern, COL["beacon-lantern"], LANTERN_ALPHA, 1e-3)
        material_ok(pre + "lantern material translucent polycarbonate", lantern, "polycarbonate")
        colour_ok(pre + "kick-guard colour crag-accent #4A3B22", kick, COL["crag-accent"])
        material_ok(pre + "kick-guard material aluminium", kick, "aluminum")
        for r in boss:
            colour_ok(pre + "boss %s colour crag-accent" % (r["id"][1:],), [r], COL["crag-accent"])
            material_ok(pre + "boss %s material steel" % (r["id"][1:],), [r], "steel")
        for k, rs in rings.items():
            rgb, a = f.color(rs)
            lum = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
            ck(pre + "tier ring %s unlit is dark (M&C §2 'dark when unlit')" % k,
               lum < 0.25 and tuple(rgb) not in (COL["alliance-blue"], COL["alliance-red"]) and a == 1,
               "rgb %s alpha %.2f relative luminance %.3f" % (tuple(rgb), a, lum))
            ck(pre + "tier ring %s: all bodies share one appearance" % k,
               len({(tuple(r["rgb"]), r["alpha"]) for r in rs}) == 1, str({(tuple(r["rgb"]), r["alpha"]) for r in rs}))
            material_ok(pre + "tier ring %s material frosted acrylic" % k, rs, "acrylic")

        # ---------------- tier rings -----------------------------------------------------------
        for k, (z0, z1, hh, gc) in RINGS.items():
            rs = rings[k]
            host = tower if hh == H else spire
            box_is(pre + "tier ring %s bbox (wraps %g x %g, band Z %.1f-%.1f, flush)" % (k, 2 * hh, 2 * hh, z0, z1),
                   f.bbox(rs, F), (-hh, -hh, z0, hh, hh, z1))
            near(pre + "tier ring %s band width 1.0" % k, f.bbox(rs, F)[5] - f.bbox(rs, F)[2], RING_W)
            near(pre + "tier ring %s / host common volume (let in, not overlapping)" % k, f.common_volume(rs, host), 0.0, 1e-6)
            zc = (z0 + z1) / 2
            # depth and flushness on the middle of each face
            faces = (("SHELF", (1, 0)), ("PEG", (-1, 0)), ("+y SOCKET", (0, 1)), ("-y SOCKET", (0, -1)))
            for lab, (nx, ny) in faces:
                def P(d, lat=0.0, nx=nx, ny=ny, hh=hh, zc=zc):
                    # point at depth d behind face (nx, ny), lateral position lat along the face
                    return (((hh - d) * nx) if nx else lat, ((hh - d) * ny) if ny else lat, zc)
                on = f.dist_point(rs, P(0.0), F)
                proud = f.dist_point(rs, P(-0.01), F)
                in24 = f.inside(rs, P(RING_D - 0.01), F)
                in26 = f.inside(rs, P(RING_D + 0.01), F)
                host26 = f.inside(host, P(RING_D + 0.01), F)
                ck(pre + "tier ring %s on the %s face: on the face plane, 0.25 deep, flush" % (k, lab),
                   on < 1e-6 and abs(proud - 0.01) < 1e-6 and in24 and not in26 and host26,
                   "dist on plane %.6f (0), 0.01 out %.6f (0.01), in ring at depth 0.24 %s (True), at 0.26 %s (False), "
                   "host behind at 0.26 %s (True)" % (on, proud, in24, in26, host26))
            # interruptions: section each face strip and find the gaps along it
            for lab, (nx, ny) in faces:
                if nx:
                    p0 = ((hh - RING_D) * nx, -hh - 1, z0 - 0.5)
                    p1 = (hh * nx, hh + 1, z1 + 0.5)
                    ax = 1
                else:
                    p0 = (-hh - 1, (hh - RING_D) * ny, z0 - 0.5)
                    p1 = (hh + 1, hh * ny, z1 + 0.5)
                    ax = 0
                sol = common_box(f, rs, F, p0, p1)
                ivs = []
                for s in sol:
                    b = bbox_solids([s], F)
                    ivs.append((b[ax], b[ax + 3]))
                gaps = intervals_gaps(ivs, -hh, hh)
                if lab == "PEG":
                    ctrs = sorted(round((a + b) / 2, 4) for a, b in gaps)
                    widths = [b - a for a, b in gaps]
                    ok = (len(gaps) == 2 and abs(ctrs[0] + gc) < TOL and abs(ctrs[1] - gc) < TOL
                          and all(w >= PEG_OD - 1e-6 for w in widths))
                    if k == "78":
                        ok = ok and all(abs(w - BOSS_W) < TOL for w in widths)
                    ck(pre + "tier ring %s interrupted only at the two peg stations y = +/-%g%s" %
                       (k, gc, " over the 3.0-in boss width (§2.5/§8)" if k == "78" else " (ring clear of the peg roots)"),
                       ok, "gaps %s" % fmt([(a, b) for a, b in gaps]))
                else:
                    ck(pre + "tier ring %s continuous across the %s face" % (k, lab), not gaps, "gaps %s" % fmt(gaps))
        near(pre + "tier ring 78 top edge on the lantern joint (ring zmax = lantern zmin)",
             f.bbox(rings["78"], F)[5] - f.bbox(lantern, F)[2], 0.0)
        near(pre + "tier ring 78 / lantern common volume (stays on the opaque spire)", f.common_volume(rings["78"], lantern), 0.0, 1e-6)
        near(pre + "tier ring 78 / High Peg root boss common volume", f.common_volume(rings["78"], boss), 0.0, 1e-6)
        if lpeg:
            near(pre + "tier rings 30/54 / Low+Mid Peg common volume", f.common_volume(rings["30"] + rings["54"], lpeg), 0.0, 1e-6)
        if hpeg:
            near(pre + "tier ring 78 / High Peg common volume", f.common_volume(rings["78"], hpeg), 0.0, 1e-6)
        for sgn in (-1, 1):
            p = (-SH + 0.1, sgn * HPEG_LAT, 77.5)
            ck(pre + "ring-78 gap at y %+g is filled by the boss" % (sgn * HPEG_LAT),
               f.inside(boss, p, F) and not f.inside(rings["78"], p, F),
               "inside boss %s, inside ring %s" % (f.inside(boss, p, F), f.inside(rings["78"], p, F)))

        # ---------------- kick-guard -----------------------------------------------------------
        box_is(pre + "kick-guard bbox: perimeter, flush to carpet and faces, 2 in tall",
               f.bbox(kick, F), (-H, -H, 0.0, H, H, KICK_LEG))
        near(pre + "kick-guard vertical-leg section at Z 1.0 = 48^2 - 47.75^2 (0.125 leg)",
             section_area(f, kick, F, 1.0), 48.0 ** 2 - (48.0 - 2 * KICK_T) ** 2, 0.02)
        near(pre + "kick-guard horizontal-leg section at Z 0.06 = 48^2 - 44^2 (2.0 leg)",
             section_area(f, kick, F, 0.06, 0.02), 48.0 ** 2 - (48.0 - 2 * KICK_LEG) ** 2, 0.1)
        for lab, (nx, ny) in (("SHELF", (1, 0)), ("PEG", (-1, 0)), ("+y SOCKET", (0, 1)), ("-y SOCKET", (0, -1))):
            def Q(d, z, nx=nx, ny=ny):
                return (((H - d) * nx) if nx else 5.0, ((H - d) * ny) if ny else 5.0, z)
            on = f.dist_point(kick, Q(0.0, 1.0), F)
            proud = f.dist_point(kick, Q(-0.01, 1.0), F)
            ck(pre + "kick-guard flush in the %s face (on the face plane, nothing proud)" % lab,
               on < 1e-6 and abs(proud - 0.01) < 1e-6, "dist on plane %.6f (0), 0.01 out %.6f (0.01)" % (on, proud))
        near(pre + "kick-guard / tower common volume", f.common_volume(kick, tower), 0.0, 1e-6)
        near(pre + "kick-guard rests on the carpet (zmin 0)", f.bbox(kick)[2], 0.0)

        # ---------------- High Peg root bosses --------------------------------------------------
        for sgn in (-1, 1):
            b1 = [r for r in boss if f.bbox([r], F)[1] * sgn > 0]
            if len(b1) != 1:
                ck(pre + "High Peg boss at y %+g" % (sgn * HPEG_LAT), False, "found %d" % len(b1))
                continue
            y0, y1 = sorted((sgn * (HPEG_LAT - BOSS_W / 2), sgn * (HPEG_LAT + BOSS_W / 2)))
            box_is(pre + "High Peg boss y %+g: 0.25 steel let flush into the spire peg face, 3.0 wide, Z 74-80" % (sgn * HPEG_LAT),
                   f.bbox(b1, F), (-SH, y0, BOSS_Z[0], -SH + BOSS_T, y1, BOSS_Z[1]))
            # the peg root ellipse lies on the boss
            miss = []
            for i in range(24):
                t = 2 * math.pi * i / 24
                p = (-SH, sgn * HPEG_LAT + 0.999 * PEG_OD / 2 * math.cos(t), HPEG_Z + 0.999 * ROOT_HALF_H * math.sin(t))
                d = f.dist_point(b1, p, F)
                if d > 1e-6:
                    miss.append((round(p[1], 3), round(p[2], 3), round(d, 4)))
            ck(pre + "High Peg y %+g root ellipse (1.5 x 2.12, Z 76.94-79.06) lies entirely on its boss" % (sgn * HPEG_LAT),
               not miss, "root points off the boss: %s" % miss)
            # lantern lower edge opaque-backed over the 3.0-in face width at the peg
            pin = (-SH + 0.1, sgn * HPEG_LAT, 79.5)
            pedge_in = (-SH + 0.1, sgn * (HPEG_LAT + BOSS_W / 2 - 0.05), 78.5)
            pedge_out = (-SH + 0.1, sgn * (HPEG_LAT + BOSS_W / 2 + 0.05), 78.5)
            pabove = (-SH + 0.1, sgn * HPEG_LAT, 80.5)
            r1 = (f.inside(b1, pin, F), f.inside(lantern, pin, F), f.inside(b1, pedge_in, F),
                  f.inside(lantern, pedge_out, F), f.inside(lantern, pabove, F))
            ck(pre + "lantern lower edge backed opaque (steel) over 3.0 in at the y %+g peg; lantern resumes above Z 80" % (sgn * HPEG_LAT),
               r1 == (True, False, True, True, True),
               "boss@Z79.5 %s, lantern@Z79.5 %s, boss@edge-0.05 %s, lantern@edge+0.05 %s, lantern@Z80.5 %s "
               "(want True, False, True, True, True)" % r1)
        near(pre + "boss / spire common volume", f.common_volume(boss, spire), 0.0, 1e-6)
        near(pre + "boss / lantern common volume", f.common_volume(boss, lantern), 0.0, 1e-6)
        if hpeg:
            dl = f.dist(hpeg, lantern)
            ck(pre + "High Pegs take no load on the translucent lantern (peg-lantern clearance > 0)", dl > 1e-3,
               "min distance High Peg to lantern %.4f in" % dl)
            ds = f.dist(hpeg, spire)
            ck(pre + "High Pegs are carried by the bosses, not the plywood spire (peg-spire clearance > 0)", ds > 1e-3,
               "min distance High Peg to spire %.4f in" % ds)
            near(pre + "High Pegs touch their bosses", f.dist(hpeg, boss), 0.0, 1e-6)
            for r in hpeg:
                sec = common_box(f, [r], F, (-SH - 0.002, -SH, 70), (-SH, SH, 88))
                bb = bbox_solids(sec, F) if sec else None
                ok = bb is not None and abs(bb[2] - (HPEG_Z - ROOT_HALF_H)) < 0.01 and abs(bb[5] - (HPEG_Z + ROOT_HALF_H)) < 0.01
                ck(pre + "High Peg %s root on the spire peg face (x = -10, 14 in inboard of the tower face) spans Z 76.94-79.06"
                   % (r["id"][1:],), ok, "root section bbox %s" % fmt(bb))

        # ---------------- AprilTag pockets ------------------------------------------------------
        tags = {}
        for tid, (x, y, n) in BLUE_TAGS.items():
            if A == "BLUE":
                tags[tid] = ((x, y), n)
            else:
                tags[tid + 13] = ((2 * FIELD_CTR[0] - x, 2 * FIELD_CTR[1] - y), (-n[0], -n[1]))
        for tid, ((x, y), n) in sorted(tags.items()):
            n3 = np.array([n[0], n[1], 0.0])
            c = np.array([x, y, TAG_Z])
            t3 = np.array([-n[1], n[0], 0.0])        # along the face
            z3 = np.array([0.0, 0.0, 1.0])
            probes_void = [c - 0.1 * n3, c - 0.1 * n3 + t3 * (TAG_PANEL / 2 - 0.05), c - 0.1 * n3 - t3 * (TAG_PANEL / 2 - 0.05),
                           c - 0.1 * n3 + z3 * (TAG_PANEL / 2 - 0.05), c - 0.1 * n3 - z3 * (TAG_PANEL / 2 - 0.05),
                           c - (TAG_T - 0.01) * n3]
            probes_solid = [c - (TAG_T + 0.01) * n3, c - 0.1 * n3 + t3 * (TAG_PANEL / 2 + 0.05), c - 0.1 * n3 - t3 * (TAG_PANEL / 2 + 0.05),
                            c - 0.1 * n3 + z3 * (TAG_PANEL / 2 + 0.05), c - 0.1 * n3 - z3 * (TAG_PANEL / 2 + 0.05)]
            v_bad = [tuple(np.round(p, 3)) for p in probes_void if f.inside(tower, p)]
            s_bad = [tuple(np.round(p, 3)) for p in probes_solid if not f.inside(tower, p)]
            ck(pre + "tag %d pocket 9.0 x 9.0 x 0.25 centred (%g, %g, 17.5) in the face" % (tid, x, y), not v_bad and not s_bad,
               "tower material inside pocket at %s; missing tower material around pocket at %s" % (v_bad, s_bad))
            trs = [r for r in all_recs if (r["name"] or "").startswith("AprilTag %d " % tid)]
            if len(trs) != 1:
                ck(pre + "tag %d panel present" % tid, False, "found %d" % len(trs))
                continue
            cv = f.common_volume(trs, tower)
            flush_on = f.dist_point(trs, c)
            flush_out = f.dist_point(trs, c + 0.01 * n3)
            seated = f.dist(trs, tower)
            ck(pre + "tag %d panel seated flush in its pocket (no overlap, face on the face plane, back on the floor)" % tid,
               cv < 1e-6 and flush_on < 1e-6 and abs(flush_out - 0.01) < 1e-6 and seated < 1e-6,
               "common %.6f (0), dist at tag centre %.6f (0), 0.01 out %.6f (0.01), panel-tower %.6f (0)"
               % (cv, flush_on, flush_out, seated))
            # the full 8.125 target must be unobstructed from the field side (§7, M&C §3.3): no field
            # structure in the horizontal prism of the target, 30 in out from the face
            TF = f.frame(tuple(c), tuple(n3), (0, 0, 1))
            prism = box_world(TF, (0.005, -TAG_TARGET / 2, -TAG_TARGET / 2), (30.0, TAG_TARGET / 2, TAG_TARGET / 2))
            pb = bbox_solids([prism], None)
            hits = []
            for r in all_recs:
                nmr = r["name"] or ""
                if (nmr.startswith("AprilTag %d " % tid) or " tape" in nmr or nmr.endswith("tape") or nmr == "Field carpet"
                        or " - " in nmr and nmr.split(" - ")[0] in ("CACHE CRATE", "O2 CELL", "ROPE COIL")
                        or "staging mark" in nmr or "CENTER CACHE mark" in nmr):
                    continue
                if not bb_overlap(rbox(r), pb, 1e-6):
                    continue
                v = common_vol_solids(r["solids"], [prism])
                if v > 1e-7:
                    hits.append((nmr, round(v, 5)))
            ck(pre + "tag %d 8.125-in target unobstructed by field structure (30 in out)" % tid, not hits,
               "obstructing: %s" % hits)

        # ---------------- face orientation (§1.1) ----------------------------------------------
        sgnx = SHELF_NX[A]
        sh1 = find(pre + "Shelf 1")
        if sh1:
            b = f.bbox(sh1)
            want = cx + sgnx * H
            ok = (b[0] >= want - 1e-6) if sgnx > 0 else (b[3] <= want + 1e-6)
            ck(pre + "SHELF FACE faces its own alliance wall (shelf outboard of X = %g toward %s)" %
               (want, "+X" if sgnx > 0 else "-X"), ok, "Shelf 1 world bbox %s" % fmt(b))
        pegs_all = find(pre + "Low Peg") + find(pre + "Mid Peg")
        if pegs_all:
            b = f.bbox(pegs_all)
            want = cx - sgnx * H
            ok = (b[3] <= want + 1e-6) if sgnx > 0 else (b[0] >= want - 1e-6)
            ck(pre + "PEG FACE faces the opponent wall (pegs outboard of X = %g)" % want, ok, "Low+Mid Peg bbox %s" % fmt(b))
        if hpeg:
            b = f.bbox(hpeg)
            want = cx - sgnx * SH
            got = b[3] if sgnx > 0 else b[0]
            near(pre + "High Peg roots on the spire peg face plane X = %g" % want, got, want)
        socks = find(pre + "Low Socket") + find(pre + "Mid Socket")
        if socks:
            ys = sorted(((f.bbox([r])[1] + f.bbox([r])[4]) / 2) for r in socks)
            ok = len(ys) == 4 and ys[0] < cy - H and ys[1] < cy - H and ys[2] > cy + H and ys[3] > cy + H
            ck(pre + "SOCKET FACES are the +/-Y faces (two sockets beyond Y = %g and two beyond %g)" % (cy + H, cy - H),
               ok, "socket centre Ys %s" % fmt(ys))
        GF = f.crag_frame(A)
        ck(pre + "generator CRAG frame agrees with §1.1 (origin at centre, +x = SHELF FACE normal)",
           np.allclose(GF.o, F.o) and np.allclose(GF.x, F.x) and np.allclose(GF.z, F.z),
           "generator origin %s x %s; document origin %s x %s" % (fmt(list(GF.o)), fmt(list(GF.x)), fmt(list(F.o)), fmt(list(F.x))))

        # ---------------- mirror symmetry about the CRAG's own X-Z plane (§2.7) ----------------------
        mt = mirror_y_trsf(cy)
        for nm_, rs in (("tower", tower), ("spire", spire), ("lantern", lantern), ("kick-guard", kick), ("bosses", boss),
                        ("tier rings", rings["30"] + rings["54"] + rings["78"])):
            sol = f.solids(rs)
            v = K._volume(sol)
            cv = common_vol_solids(transformed(sol, mt), sol)
            near(pre + nm_ + " mirror-symmetric about the CRAG X-Z plane (common/volume)", cv / v, 1.0, 1e-6)

        # ---------------- interference with every neighbour --------------------------------------
        mine = tower + spire + lantern + kick + boss + rings["30"] + rings["54"] + rings["78"]
        mine_ids = {r["id"] for r in mine}
        clashes = []
        for m in mine:
            mb = rbox(m)
            for r in all_recs:
                if r["id"] in mine_ids and r["id"] <= m["id"]:
                    continue
                if r["id"] == m["id"]:
                    continue
                if not bb_overlap(mb, rbox(r), 1e-6):
                    continue
                v = common_vol_solids(m["solids"], r["solids"])
                if v > 1e-6:
                    clashes.append((m["name"], r["name"], round(v, 5)))
        ck(pre + "no interference between the CRAG body parts and any other body", not clashes, "clashes: %s" % clashes)

    # ---------------- Red = Blue rotated 180 degrees about (324, 162) ----------------------------
    rt = rot180_trsf()
    for part in ("tower", "spire", "SUMMIT BEACON", "kick-guard", "High Peg root boss", "tier ring 30", "tier ring 54",
                 "tier ring 78"):
        try:
            b = f.solids(f.find("BLUE CRAG " + part))
            r = f.solids(f.find("RED CRAG " + part))
        except KeyError as e:
            ck("RED CRAG %s = BLUE rotated 180" % part, False, str(e))
            continue
        vb, vr = K._volume(b), K._volume(r)
        cv = common_vol_solids(transformed(b, rt), r)
        ck("RED CRAG %s is BLUE rotated 180 deg about (324, 162)" % part,
           abs(cv / vb - 1) < 1e-6 and abs(vr / vb - 1) < 1e-6, "vol blue %.4f red %.4f common %.4f" % (vb, vr, cv))

    # ---------------- lit state (M&C §3.6: both states modelled) ----------------------------------
    fl = type(f)(**dict(f.opts, lit=True))
    for A in ("BLUE", "RED"):
        pre = A + " CRAG "
        lit_l = [r for r in fl.records() if (r["name"] or "").startswith(pre + "SUMMIT BEACON")]
        if len(lit_l) != 1:
            ck(pre + "lit SUMMIT BEACON present", False, "found %d" % len(lit_l))
        else:
            rgb, a = fl.color(lit_l)
            ck(pre + "lit SUMMIT BEACON in alliance colour and still translucent", tuple(rgb) == ALLIANCE_RGB[A] and a < 1,
               "rgb %s alpha %.2f, expected %s alpha < 1" % (tuple(rgb), a, ALLIANCE_RGB[A]))
            box_is(pre + "lit SUMMIT BEACON geometry unchanged (Z 78-90)", fl.bbox(lit_l, doc_frame(fl, A)),
                   (-SH, -SH, LANTERN_LO, SH, SH, SPIRE_TOP))
        for k in RINGS:
            try:
                rs = fl.find(pre + "tier ring " + k)
            except KeyError:
                ck(pre + "lit tier ring %s present" % k, False, "missing")
                continue
            cols = {tuple(r["rgb"]) for r in rs}
            ck(pre + "lit tier ring %s in alliance colour %s" % (k, ALLIANCE_RGB[A]), cols == {ALLIANCE_RGB[A]}, "rgb %s" % cols)

    # ---------------- cosmetics layer (§2.7, §8 CAD notes, M&C §3.1) -------------------------------
    keys = sorted(f.opts)
    sup = [k for k in keys if any(w in k.lower() for w in ("cosmetic", "ring", "led_ring", "tier"))]
    ck("tier rings sit on a suppressible 'cosmetics' layer (a build option removes them)", bool(sup),
       "build options: %s" % keys)
    return out
