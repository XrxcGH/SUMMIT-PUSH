# -*- coding: utf-8 -*-
"""
CRAG PEG FACE: Low, Mid and High Pegs — independent checks of the off-line build.

Sources (expected values come ONLY from these documents, never from src/):
  FIELD-CAD-PACKAGE §0 (frame, 180-degree symmetry, angle rule), §1.1 (crag centres, face
  orientation), §2.1 (48 x 48 tower, 20 x 20 spire, lantern Z 78-90), §2.5 (the whole peg
  table, the ROPE COIL rest poses, High Peg root mounting, robot approach), §2.6 / §8 (tier
  rings 30 / 54 centred, 78 hung Z 77-78 and interrupted at the High Peg root bosses), §7
  (CRAG tag panel Z 13-22), §9.3 (ROPE COIL torus 10.0 OD / 2.5 tube / 5.0 ID),
  §10 ledger row 8.
  MATERIALS-AND-COLORS §1.2 / §2 (Peg: steel round bar, `rung` #9AA0A6; High Peg root
  boss: steel plate let into the spire, `crag-accent` #4A3B22, 0.25 in, spanning Z 74-80).
  Game Manual §3.3 (PEG FACE planes: Blue X = 348, Red X = 300) and §3.3.3.
  VISION-GUIDE §1.3 (coil on a Low Peg clear of the tag panel) and the PEG FACE table
  (Low / Mid Pegs directly above the tags; High Pegs 14.0 inboard).

Virtual ROPE COILS are built here as OpenCascade tori from the §9.3 numbers and posed on the
built pegs in the §2.5 rest poses; a copy of the generator's own staged ROPE COIL is posed
the same way so the piece and the peg are checked together.

Construction reading (naming only; the package does not name parts): each peg is its own part,
"<A> CRAG <Low|Mid|High> Peg (guardrail side)" or "(center side)", the guardrail side being the
one farther from the field's long centreline Y = 162.  Pegs are matched to their expected roots by
geometry and the name's side is then checked against the match.
"""
import math

import numpy as np
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

import kernel_occ as K

# ------------------------------------------------------------------------------------------
# Document values
# ------------------------------------------------------------------------------------------
FIELD_L, FIELD_W = 648.0, 324.0                     # §0 carpet; Red = Blue rotated about (324, 162)
CRAG_C = {"BLUE": (324.0, 240.0)}                   # §1.1 (Red derived by the 180-degree rotation)
TOWER_HALF = 48.0 / 2                               # §2.1 48 x 48 footprint
SPIRE_HALF = 20.0 / 2                               # §2.1 20 x 20 spire prism
SPIRE_INBOARD = 14.0                                # §2.5 "roots sit on the spire's peg face, 14.0 in inboard"
PEG_OD = 1.5                                        # §2.5 CRITICAL
PEG_R = PEG_OD / 2
PEG_ANG = 45.0                                      # §2.5 CRITICAL, 45 deg upward in the face-normal plane
PEG_EXP = 10.0                                      # §2.5 CRITICAL, along the axis
TIP_R = 0.75                                        # §2.5 rounded tip, 0.75 spherical radius
HORIZ_PROJ = 10.0 * math.cos(math.radians(45))      # §2.5 "projects 7.07 in horizontally"
ELLIPSE_H = PEG_OD / math.sin(math.radians(45))     # §2.5 root ellipse 1.5 wide x 2.12 tall
LEVELS = [                                          # §2.5 table / §10 row 8
    ("Low Peg", 30.0, 14.0, "tower"),
    ("Mid Peg", 54.0, 14.0, "tower"),
    ("High Peg", 78.0, 7.0, "spire"),
]
BOSS_Z = (74.0, 80.0)                               # MATERIALS §2 "spanning Z 74-80"
BOSS_T = 0.25                                       # MATERIALS §2 "0.25 in"
BOSS_W = 3.0                                        # §2.5 "back the lantern's lower edge with opaque material over the 3.0 in of face width at each peg"
LANTERN_Z0, LANTERN_Z1 = 78.0, 90.0                 # §2.1
RING78 = (77.0, 78.0)                               # §2.6 / §8
RING_W = 1.0                                        # §2.6 band width
RGB_RUNG = (0x9A, 0xA0, 0xA6)                       # MATERIALS `rung`
RGB_ACCENT = (0x4A, 0x3B, 0x22)                     # MATERIALS `crag-accent`
STEEL_DENSITY = (7750.0, 8050.0)                    # "Steel round bar" / "Steel plate": plain carbon steel, kg/m^3
COIL_OD, COIL_TUBE, COIL_ID = 10.0, 2.5, 5.0        # §9.3 CRITICAL
COIL_R = COIL_OD / 2 - COIL_TUBE / 2                # torus centre radius 3.75 (§9.3 "centre at r = 3.75")
COIL_r = COIL_TUBE / 2
COIL_INNER_OUT = 1.25                               # §2.5 "inner face about 1.25 in outboard of the crag face"
COIL_CENTRE_UP = 1.0                                # §2.5 "center roughly 1 in above the peg root"
TAG_PANEL_TOP = 17.5 + 9.0 / 2                      # §7 CRAG panel spans Z 13.00-22.00
FRAME_PERIM = 3.0                                   # §2.5 FRAME PERIMETER 3.0 in off the tower face
REACH_LIMIT = 18.0                                  # §2.5 / R105
TAG_IDS = {"BLUE": (12, 13), "RED": (25, 26)}       # §7

TOL = 0.005        # in, CRITICAL linear
ATOL = 0.05        # deg, CRITICAL angular
S45 = math.sqrt(0.5)
EZ = np.array([0.0, 0.0, 1.0])
EY = np.array([0.0, 1.0, 0.0])


def rot180(p):
    return np.array([FIELD_L - p[0], FIELD_W - p[1], p[2]], float)


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


# ------------------------------------------------------------------------------------------
# Expected geometry, per crag / peg (Blue from the documents, Red by the 180-degree rotation)
# ------------------------------------------------------------------------------------------
def expected_pegs(side):
    cx, cy = CRAG_C["BLUE"]
    n_blue = np.array([1.0, 0.0, 0.0])            # Blue PEG FACE faces the Red wall (+X), plane X = 348
    out = []
    for level, z, lat, face in LEVELS:
        xf = cx + TOWER_HALF - (SPIRE_INBOARD if face == "spire" else 0.0)
        for sgn in (-1, 1):
            root = np.array([xf, cy + sgn * lat, z])
            n = n_blue.copy()
            if side == "RED":
                root = rot180(root)
                n = -n
            out.append({"level": level, "root": root, "n": n, "lat": lat, "face": face, "sgn": sgn,
                        "u": n * math.cos(math.radians(PEG_ANG)) + EZ * math.sin(math.radians(PEG_ANG))})
    return out


def tower_face_x(side):
    x = CRAG_C["BLUE"][0] + TOWER_HALF
    return x if side == "BLUE" else FIELD_L - x


# ------------------------------------------------------------------------------------------
# Virtual solids
# ------------------------------------------------------------------------------------------
def _perp(a):
    a = unit(a)
    t = EZ if abs(a[2]) < 0.9 else EY
    return unit(np.cross(a, t))


def torus(c, a, R=COIL_R, r=COIL_r, name="virtual ROPE COIL"):
    ax = gp_Ax2(gp_Pnt(*map(float, c)), gp_Dir(*map(float, unit(a))), gp_Dir(*map(float, _perp(a))))
    return {"solids": [BRepPrimAPI_MakeTorus(ax, float(R), float(r)).Shape()], "name": name, "id": ("virtual",)}


def disk(c, a, r, t=0.02):
    """Thin disk (the coil's hole) centred on c, normal a."""
    base = np.asarray(c, float) - unit(a) * t / 2
    ax = gp_Ax2(gp_Pnt(*map(float, base)), gp_Dir(*map(float, unit(a))), gp_Dir(*map(float, _perp(a))))
    return {"solids": [BRepPrimAPI_MakeCylinder(ax, float(r), float(t)).Shape()], "name": "virtual hole disk", "id": ("virtual",)}


def moved_copy(rec, src_o, src_z, dst_o, dst_z, name):
    """Copy a record's solids from frame (src_o, axis src_z) to (dst_o, axis dst_z)."""
    Fs = K.Frame(src_o, _perp(src_z), src_z)
    Fd = K.Frame(dst_o, _perp(dst_z), dst_z)
    tr = Fd.trsf().Multiplied(Fs.trsf().Inverted())
    sol = [BRepBuilderAPI_Transform(s, tr, True).Shape() for s in rec["solids"]]
    return {"solids": sol, "name": name, "id": ("virtual",)}


# ------------------------------------------------------------------------------------------
# Helpers over the Field
# ------------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, f):
        self.f = f
        self.recs = f.records()
        self.bb = {}
        for r in self.recs:
            self.bb[r["id"]] = f.bbox([r])

    def overlapping(self, bb, pad=0.05, exclude=()):
        out = []
        for r in self.recs:
            if r["id"] in exclude:
                continue
            b = self.bb[r["id"]]
            if all(b[i] <= bb[i + 3] + pad and bb[i] <= b[i + 3] + pad for i in range(3)):
                out.append(r)
        return out

    def clashes(self, rec, exclude=(), vtol=1e-6):
        """Bodies whose common volume with rec exceeds vtol: list of (name, volume)."""
        bb = self.f.bbox([rec])
        hits = []
        for r in self.overlapping(bb, exclude=exclude):
            v = self.f.common_volume([rec], [r])
            if v > vtol:
                hits.append((r["name"], v))
        return hits


SIDE_SUFFIX = (" (guardrail side)", " (center side)")


def find_sided(f, base):
    """Both parts named base + " (guardrail side)" / " (center side)"; [] if there are none."""
    out = []
    for suf in SIDE_SUFFIX:
        try:
            out += f.find(base + suf)
        except KeyError:
            pass
    return out


def side_suffix(root):
    """Name suffix the documents' geometry implies: guardrail side = farther from Y 162."""
    return SIDE_SUFFIX[0] if abs(root[1] - FIELD_W / 2) > 162.0 - 84.0 else SIDE_SUFFIX[1]


def fmt(v, n=4):
    return "(" + ", ".join(("%." + str(n) + "f") % x for x in v) + ")"


def fit_axis(f, rs, root, u):
    """Fit the peg axis from point distances at two stations (radius probe 2.5 in)."""
    P = f.frame(root, EY, u)                # x = world Y (lateral), z = nominal axis, y = u x Y
    R = 2.5
    cents, radii = [], []
    for s in (2.0, 8.5):
        dpx = f.dist_point(rs, (R, 0, s), P)
        dmx = f.dist_point(rs, (-R, 0, s), P)
        dpy = f.dist_point(rs, (0, R, s), P)
        dmy = f.dist_point(rs, (0, -R, s), P)
        cx, cy = (dmx - dpx) / 2, (dmy - dpy) / 2
        radii.append(R - (dpx + dmx + dpy + dmy) / 4)
        cents.append(P.pt((cx, cy, s)))
    a = unit(cents[1] - cents[0])
    return cents[0], a, radii


# ------------------------------------------------------------------------------------------
def run(f):
    out = []
    C = Ctx(f)

    def add(label, ok, detail):
        out.append((label, bool(ok), detail))

    # the generator's ROPE COIL (used below in the rest poses) must itself be the §9.3 torus
    src = f.find("re:^ROPE COIL")[0]
    sb = C.bb[src["id"]]
    ext = sorted([sb[3] - sb[0], sb[4] - sb[1], sb[5] - sb[2]])
    sc0 = (np.array(sb[:3]) + np.array(sb[3:])) / 2
    hole = f.dist_point([src], sc0)
    add("generator ROPE COIL is a 10.0 OD x 2.5 tube torus with a 5.0 ID hole (for the rest-pose tests)",
        abs(ext[0] - COIL_TUBE) < TOL and abs(ext[1] - COIL_OD) < TOL and abs(ext[2] - COIL_OD) < TOL
        and abs(2 * hole - COIL_ID) < TOL, "envelope %s, hole ID %.4f" % (fmt(ext, 3), 2 * hole))

    coils_by_side = {}
    for side in ("BLUE", "RED"):
        pegs = expected_pegs(side)
        tfx = tower_face_x(side)

        # ---- counts, names ------------------------------------------------------------
        found = {}
        for level, _, _, _ in LEVELS:
            rs = find_sided(f, "%s CRAG %s" % (side, level))
            found[level] = rs
            add("%s %s: 2 bodies named '%s CRAG %s (guardrail side)' / '(center side)'" % (side, level, side, level),
                len(rs) == 2, "found %d" % len(rs))
        try:
            bosses = f.find("%s CRAG High Peg root boss" % side)
        except KeyError:
            bosses = []
        add("%s High Peg root boss: 2 bodies" % side, len(bosses) == 2, "found %d" % len(bosses))

        lantern = f.find("re:^%s CRAG SUMMIT BEACON" % side)
        spire = f.find("%s CRAG spire" % side)
        tower = f.find("%s CRAG tower" % side)
        rings = {k: f.find("%s CRAG tier ring %s" % (side, k)) for k in ("30", "54", "78")}
        all_rings = rings["30"] + rings["54"] + rings["78"]

        # ---- match each expected peg to a body -----------------------------------------
        used = set()
        for pg in pegs:
            cand = [r for r in found[pg["level"]] if r["id"] not in used]
            if not cand:
                pg["rec"] = None
                continue
            best = min(cand, key=lambda r: np.linalg.norm(
                np.array(C.bb[r["id"]][:3]) + np.array(C.bb[r["id"]][3:]) - 2 * (pg["root"] + pg["u"] * 4.6)))
            used.add(best["id"])
            pg["rec"] = best
            want_name = "%s CRAG %s%s" % (side, pg["level"], side_suffix(pg["root"]))
            add("%s %s at Y = %g is named '%s'" % (side, pg["level"], pg["root"][1], want_name),
                best["name"] == want_name, "matched body %r" % best["name"])

        side_coils = {}
        for pg in pegs:
            rec = pg["rec"]
            root, n, u = pg["root"], pg["n"], pg["u"]
            w = unit(np.cross(u, EY))           # radial direction in the vertical plane
            tag = "%s %s Y=%g" % (side, pg["level"], root[1])
            if rec is None:
                add(tag + ": body present", False, "no body")
                continue
            rs = [rec]

            add(tag + ": one solid", len(rec["solids"]) == 1, "solids %d" % len(rec["solids"]))

            # ---- bounding box in the peg frame (x lateral, z along the documented axis) ----
            P = f.frame(root, EY, u)
            bb = f.bbox(rs, P)
            want = [-PEG_R, -PEG_R, -PEG_R, PEG_R, PEG_R, PEG_EXP]
            err = max(abs(a - b) for a, b in zip(bb, want))
            add(tag + ": bbox in peg frame = OD 1.5 x exposed 10.0 (root trimmed on the 45-deg face)",
                err < TOL, "got %s want %s" % (fmt(bb), fmt(want, 2)))

            # ---- fitted axis: OD, elevation, plane, root ----------------------------------
            c1, a, radii = fit_axis(f, rs, root, u)
            dia = [2 * r for r in radii]
            add(tag + ": OD 1.5 (probed at two stations)", all(abs(d - PEG_OD) < TOL for d in dia),
                "diameters %s" % fmt(dia))
            elev = math.degrees(math.asin(max(-1, min(1, a[2]))))
            add(tag + ": axis 45 deg upward", abs(elev - PEG_ANG) < ATOL, "elevation %.4f deg" % elev)
            latang = math.degrees(math.asin(max(-1, min(1, a @ EY))))
            add(tag + ": axis in the vertical plane of the face normal, pointing outward",
                abs(latang) < ATOL and a @ n > 0.5, "lateral %.4f deg, a.n %.4f" % (latang, a @ n))
            t = (root[0] - c1[0]) / a[0]
            rootm = c1 + a * t                 # fitted axis meets the mounting-face plane
            add(tag + ": root height (axis meets face) Z = %g" % root[2], abs(rootm[2] - root[2]) < TOL,
                "measured Z %.4f" % rootm[2])
            add(tag + ": root lateral Y = %g (%s %.1f from the %s centreline)" % (root[1], "+/-", pg["lat"], pg["face"]),
                abs(rootm[1] - root[1]) < TOL, "measured Y %.4f" % rootm[1])

            # ---- root on the face: nothing inboard of the face plane ------------------------
            wb = C.bb[rec["id"]]
            inner = wb[0] if n[0] > 0 else wb[3]
            add(tag + ": root on the face plane X = %g (no part inboard)" % root[0], abs(inner - root[0]) < 1e-3,
                "inboard extreme X %.4f" % inner)
            # root ellipse on the face: 1.5 wide x 2.12 tall
            ins, outs = [], []
            for k in range(8):
                ph = 2 * math.pi * k / 8
                e = EY * PEG_R * math.cos(ph) + EZ * (ELLIPSE_H / 2) * math.sin(ph)
                ins.append(f.dist_point(rs, root + n * 0.002 + 0.97 * e))
                outs.append(f.dist_point(rs, root + n * 0.002 + 1.04 * e))
            add(tag + ": root footprint on the face is the 1.5 x 2.12 ellipse",
                max(ins) < 1e-6 and min(outs) > 1e-4 and abs(wb[2] - (root[2] - ELLIPSE_H / 2)) < TOL,
                "inside max %.4f, outside min %.4f, zmin %.4f (want %.4f)" % (max(ins), min(outs), wb[2], root[2] - ELLIPSE_H / 2))

            # ---- tip: exposed 10.0 along the axis, R0.75 spherical ---------------------------
            apex = root + u * PEG_EXP
            d0 = f.dist_point(rs, apex)
            d1 = f.dist_point(rs, apex + u * 0.05)
            add(tag + ": exposed length 10.0 along the axis (apex on the axis)", d0 < 1e-4 and abs(d1 - 0.05) < 1e-3,
                "apex dist %.5f, 0.05 beyond %.5f" % (d0, d1))
            sc = root + u * (PEG_EXP - TIP_R)
            ds = []
            for al in (0, 30, 60, 88):
                for be in (0, 90, 180, 270):
                    dv = (u * math.cos(math.radians(al)) + math.sin(math.radians(al)) *
                          (EY * math.cos(math.radians(be)) + w * math.sin(math.radians(be))))
                    ds.append(f.dist_point(rs, sc + 2.0 * dv) - (2.0 - TIP_R))
            add(tag + ": rounded tip is a 0.75-radius sphere", max(abs(x) for x in ds) < 2e-3,
                "max radial error %.5f" % max(abs(x) for x in ds))
            hp = (apex - root) @ n
            rise = apex[2] - root[2]
            add(tag + ": tip projects 7.07 horizontally and rises 7.07", abs(hp - HORIZ_PROJ) < TOL and abs(rise - HORIZ_PROJ) < TOL,
                "horizontal %.4f, rise %.4f (apex on the fitted axis at %s)" % (hp, rise, fmt(rootm + a * PEG_EXP, 3)))

            # ---- volume / appearance / material ------------------------------------------
            vwant = math.pi * PEG_R ** 2 * (PEG_EXP - TIP_R) + 2.0 / 3.0 * math.pi * TIP_R ** 3
            vol = f.volume(rs)
            add(tag + ": volume of a 1.5 x 10.0 R0.75-tip bar", abs(vol - vwant) < 0.02, "%.4f in^3 want %.4f" % (vol, vwant))
            rgb, alpha = f.color(rs)
            add(tag + ": colour `rung` #9AA0A6, opaque", tuple(rgb) == RGB_RUNG and alpha == 1, "rgb %s alpha %s" % (rgb, alpha))
            m = f.material(rs)
            add(tag + ": material steel", "steel" in m["name"].lower() and STEEL_DENSITY[0] <= m["density"] <= STEEL_DENSITY[1],
                "%s %.0f kg/m^3" % (m["name"], m["density"]))

            # ---- interference / support ------------------------------------------------------
            hits = C.clashes(rec, exclude=(rec["id"],))
            add(tag + ": no interference with any other body", not hits, "clashes %s" % hits)
            mount = tower if pg["face"] == "tower" else bosses
            dm = f.dist(rs, mount)
            add(tag + ": root seated on its mounting body (%s)" % ("tower" if pg["face"] == "tower" else "High Peg root boss"),
                dm < 1e-6, "distance %.6f" % dm)
            behind = [root - n * 0.02] + [root - n * 0.02 + 0.97 * (EY * PEG_R * math.cos(2 * math.pi * k / 8) +
                                                                  EZ * (ELLIPSE_H / 2) * math.sin(2 * math.pi * k / 8)) for k in range(8)]
            on_mount = all(f.inside(mount, p) for p in behind)
            on_led = [p for p in behind if f.inside(all_rings, p) or f.inside(lantern, p)]
            add(tag + ": whole root footprint backed by opaque structure (not an LED ring or the lantern)",
                on_mount and not on_led, "all on mount %s, on ring/lantern %d" % (on_mount, len(on_led)))

            # ---- ROPE COIL rest poses ------------------------------------------------------
            ex = (rec["id"],)
            # (a) perpendicular to the peg, hole concentric: 5.0 ID over 1.5 OD
            s_c = (COIL_R * S45 + COIL_r) / S45 + 0.5
            Tc = torus(root + u * s_c, u)
            dc = f.dist([Tc], rs)
            cvc = f.common_volume([Tc], rs)
            add(tag + ": coil perpendicular to the peg, concentric: 5.0 hole clears 1.5 peg by 1.75 radial",
                cvc < 1e-9 and abs(dc - (COIL_ID - PEG_OD) / 2) < TOL, "clearance %.4f, overlap %.2e" % (dc, cvc))
            # (b) perpendicular-to-peg bounding pose, hanging: top of the hole on the peg, slid
            #     down the peg until 0.01 from the face
            dn = unit(-EZ + (EZ @ u) * u)
            eps = 0.01
            s_h = (COIL_R * S45 + COIL_r + eps) / S45 - (COIL_ID / 2 - PEG_R - eps)
            Tp = torus(root + u * s_h + dn * (COIL_ID / 2 - PEG_R - eps), u)
            hits = C.clashes(Tp, exclude=())
            dp = f.dist([Tp], rs)
            add(tag + ": coil in the perpendicular-to-peg rest pose rests on the peg, clear of peg/face/everything",
                not hits and dp < 0.03, "peg gap %.4f, clashes %s" % (dp, hits))
            # (c) near-vertical wedged pose: plane parallel to the face, inner face 1.25 outboard,
            #     hung on the peg (upper tube 0.01 above it)
            oc = COIL_INNER_OUT + COIL_r
            zc = oc - COIL_R + (COIL_r + PEG_R + eps) * math.sqrt(2)
            Tv = torus(root + n * oc + EZ * zc, n)
            hits = C.clashes(Tv, exclude=())
            dv_ = f.dist([Tv], rs)
            thread = f.common_volume([disk(root + n * oc + EZ * zc, n, COIL_ID / 2)], rs)
            add(tag + ": near-vertical pose (plane // face, inner face 1.25 out) hangs on the peg, peg through the hole, no clash",
                not hits and dv_ < 0.03 and thread > 1e-4,
                "centre %.3f above root, peg gap %.4f, peg-in-hole section %.4f in^3, clashes %s" % (zc, dv_, thread, hits))
            side_coils[(pg["level"], pg["sgn"])] = Tv
            # (d) near-vertical with the centre exactly 1.0 above the root (the other published number)
            oc2 = COIL_CENTRE_UP + COIL_R - (COIL_r + PEG_R + eps) * math.sqrt(2)
            Tv2 = torus(root + n * oc2 + EZ * COIL_CENTRE_UP, n)
            hits = C.clashes(Tv2, exclude=())
            dv2 = f.dist([Tv2], rs)
            add(tag + ": near-vertical pose with centre 1.0 above root hangs on the peg, clear of peg and face",
                not hits and dv2 < 0.03, "inner face %.3f out, peg gap %.4f, clashes %s" % (oc2 - COIL_r, dv2, hits))
            # (e) the generator's own ROPE COIL in pose (c)
            src = f.find("re:^ROPE COIL")[0]
            sb = C.bb[src["id"]]
            so = (np.array(sb[:3]) + np.array(sb[3:])) / 2
            G = moved_copy(src, so, EZ, root + n * oc + EZ * zc, n, "generator ROPE COIL")
            gcv = f.common_volume([G], rs)
            gd = f.dist([G], rs)
            gface = f.dist([G], mount + (tower if pg["face"] == "tower" else spire + lantern))
            add(tag + ": generator's ROPE COIL hung in the near-vertical pose clears the peg and face",
                gcv < 1e-9 and gd < 0.03 and gface > 1.0, "overlap %.2e, peg gap %.4f, face gap %.3f" % (gcv, gd, gface))
            if pg["level"] == "Low Peg":
                zmin = min(f.bbox([Tv])[2], f.bbox([Tp])[2], f.bbox([Tv2])[2])
                add(tag + ": coil at rest stays above the PEG FACE tag panel (Z 22.0)", zmin > TAG_PANEL_TOP,
                    "lowest coil point Z %.3f" % zmin)

        coils_by_side[side] = side_coils

        # ---- pair spacing / tags ----------------------------------------------------------
        byk = {(p["level"], p["sgn"]): p for p in pegs if p["rec"] is not None}
        for level, _, lat, _ in LEVELS:
            if (level, -1) in byk and (level, 1) in byk:
                ya = [(np.array(C.bb[byk[(level, s)]["rec"]["id"]][1]) + C.bb[byk[(level, s)]["rec"]["id"]][4]) / 2 for s in (-1, 1)]
                gap = abs(ya[1] - ya[0])
                add("%s %s pair: roots %.1f apart" % (side, level, 2 * lat), abs(gap - 2 * lat) < TOL, "measured %.4f" % gap)
        for tid in TAG_IDS[side]:
            try:
                tb = f.bbox(f.find("AprilTag %d - %s CRAG PEG FACE" % (tid, side)))
            except KeyError:
                add("%s tag %d present for the peg-over-tag check" % (side, tid), False, "missing")
                continue
            ty = (tb[1] + tb[4]) / 2
            for level in ("Low Peg", "Mid Peg"):
                pyb = [(C.bb[p["rec"]["id"]][1] + C.bb[p["rec"]["id"]][4]) / 2 for p in pegs
                       if p["level"] == level and p["rec"] is not None and abs(p["root"][1] - ty) < 7]
                add("%s %s directly above AprilTag %d" % (side, level, tid), len(pyb) == 1 and abs(pyb[0] - ty) < TOL,
                    "tag Y %.4f, peg Y %s" % (ty, fmt(pyb)))

        # ---- adjacent coils do not interfere --------------------------------------------
        def cd(k1, k2):
            if k1 in side_coils and k2 in side_coils:
                return f.dist([side_coils[k1]], [side_coils[k2]])
            return float("nan")
        for level, _, lat, _ in LEVELS:
            d = cd((level, -1), (level, 1))
            add("%s coils on the two %ss clear each other (%.0f apart vs 10.0 OD)" % (side, level, 2 * lat),
                d > 2 * lat - COIL_OD - TOL, "gap %.4f (want %.2f)" % (d, 2 * lat - COIL_OD))
        for sg in (-1, 1):
            d = cd(("Low Peg", sg), ("Mid Peg", sg))
            add("%s coils on the Low and Mid Pegs (sgn %d) clear each other" % (side, sg), d > 24.0 - COIL_OD - TOL,
                "gap %.4f" % d)

        # ---- robot approach (High Peg reach) ---------------------------------------------
        for p in pegs:
            if p["level"] != "High Peg" or p["rec"] is None:
                continue
            wb = C.bb[p["rec"]["id"]]
            rx = wb[0] if p["n"][0] > 0 else wb[3]
            root_in = abs(tfx - rx)
            reach_root = root_in + FRAME_PERIM
            tip_reach = reach_root - HORIZ_PROJ
            add("%s High Peg Y=%g: root 14.0 inboard of the tower PEG FACE, 17.0 reach <= 18.0" % (side, p["root"][1]),
                abs(root_in - SPIRE_INBOARD) < TOL and reach_root <= REACH_LIMIT,
                "inboard %.4f, reach %.4f, tip (apex) reach %.4f (doc 9.93)" % (root_in, reach_root, tip_reach))

        # ---- High Peg root bosses ------------------------------------------------------
        for p in pegs:
            if p["level"] != "High Peg":
                continue
            root, n = p["root"], p["n"]
            tag = "%s High Peg root boss Y=%g" % (side, root[1])
            mine = [b for b in bosses if abs((C.bb[b["id"]][1] + C.bb[b["id"]][4]) / 2 - root[1]) < 2.0]
            if len(mine) != 1:
                add(tag + ": one boss at the peg", False, "found %d" % len(mine))
                continue
            b = mine[0]
            bb = C.bb[b["id"]]
            xin = root[0] - n[0] * BOSS_T
            want = [min(root[0], xin), root[1] - BOSS_W / 2, BOSS_Z[0], max(root[0], xin), root[1] + BOSS_W / 2, BOSS_Z[1]]
            err = max(abs(x - y) for x, y in zip(bb, want))
            add(tag + ": let flush into the spire face, 0.25 deep, 3.0 wide, Z 74-80", err < TOL,
                "got %s want %s" % (fmt(bb, 3), fmt(want, 3)))
            rgb, alpha = f.color([b])
            add(tag + ": colour `crag-accent` #4A3B22, opaque", tuple(rgb) == RGB_ACCENT and alpha == 1, "rgb %s alpha %s" % (rgb, alpha))
            m = f.material([b])
            add(tag + ": material steel plate", "steel" in m["name"].lower() and STEEL_DENSITY[0] <= m["density"] <= STEEL_DENSITY[1],
                "%s %.0f" % (m["name"], m["density"]))
            cv = {nm_: f.common_volume([b], rs_) for nm_, rs_ in (("lantern", lantern), ("spire", spire), ("ring78", rings["78"]))}
            add(tag + ": no overlap with lantern / spire / ring 78", all(v < 1e-9 for v in cv.values()), "%s" % cv)
            dsp = f.dist([b], spire)
            below = [root - n * (BOSS_T + 0.05) + EZ * (zz - root[2]) for zz in (74.5, 76.0, 77.5)]
            backed = all(f.inside(spire, q) for q in below)
            add(tag + ": let into the opaque spire (seated on the spire panel behind it below the joint)",
                dsp < 1e-6 and backed, "distance %.6f, spire behind boss at Z 74.5/76/77.5: %s" % (dsp, backed))
            # lantern's lower edge opaque over the 3.0 in of face width at the peg (Z 78 up to the boss top)
            pts = [root - n * 0.1 + EY * dy + EZ * (zz - root[2]) for dy in (-1.45, -0.75, 0.0, 0.75, 1.45)
                   for zz in (78.1, 78.6, 79.06, 79.5, 79.9)]
            bad = [fmt(q, 2) for q in pts if f.inside(lantern, q) or not f.inside([b], q)]
            add(tag + ": lantern lower edge opaque (steel) across the 3.0 in at the peg, Z 78-80", not bad,
                "translucent/empty at %s" % bad[:4])
            # ring 78 interrupted over the boss, continuous beside it
            gap_pts = [root - n * 0.1 + EY * dy + EZ * (77.5 - root[2]) for dy in (-1.45, 0.0, 1.45)]
            in_gap = [fmt(q, 2) for q in gap_pts if f.inside(rings["78"], q)]
            beside = [root - n * 0.1 + EY * dy + EZ * (77.5 - root[2]) for dy in (-1.75, 1.75)]
            miss = [fmt(q, 2) for q in beside if not f.inside(rings["78"], q) and abs(q[1] - (FIELD_W - 240 if side == "RED" else 240)) < SPIRE_HALF - 0.3]
            add(tag + ": 78 ring interrupted exactly over the boss", not in_gap and not miss,
                "ring inside boss width at %s; ring missing beside it at %s" % (in_gap, miss))

        # ring 78 continuous on the rest of the spire peg face (centre)
        cy = 240.0 if side == "BLUE" else FIELD_W - 240.0
        hx = [p["root"][0] for p in pegs if p["level"] == "High Peg"][0]
        nn = pegs[0]["n"]
        pc = np.array([hx, cy, 77.5]) - nn * 0.1
        add("%s 78 ring present on the spire peg face between the High Pegs" % side, f.inside(rings["78"], pc),
            "probe %s" % fmt(pc, 2))

    # ---- symmetry: Red pegs are the Blue pegs rotated 180 deg about (324, 162) --------------
    for level, _, _, _ in LEVELS:
        try:
            bl = find_sided(f, "BLUE CRAG %s" % level)
            rd = find_sided(f, "RED CRAG %s" % level)
            if not bl or not rd:
                raise KeyError(level)
        except KeyError:
            add("RED %ss = BLUE %ss rotated 180 deg about (324, 162)" % (level, level), False, "pegs missing")
            continue
        vb, vr = f.volume(bl), f.volume(rd)
        bbb = f.bbox(bl)
        rb = f.bbox(rd)
        rot = [FIELD_L - bbb[3], FIELD_W - bbb[4], bbb[2], FIELD_L - bbb[0], FIELD_W - bbb[1], bbb[5]]
        err = max(abs(a - b) for a, b in zip(rot, rb))
        add("RED %ss = BLUE %ss rotated 180 deg about (324, 162)" % (level, level), err < 1e-3 and abs(vb - vr) < 1e-3,
            "bbox err %.5f, volumes %.4f / %.4f" % (err, vb, vr))

    # ---- coil tilt capacity on a built peg (§2.5 "at most about 48 deg (47.9)") --------------
    pg = [p for p in expected_pegs("BLUE") if p["level"] == "Low Peg" and p["sgn"] == 1][0]
    rs = [r for r in find_sided(f, "BLUE CRAG Low Peg") if abs((f.bbox([r])[1] + f.bbox([r])[4]) / 2 - pg["root"][1]) < 1]
    if rs:
        def clash_at(th):
            el = math.radians(PEG_ANG - th)
            a = pg["n"] * math.cos(el) + EZ * math.sin(el)
            return f.common_volume([torus(pg["root"] + pg["u"] * 5.5, a)], rs) > 1e-9
        lo, hi = 0.0, 80.0
        for _ in range(24):
            mid = (lo + hi) / 2
            if clash_at(mid):
                hi = mid
            else:
                lo = mid
        add("coil (10.0 OD torus) can hang vertically on a 1.5 peg at 45 deg (tilt capacity >= 45 deg)", lo >= 45.0,
            "measured max tilt from perpendicular-to-peg %.2f deg (package states 47.9)" % lo)
    else:
        add("coil (10.0 OD torus) can hang vertically on a 1.5 peg at 45 deg (tilt capacity >= 45 deg)", False,
            "no BLUE Low Peg at Y %g" % pg["root"][1])
    return out
