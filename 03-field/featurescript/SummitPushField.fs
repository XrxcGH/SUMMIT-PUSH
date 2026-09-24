FeatureScript 2960;
import(path : "onshape/std/geometry.fs", version : "2960.0");

// =====================================================================================
// SUMMIT PUSH — field generator (Onshape FeatureScript)
//
// Builds the complete SUMMIT PUSH field from the locked design package: carpet, guardrails
// and FIELD LEDs, alliance walls with driver stations, four OUTFITTER chutes, both CRAGS with
// every scoring position and their BASE DEPOTS, both HEADWALLS, all tape, 26 AprilTag panels
// with 36h11 decals, and the 63 SUPPLIES in their staged poses — with names, colours,
// materials and densities from 03-field/MATERIALS-AND-COLORS.md.
//
// Coordinate frame: always-blue-origin NWU, inches.  The Part Studio origin is the right
// corner of the Blue alliance wall; +X toward Red, +Y left (from Blue), +Z up.
//
// GENERATED FILE — built by 03-field/featurescript/build.py from src/*.fs.  Edit the
// sources, not this file.  Verified off-line by 03-field/featurescript/verify/run.py.
// =====================================================================================

// ---------------------------------------------------------------- src/10_kernel.fs

// =====================================================================================
// KERNEL — the only code in this Feature Studio that talks to the Onshape standard
// library.  Everything else (the part code in 20_*.fs .. 49_*.fs) is written in plain
// numbers — inches and degrees — and calls these helpers, which add the units.
//
// Every helper here has a twin in verify/kernel_occ.py with identical semantics, so the
// part code can be executed off-line against an OpenCascade kernel and measured.
// Change one, change the other.
//
// Conventions
//   * A frame F is a CoordSystem (see frameMake).  Local points p = [x, y, z] (inches).
//   * A local plane pl = [origin, normal, xDir] (3-vectors, in F coordinates).  Sketch
//     coordinates on it are (u, v) with u along xDir and v along normal x xDir.
//   * "bodies" arguments are arrays of Ids; each Id stands for every body created by it.
// =====================================================================================

function kQ(bodies is array) returns Query
{
    var qs = [];
    for (var b in bodies)
    {
        qs = append(qs, qCreatedBy(b, EntityType.BODY));
    }
    return qBodyType(qUnion(qs), BodyType.SOLID);
}

function kPt(F is CoordSystem, p) returns Vector
{
    const yAxis = cross(F.zAxis, F.xAxis);
    return F.origin + (F.xAxis * p[0] + yAxis * p[1] + F.zAxis * p[2]) * inch;
}

function kDir(F is CoordSystem, d) returns Vector
{
    const yAxis = cross(F.zAxis, F.xAxis);
    return normalize(F.xAxis * d[0] + yAxis * d[1] + F.zAxis * d[2]);
}

function kPlane(F is CoordSystem, pl is array, offset is number) returns Plane
{
    const n = kDir(F, pl[1]);
    return plane(kPt(F, pl[0]) + n * offset * inch, n, kDir(F, pl[2]));
}

function k2(p) returns Vector
{
    return vector(p[0], p[1]) * inch;
}

// ---------- plain-number maths (degrees) ----------------------------------------------

function sind(a is number) returns number
{
    return sin(a * degree);
}

function cosd(a is number) returns number
{
    return cos(a * degree);
}

function tand(a is number) returns number
{
    return tan(a * degree);
}

function atan2d(y is number, x is number) returns number
{
    return atan2(y * inch, x * inch) / degree;
}

function nm(s is string, i) returns string
{
    return s ~ i;
}

function msg(parts is array) returns string
{
    var s = "";
    for (var p in parts)
    {
        s = s ~ p;
    }
    return s;
}

// ---------- frames ---------------------------------------------------------------------

function frameMake(o, x, z) returns CoordSystem
{
    return coordSystem(vector(o[0], o[1], o[2]) * inch, vector(x[0], x[1], x[2]), vector(z[0], z[1], z[2]));
}

// Frame whose origin and axes are given in the coordinates of frame F.
function frameIn(F is CoordSystem, o, x, z) returns CoordSystem
{
    return coordSystem(kPt(F, o), kDir(F, x), kDir(F, z));
}

// ---------- sketch profiles -------------------------------------------------------------
// A loop is an array of segments:  ["L", a, b]  line;  ["A", a, mid, b]  3-point arc;
// ["C", centre, r]  full circle.  a, b, mid, centre are [u, v] sketch points.

function kSketchLoops(sk is Sketch, loops is array)
{
    var n = 0;
    for (var loop in loops)
    {
        for (var s in loop)
        {
            n += 1;
            const nid = "s" ~ n;
            if (s[0] == "L")
            {
                skLineSegment(sk, nid, { "start" : k2(s[1]), "end" : k2(s[2]) });
            }
            else if (s[0] == "A")
            {
                skArc(sk, nid, { "start" : k2(s[1]), "mid" : k2(s[2]), "end" : k2(s[3]) });
            }
            else
            {
                skCircle(sk, nid, { "center" : k2(s[1]), "radius" : s[2] * inch });
            }
        }
    }
}

function kPolyLoop(pts is array) returns array
{
    var loop = [];
    for (var i = 0; i < size(pts); i += 1)
    {
        const j = (i + 1 == size(pts)) ? 0 : i + 1;
        loop = append(loop, ["L", pts[i], pts[j]]);
    }
    return loop;
}

// Extrude the region bounded by `loops` (first loop outer, the rest holes) on plane pl,
// from d0 to d1 along the plane normal (d1 > d0).
function mkPrismProfile(context is Context, id is Id, F is CoordSystem, pl is array, loops is array, d0 is number, d1 is number)
{
    if (!(d1 > d0))
        throw regenError("SUMMIT PUSH kernel: mkPrismProfile needs d1 > d0 (" ~ d0 ~ ", " ~ d1 ~ ")");
    const P = kPlane(F, pl, d0);
    const skId = id + "sk";
    const sk = newSketchOnPlane(context, skId, { "sketchPlane" : P });
    kSketchLoops(sk, loops);
    skSolve(sk);
    opExtrude(context, id + "ex", {
                "entities" : qSketchRegion(skId, true),
                "direction" : P.normal,
                "endBound" : BoundingType.BLIND,
                "endDepth" : (d1 - d0) * inch
            });
    opDeleteBodies(context, id + "dl", { "entities" : qCreatedBy(skId, EntityType.BODY) });
}

function mkPrism(context is Context, id is Id, F is CoordSystem, pl is array, pts is array, d0 is number, d1 is number)
{
    mkPrismProfile(context, id, F, pl, [kPolyLoop(pts)], d0, d1);
}

function mkPrismHoles(context is Context, id is Id, F is CoordSystem, pl is array, outer is array, holes is array, d0 is number, d1 is number)
{
    var loops = [kPolyLoop(outer)];
    for (var h in holes)
    {
        loops = append(loops, kPolyLoop(h));
    }
    mkPrismProfile(context, id, F, pl, loops, d0, d1);
}

function mkCyl(context is Context, id is Id, F is CoordSystem, pl is array, c, r is number, d0 is number, d1 is number)
{
    mkPrismProfile(context, id, F, pl, [[["C", c, r]]], d0, d1);
}

function mkTube(context is Context, id is Id, F is CoordSystem, pl is array, c, ro is number, ri is number, d0 is number, d1 is number)
{
    mkPrismProfile(context, id, F, pl, [[["C", c, ro]], [["C", c, ri]]], d0, d1);
}

// Full 360-degree revolve of the closed profile `loop` (sketched on pl) about the
// plane's v axis through its origin.  The profile must lie in u >= 0.
function mkRevolve(context is Context, id is Id, F is CoordSystem, pl is array, loop is array)
{
    const P = kPlane(F, pl, 0);
    const skId = id + "sk";
    const sk = newSketchOnPlane(context, skId, { "sketchPlane" : P });
    kSketchLoops(sk, [loop]);
    skSolve(sk);
    opRevolve(context, id + "rv", {
                "entities" : qSketchRegion(skId, true),
                "axis" : line(P.origin, cross(P.normal, P.x)),
                "endBound" : RevolveBoundingType.BLIND,
                "endBoundAngle" : 2 * PI * radian,
                "startBound" : RevolveBoundingType.BLIND,
                "startBoundAngle" : 0 * radian,
                "endBoundOffset" : 0 * radian,
                "startBoundOffset" : 0 * radian
            });
    opDeleteBodies(context, id + "dl", { "entities" : qCreatedBy(skId, EntityType.BODY) });
}

// Pillowed cube: side 2*h, every face a biquadratic Bezier patch that is flat on the
// cube edges and rises `crown` at the face centre.  Centred on the frame origin.
function mkPillowBox(context is Context, id is Id, F is CoordSystem, h is number, crown is number)
{
    var sheets = [];
    for (var ax = 0; ax < 3; ax += 1)
    {
        for (var sgn in [-1, 1])
        {
            var rows = [];
            for (var i = 0; i < 3; i += 1)
            {
                var row = [];
                for (var j = 0; j < 3; j += 1)
                {
                    const a = (i - 1) * h;
                    const b = (j - 1) * h * sgn;
                    const c = sgn * (h + ((i == 1 && j == 1) ? 4 * crown : 0));
                    var p = [0, 0, 0];
                    p[ax] = c;
                    p[(ax + 1) % 3] = a;
                    p[(ax + 2) % 3] = b;
                    row = append(row, kPt(F, p));
                }
                rows = append(rows, row);
            }
            const sid = id + ("face" ~ ax ~ (sgn > 0 ? "p" : "n"));
            opCreateBSplineSurface(context, sid, {
                        "bSplineSurface" : bSplineSurface({
                                    "uDegree" : 2,
                                    "vDegree" : 2,
                                    "isUPeriodic" : false,
                                    "isVPeriodic" : false,
                                    "controlPoints" : controlPointMatrix(rows)
                                })
                    });
            sheets = append(sheets, qCreatedBy(sid, EntityType.BODY));
        }
    }
    opEnclose(context, id + "ex", { "entities" : qUnion(sheets) });
    opDeleteBodies(context, id + "dl", { "entities" : qUnion(sheets) });
}

// ---------- booleans and body operations ------------------------------------------------

function bSubtract(context is Context, id is Id, targets is array, tools is array, keepTools is boolean)
{
    opBoolean(context, id, {
                "targets" : kQ(targets),
                "tools" : kQ(tools),
                "operationType" : BooleanOperationType.SUBTRACTION,
                "keepTools" : keepTools
            });
}

// Style every input body identically BEFORE calling this: the merged body keeps the
// name and appearance of whichever tool survives.
function bUnion(context is Context, id is Id, bodies is array)
{
    opBoolean(context, id, {
                "tools" : kQ(bodies),
                "operationType" : BooleanOperationType.UNION
            });
}

function bDelete(context is Context, id is Id, bodies is array)
{
    opDeleteBodies(context, id, { "entities" : kQ(bodies) });
}

// Hollow a closed solid inward by t (no faces removed).
function shellHollow(context is Context, id is Id, bodies is array, t is number)
{
    opShell(context, id, { "entities" : kQ(bodies), "thickness" : -t * inch });
}

// Fillet the edges of `bodies` passing through the local points `pts`.
function filletAt(context is Context, id is Id, bodies is array, F is CoordSystem, pts is array, r is number)
{
    var qs = [];
    for (var p in pts)
    {
        qs = append(qs, qContainsPoint(qOwnedByBody(kQ(bodies), EntityType.EDGE), kPt(F, p)));
    }
    opFillet(context, id, { "entities" : qUnion(qs), "radius" : r * inch, "tangentPropagation" : true });
}

// Same as filletAt, but a failure is reported as a feature warning instead of an error
// (used only for reference-grade roundovers that no rule depends on).
function softFilletAt(context is Context, id is Id, bodies is array, F is CoordSystem, pts is array, r is number, label is string)
{
    try silent
    {
        filletAt(context, id, bodies, F, pts, r);
    }
    catch (e)
    {
        reportFeatureWarning(context, id, "SUMMIT PUSH: reference roundover skipped - " ~ label);
    }
}

// Copy `src` bodies to frame F (the source is modelled about the world origin).
function copyBody(context is Context, id is Id, src is array, F is CoordSystem)
{
    opPattern(context, id, {
                "entities" : kQ(src),
                "transforms" : [toWorld(F)],
                "instanceNames" : ["c"]
            });
}

// ---------- properties ------------------------------------------------------------------

function kColor(rgb is array, alpha is number) returns Color
{
    return color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, alpha);
}

function styleBody(context is Context, bodies is array, name is string, rgb is array, alpha is number, mat is map)
{
    const q = kQ(bodies);
    setProperty(context, { "entities" : q, "propertyType" : PropertyType.NAME, "value" : name });
    setProperty(context, { "entities" : q, "propertyType" : PropertyType.APPEARANCE, "value" : kColor(rgb, alpha) });
    setProperty(context, { "entities" : q, "propertyType" : PropertyType.MATERIAL,
                "value" : material(mat["name"], mat["density"] * kilogram / meter ^ 3) });
}

function nameBody(context is Context, bodies is array, name is string)
{
    setProperty(context, { "entities" : kQ(bodies), "propertyType" : PropertyType.NAME, "value" : name });
}

// Faces of `bodies` that contain the local points `pts` get their own appearance.
function styleFacesAt(context is Context, bodies is array, F is CoordSystem, pts is array, rgb is array, alpha is number)
{
    var qs = [];
    for (var p in pts)
    {
        qs = append(qs, qContainsPoint(qOwnedByBody(kQ(bodies), EntityType.FACE), kPt(F, p)));
    }
    setProperty(context, { "entities" : qUnion(qs), "propertyType" : PropertyType.APPEARANCE, "value" : kColor(rgb, alpha) });
}

// Material whose density makes the body weigh exactly massLb.  Returns the density
// (kg/m^3, plain number) so the caller can report it.
function massBody(context is Context, bodies is array, matName is string, massLb is number) returns number
{
    const q = kQ(bodies);
    const vol = evVolume(context, { "entities" : q });
    const rho = massLb * pound / vol;
    setProperty(context, { "entities" : q, "propertyType" : PropertyType.MATERIAL, "value" : material(matName, rho) });
    return rho / (kilogram / meter ^ 3);
}

// AprilTag decal: split the panel face lying in plane pl into a grid of `cells` x `cells`
// squares of side s centred on the plane origin, and paint the listed [row, col] cells
// (row 0 at the top, col 0 at the left, as seen facing the tag).
function tagDecal(context is Context, id is Id, bodies is array, F is CoordSystem, pl is array, black is array, cells is number, s is number, rgb is array)
{
    const P = kPlane(F, pl, 0);
    const skId = id + "sk";
    try silent
    {
        const sk = newSketchOnPlane(context, skId, { "sketchPlane" : P });
        const h = cells / 2;
        for (var i = 0; i <= cells; i += 1)
        {
            for (var j = 0; j < cells; j += 1)
            {
                skLineSegment(sk, "h" ~ i ~ "_" ~ j, { "start" : k2([(j - h) * s, (h - i) * s]), "end" : k2([(j + 1 - h) * s, (h - i) * s]) });
                skLineSegment(sk, "v" ~ i ~ "_" ~ j, { "start" : k2([(i - h) * s, (h - j) * s]), "end" : k2([(i - h) * s, (h - j - 1) * s]) });
            }
        }
        skSolve(sk);
        opSplitFace(context, id + "sp", {
                    "faceTargets" : qContainsPoint(qOwnedByBody(kQ(bodies), EntityType.FACE), P.origin),
                    "edgeTools" : qCreatedBy(skId, EntityType.EDGE)
                });
        opDeleteBodies(context, id + "dl", { "entities" : qCreatedBy(skId, EntityType.BODY) });
        var qs = [];
        for (var rc in black)
        {
            const c = [(rc[1] + 0.5 - h) * s, (h - rc[0] - 0.5) * s];
            qs = append(qs, qContainsPoint(qOwnedByBody(kQ(bodies), EntityType.FACE), P.origin + (P.x * c[0] + cross(P.normal, P.x) * c[1]) * inch));
        }
        setProperty(context, { "entities" : qUnion(qs), "propertyType" : PropertyType.APPEARANCE, "value" : kColor(rgb, 1) });
    }
    catch (e)
    {
        try silent
        {
            opDeleteBodies(context, id + "dl2", { "entities" : qCreatedBy(skId, EntityType.BODY) });
        }
        reportFeatureWarning(context, id, "SUMMIT PUSH: AprilTag decal could not be applied; the panel is built without it");
    }
}

// ---------- measurement (used by the dimension self-check) --------------------------------

// Tight bounding box of `bodies` in frame F: [xmin, ymin, zmin, xmax, ymax, zmax] (inches).
function measureBox(context is Context, bodies is array, F is CoordSystem) returns array
{
    const b = evBox3d(context, { "topology" : kQ(bodies), "cSys" : F, "tight" : true });
    return [b.minCorner[0] / inch, b.minCorner[1] / inch, b.minCorner[2] / inch,
            b.maxCorner[0] / inch, b.maxCorner[1] / inch, b.maxCorner[2] / inch];
}

function measureVolume(context is Context, bodies is array) returns number
{
    return evVolume(context, { "entities" : kQ(bodies) }) / inch ^ 3;
}

// Minimum distance from local point p to `bodies` (0 if the point is on or inside).
function measureDistToPoint(context is Context, bodies is array, F is CoordSystem, p) returns number
{
    return evDistance(context, { "side0" : kQ(bodies), "side1" : kPt(F, p) }).distance / inch;
}

function measureDist(context is Context, a is array, b is array) returns number
{
    return evDistance(context, { "side0" : kQ(a), "side1" : kQ(b) }).distance / inch;
}

function countBodies(context is Context, bodies is array) returns number
{
    return size(evaluateQuery(context, kQ(bodies)));
}

// ---------------------------------------------------------------- src/20_ledger.fs

// =====================================================================================
// LEDGER — every number the field is built from.  Sources: 03-field/FIELD-CAD-PACKAGE.md
// (§10 master dimension ledger and the per-element sections) and
// 03-field/MATERIALS-AND-COLORS.md.  Inches and degrees.  (ref) = reference geometry the
// package leaves free; the value chosen here is documented in README.md.
// =====================================================================================

// ---- field (§0, §1) ---------------------------------------------------------------------
const FIELD_L = 648;
const FIELD_W = 324;
const FIELD_CX = 324;
const FIELD_CY = 162;
const CARPET_T = 0.25;          // (ref) carpet thickness, below Z = 0
const TAPE_W = 2;
const TAPE_T = 0.01;

// ---- perimeter (§1.3) --------------------------------------------------------------------
const GUARD_H = 20;
const GUARD_RAIL_H = 2;         // (ref) 2 x 1 in tube: 2 tall, 1 deep
const GUARD_RAIL_D = 1;
const GUARD_POST_PITCH = 81;    // (ref) 8 bays
const GUARD_GLAZE_T = 0.25;
const LED_Z = 19;               // FIELD LED lens centre
const LED_W = 1;
const LED_DEPTH = 0.25;         // (ref) let into the top rail
const WALL_H = 78;
const WALL_T = 2;
const WALL_SOLID_H = 39;
const WALL_PANEL_T = 0.75;
const WALL_GLAZE_T = 0.25;
const WALL_RAIL = 2;            // (ref) frame member, 2 tall/wide x 1.25 deep
const STATION_Y = [54, 162, 270];
const STATION_W = 96;
const STATION_SHELF_TOP = 36;
const STATION_SHELF_T = 0.75;
const STATION_SHELF_D = 12;     // (ref)
const BUTTON_HEAD_D = 2;

// ---- OUTFITTER (§5) ----------------------------------------------------------------------
const CHUTE_Y = [30, 294];      // Blue; Red is the 180-degree rotation
const CHUTE_W = 30;
const CHUTE_H = 16;
const CHUTE_SILL = 24;
const CHUTE_SILL_R = 0.5;       // (ref)
const RAMP_ANGLE = 30;          // (ref)
const RAMP_RUN = 40;            // (ref) measured along the ramp
const RAMP_T = 0.5;
const RAMP_FLARE_W = 36;        // (ref) cheek funnel width at the loading end
const CHEEK_H = 8;              // (ref) cheek height above the ramp
const LANE_TAPE_W = 36;
const LANE_TAPE_D = 48;

// ---- CRAG (§2) ---------------------------------------------------------------------------
const CRAG_BLUE = [324, 240];
const CRAG_RED = [324, 84];
const CRAG_S = 48;
const CRAG_H = 60;
const CRAG_PANEL_T = 0.75;
const SPIRE_S = 20;
const SPIRE_TOP = 90;
const LANTERN_LO = 78;
const LANTERN_T = 0.25;
const SHELF_Z = [24, 42];
const SHELF_DEPTH = 14;
const SHELF_T = 0.75;
const SHELF_ROUND = 0.25;       // (ref)
const SLOT_W = 14;
const SLOT_CTRS = [-15.5, 0, 15.5];
const FENCE_W = 1.5;
const FENCE_H = 2;
const FENCE_POS = [0, 15.5, 31, 46.5];   // left edges from the face's left edge
const GUSSET_LEG = 3;           // (ref) 45-degree gusset legs
const GUSSET_T = 0.125;
const GUSSET_Y = [-22, -7.75, 7.75, 22];  // (ref) lateral stations, clear of the tag prisms
const SOCK_ID = 6.5;
const SOCK_WALL = 0.09;
const SOCK_LEN = 7;             // along the axis, rim plane to outer bottom face
const SOCK_STANDOFF = 8;
const SOCK_LAT = 14;
const SOCK_TILT = 30;
const LOW_SOCK_Z = 30;
const MID_SOCK_Z = 54;
const SUM_SOCK_Z = 72;
const SUM_TILT = 15;
const SOCK_BRACKET_T = 0.125;
const MAST_S = 2;               // Summit Socket mast, 2 x 2 steel tube
const MAST_BASE_X = 20;         // (ref) mast arm starts 4.0 in inside the shelf-face edge
const PEG_OD = 1.5;
const PEG_EXP = 10;
const PEG_ANG = 45;
const PEG_TIP_R = 0.75;
const PEG_EMBED = 1.5;          // (ref) length modelled behind the root before trimming
const PEG_Z = [30, 54];
const PEG_LAT = 14;
const HPEG_Z = 78;
const HPEG_LAT = 7;
const BOSS_W = 3;
const BOSS_T = 0.25;
const BOSS_Z = [74, 80];
const RING_Z = [30, 54];        // centred rings on the tower
const RING_W = 1;
const RING_DEPTH = 0.25;
const RING78_TOP = 78;          // the 78 ring hangs from the lantern joint: Z 77-78
const RING_GAP = 3;             // rings break over 3.0 in of face width at each peg
const KICK_H = 2;
const KICK_T = 0.125;
const TAG_Z_CRAG = 17.5;

// ---- BASE DEPOT (§3) ---------------------------------------------------------------------
const DEPOT_CH = 16;
const DEPOT_WRAP = 16;
const DEPOT_LIP_Z = 4;
const DEPOT_LIP_T = 0.75;
const DEPOT_LIP_R = 0.25;
const DEPOT_FLOOR_T = 0.25;
const DEPOT_CHAMFER = 1;

// ---- HEADWALL (§4) -----------------------------------------------------------------------
const HW_X = 48;
const HW_LEAN = 15;
const HW_Y0 = 90;
const HW_Y1 = 234;
const LANE_W = 48;
const LANE_Y = [114, 162, 210];
const RUNG_TOP = [30, 54, 78];
const RUNG_STAGGER = [-12, 12, -12];
const RUNG_OD = 1.5;
const RUNG_L = 20;
const TRUSS_CLR = 4;
const TRUSS_TOP = 84;
const TUBE_S = 2;
const TUBE_WALL = 0.12;         // (ref) 11-gauge
const UPRIGHT_N = [-8, -6];     // (ref) upright layer, normal offset from plane P
const FRONT_N = [-6, -4];       // front layer: rung carriers, rails
const BEAM_N = [-10, -8];       // (ref) lower crossbeam layer — see README (spec finding)
const UPRIGHT_INSET = 2.5;      // (ref) upright's inner face from the lane edge
const BRACKET_T = 0.25;
const BRACKET_FROM_END = 1;     // bracket plate 1.0-1.25 in from each rung end
const BRACKET_FRONT = 1;        // plate reaches 1.0 in in front of plane P
const TAG_HW_X = 39;
const TAG_Z_HW = 12;
const BEAM_Z = 12;

// ---- AprilTags (§7) ----------------------------------------------------------------------
const TAG_BODY = 6.5;
const TAG_TARGET = 8.125;
const TAG_PANEL = 9;
const TAG_PANEL_T = 0.25;
const TAG_Z_OUT = 52;
const TAG_CELL = 0.8125;        // 8.125 / 10 = 6.5 / 8

// ---- game pieces (§9) --------------------------------------------------------------------
const CRATE_S = 12;
const CRATE_CROWN = 0.5;
const CRATE_FILLET = 1;
const CRATE_LB = 2;
const CELL_D = 5;
const CELL_L = 14;
const CELL_DOME = 1.5;
const CELL_FILLET = 1;
const CELL_LB = 1.5;
const COIL_OD = 10;
const COIL_TUBE = 2.5;
const COIL_LB = 1;
const CACHE_X = [300, 324, 348];
const CACHE_Y = [138, 162, 186];
const STAGE_X = 144;            // Blue; Red is the rotation (504)
const STAGE_Y = [108, 162, 216];

// ---- appearance (MATERIALS-AND-COLORS §1) — decimal RGB of the published hex ------------
const PAL = {
        "alliance-blue" : [29, 99, 200],        // #1D63C8
        "alliance-blue-dark" : [14, 63, 134],   // #0E3F86
        "alliance-red" : [204, 51, 51],         // #CC3333
        "alliance-red-dark" : [142, 32, 32],    // #8E2020
        "neutral-white" : [245, 245, 245],      // #F5F5F5
        "led-green" : [63, 191, 79],            // #3FBF4F
        "crag-body" : [233, 226, 212],          // #E9E2D4
        "crag-spire" : [221, 211, 192],         // #DDD3C0
        "crag-accent" : [74, 59, 34],           // #4A3B22
        "beacon-lantern" : [255, 243, 208],     // #FFF3D0 at 35 %
        "truss" : [138, 109, 59],               // #8A6D3B
        "truss-dark" : [92, 72, 35],            // #5C4823
        "rung" : [154, 160, 166],               // #9AA0A6
        "shelf" : [138, 109, 59],               // #8A6D3B
        "socket" : [157, 184, 214],             // #9DB8D6
        "depot" : [127, 127, 127],              // #7F7F7F
        "wall" : [154, 164, 178],               // #9AA4B2
        "glazing" : [220, 232, 250],            // #DCE8FA at 25 %
        "carpet" : [110, 106, 99],              // #6E6A63
        "crate-violet" : [123, 63, 160],        // #7B3FA0
        "cell-body" : [242, 242, 240],          // #F2F2F0
        "cell-cap" : [46, 139, 87],             // #2E8B57
        "cell-fillet" : [77, 77, 77],           // #4D4D4D
        "coil-amber" : [217, 164, 65],          // #D9A441
        "estop-red" : [204, 32, 32],            // #CC2020
        "tag-black" : [17, 17, 17],             // #111111
        "led-dark" : [43, 43, 43],              // (ref) unlit LED channel
        "button-base" : [51, 51, 51]            // (ref)
    };
const ALPHA_LANTERN = 0.35;
const ALPHA_GLAZING = 0.25;
const ALPHA_LIT = 0.9;

// ---- materials: name and density (kg/m^3).  "effective" = a solid body standing in for a
// hollow tube, with the density scaled by the tube's wall-area fraction so mass is right.
const MAT = {
        "carpet" : { "name" : "Event carpet, low pile", "density" : 220 },
        "plywood" : { "name" : "Plywood, painted", "density" : 600 },
        "hardwood" : { "name" : "Hardwood (maple), painted", "density" : 705 },
        "uhmw-ply" : { "name" : "UHMW-faced plywood", "density" : 650 },
        "aluminum" : { "name" : "Aluminum 6061", "density" : 2700 },
        "steel" : { "name" : "Steel, mild", "density" : 7850 },
        "polycarbonate" : { "name" : "Polycarbonate", "density" : 1200 },
        "acrylic" : { "name" : "Acrylic (PMMA), frosted", "density" : 1190 },
        "tape" : { "name" : "Gaffer tape", "density" : 830 },
        "tag" : { "name" : "Printed vinyl on rigid PVC backer", "density" : 1400 },
        "abs" : { "name" : "ABS, molded", "density" : 1050 },
        "al-tube-2x1" : { "name" : "Aluminum 2 x 1 x 0.125 tube (effective solid)", "density" : 928.1 },
        "steel-tube-2x2" : { "name" : "Steel 2 x 2 x 0.120 tube (effective solid)", "density" : 1771 },
        "steel-frame" : { "name" : "Steel 2 x 1.25 x 0.083 tube (effective solid)", "density" : 1608 }
    };

// ---------------------------------------------------------------- src/30_util.fs

// =====================================================================================
// UTIL — small helpers shared by the element builders.  Part-code dialect.
// =====================================================================================

// Sketch planes in a frame.  plXY: (u, v) = (x, y), extrude along +z.
// plYZ: (u, v) = (y, z), extrude along +x.  plXZ: (u, v) = (x, z), extrude along -y.
function plXY(z0)
{
    return [[0, 0, z0], [0, 0, 1], [1, 0, 0]];
}

function plYZ(x0)
{
    return [[x0, 0, 0], [1, 0, 0], [0, 1, 0]];
}

function plXZ(y0)
{
    return [[0, y0, 0], [0, -1, 0], [1, 0, 0]];
}

// Plane containing an axis, for revolves: v runs along `axis`, u along `radial`
// (both unit vectors, perpendicular), origin at `o`.
function plAxis(o, axis, radial)
{
    return [o, cross(vector(radial[0], radial[1], radial[2]), vector(axis[0], axis[1], axis[2])), radial];
}

// Plane normal to `axis` through `o`, with `xd` as its sketch u direction.
function plNormal(o, axis, xd)
{
    return [o, axis, xd];
}

function rectPts(u0, v0, u1, v1)
{
    return [[u0, v0], [u1, v0], [u1, v1], [u0, v1]];
}

// Axis-aligned box in frame F between local corners p0 and p1.
function mkBox(context is Context, id is Id, F, p0, p1)
{
    mkPrism(context, id, F, plXY(0), rectPts(min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])),
            min(p0[2], p1[2]), max(p0[2], p1[2]));
}

// Prism from an (x, z) polygon, spanning y0..y1 in frame F.
function prismXZ(context is Context, id is Id, F, pts, y0, y1)
{
    mkPrism(context, id, F, plXZ(0), pts, -y1, -y0);
}

function prismXZHoles(context is Context, id is Id, F, outer, holes, y0, y1)
{
    mkPrismHoles(context, id, F, plXZ(0), outer, holes, -y1, -y0);
}

// Prism from a (y, z) polygon, spanning x0..x1 in frame F.
function prismYZ(context is Context, id is Id, F, pts, x0, x1)
{
    mkPrism(context, id, F, plYZ(0), pts, x0, x1);
}

// Prism from an (x, y) polygon, spanning z0..z1 in frame F.
function prismXY(context is Context, id is Id, F, pts, z0, z1)
{
    mkPrism(context, id, F, plXY(0), pts, z0, z1);
}

function prismXYHoles(context is Context, id is Id, F, outer, holes, z0, z1)
{
    mkPrismHoles(context, id, F, plXY(0), outer, holes, z0, z1);
}

// ---- alliance frames ---------------------------------------------------------------------
// Blue builds in world coordinates; Red is the same geometry rotated 180 degrees about the
// vertical line through field centre (324, 162).
function allianceFrame(isRed)
{
    if (isRed)
    {
        return frameMake([FIELD_L, FIELD_W, 0], [-1, 0, 0], [0, 0, 1]);
    }
    return frameMake([0, 0, 0], [1, 0, 0], [0, 0, 1]);
}

function worldFrame()
{
    return frameMake([0, 0, 0], [1, 0, 0], [0, 0, 1]);
}

// World point of Blue point p after the 180-degree rotation (for Red coordinates).
function rot180(p)
{
    return [FIELD_L - p[0], FIELD_W - p[1], p[2]];
}

function allianceName(isRed)
{
    if (isRed)
    {
        return "RED";
    }
    return "BLUE";
}

function allianceRGB(isRed)
{
    if (isRed)
    {
        return PAL["alliance-red"];
    }
    return PAL["alliance-blue"];
}

// Style shortcut: palette token + material key.
function paint(context is Context, bodies, name, tok, alpha, matKey)
{
    styleBody(context, bodies, name, PAL[tok], alpha, MAT[matKey]);
}

function paintRGB(context is Context, bodies, name, rgb, alpha, matKey)
{
    styleBody(context, bodies, name, rgb, alpha, MAT[matKey]);
}

// Square tube profile (outer square with a hole) for hollow members: returns [outer, [hole]].
function tubeLoops(u0, v0, u1, v1, wall)
{
    return [rectPts(u0, v0, u1, v1), [rectPts(u0 + wall, v0 + wall, u1 - wall, v1 - wall)]];
}

// ---------------------------------------------------------------- src/40_field.fs

// =====================================================================================
// FIELD PERIMETER — carpet, guardrails with FIELD LED bands, alliance walls, driver
// stations and OUTFITTER chutes (FIELD-CAD-PACKAGE §1.3, §5; MATERIALS-AND-COLORS §2).
// Part-code dialect.
// =====================================================================================

function buildCarpet(context is Context, id is Id)
{
    const W = worldFrame();
    mkBox(context, id + "carpet", W, [0, 0, -CARPET_T], [FIELD_L, FIELD_W, 0]);
    paint(context, [id + "carpet"], "Field carpet", "carpet", 1, "carpet");
}

// FIELD LED colour for a segment on the Blue (X < 324) or Red half.
function fieldLedRGB(opts, isRedHalf)
{
    const st = opts["fieldLed"];
    if (st == "GREEN")
    {
        return PAL["led-green"];
    }
    if (st == "FORECAST")
    {
        return PAL["neutral-white"];
    }
    if (st == "ROUTE")
    {
        return allianceRGB(isRedHalf);
    }
    return PAL["led-dark"];
}

// One long-side guardrail.  side 0 runs along Y = 0, side 1 along Y = 324.  Built in world
// coordinates because its LED segments are coloured by field half, not by alliance.
function buildGuardrail(context is Context, id is Id, side, opts)
{
    const W = worldFrame();
    var yIn = 0;
    var yOut = -GUARD_RAIL_D;
    var gIn = LED_DEPTH;
    var label = "Y = 0";
    if (side == 1)
    {
        yIn = FIELD_W;
        yOut = FIELD_W + GUARD_RAIL_D;
        gIn = -LED_DEPTH;
        label = "Y = 324";
    }
    const lo = min(yIn, yOut);
    const hi = max(yIn, yOut);
    const name = msg(["Guardrail (", label, ")"]);
    mkBox(context, id + "bot", W, [0, lo, 0], [FIELD_L, hi, GUARD_RAIL_H]);
    mkBox(context, id + "top", W, [0, lo, GUARD_H - GUARD_RAIL_H], [FIELD_L, hi, GUARD_H]);
    // FIELD LED bands: two 324-in segments let into the inner face of the top rail
    const ledLo = min(yIn, yIn - gIn);
    const ledHi = max(yIn, yIn - gIn);
    mkBox(context, id + "ledA", W, [0, ledLo, LED_Z - LED_W / 2], [FIELD_CX, ledHi, LED_Z + LED_W / 2]);
    mkBox(context, id + "ledB", W, [FIELD_CX, ledLo, LED_Z - LED_W / 2], [FIELD_L, ledHi, LED_Z + LED_W / 2]);
    bSubtract(context, id + "groove", [id + "top"], [id + "ledA", id + "ledB"], true);
    paintRGB(context, [id + "ledA"], msg([name, " FIELD LED, Blue half"]), fieldLedRGB(opts, false), 1, "acrylic");
    paintRGB(context, [id + "ledB"], msg([name, " FIELD LED, Red half"]), fieldLedRGB(opts, true), 1, "acrylic");
    paint(context, [id + "bot"], msg([name, " bottom rail"]), "wall", 1, "al-tube-2x1");
    paint(context, [id + "top"], msg([name, " top rail"]), "wall", 1, "al-tube-2x1");
    // posts and glazing bays
    var posts = [[0, GUARD_RAIL_D]];
    for (var k = 1; k < 8; k += 1)
    {
        posts = append(posts, [k * GUARD_POST_PITCH - GUARD_RAIL_D / 2, k * GUARD_POST_PITCH + GUARD_RAIL_D / 2]);
    }
    posts = append(posts, [FIELD_L - GUARD_RAIL_D, FIELD_L]);
    const gMid = (yIn + yOut) / 2;
    for (var i = 0; i < size(posts); i += 1)
    {
        const pid = id + nm("post", i);
        mkBox(context, pid, W, [posts[i][0], lo, GUARD_RAIL_H], [posts[i][1], hi, GUARD_H - GUARD_RAIL_H]);
        paint(context, [pid], msg([name, " post"]), "wall", 1, "al-tube-2x1");
        if (i + 1 < size(posts))
        {
            const gid = id + nm("glaze", i);
            mkBox(context, gid, W, [posts[i][1], gMid - GUARD_GLAZE_T / 2, GUARD_RAIL_H],
                    [posts[i + 1][0], gMid + GUARD_GLAZE_T / 2, GUARD_H - GUARD_RAIL_H]);
            paint(context, [gid], msg([name, " glazing"]), "glazing", ALPHA_GLAZING, "polycarbonate");
        }
    }
}

// Driver-station shelf span for station centre s: the shelf is cut back clear of the
// OUTFITTER chute so a CACHE CRATE can slide down the ramp (README: spec finding F-1).
function stationShelfSpan(s)
{
    var lo = s - STATION_W / 2;
    var hi = s + STATION_W / 2;
    const clear = RAMP_FLARE_W / 2 + RAMP_T;
    for (var c in CHUTE_Y)
    {
        if (c - clear < hi && c + clear > lo)
        {
            if (c < s)
            {
                lo = c + clear;
            }
            else
            {
                hi = c - clear;
            }
        }
    }
    return [lo, hi];
}

function buildButton(context is Context, id is Id, F, x, y, tok, name)
{
    const zTop = STATION_SHELF_TOP;
    mkCyl(context, id + "base", F, plXY(0), [x, y], 0.625, zTop, zTop + 1);
    paint(context, [id + "base"], msg([name, " base"]), "button-base", 1, "abs");
    // mushroom head: 1.0-in radius skirt 0.5 tall, then a spherical cap to 1.0 above the skirt base
    const z0 = zTop + 1;
    const rc = 1.25;
    const zc = z0 + 1 - rc;
    const aMid = (atan2d(z0 + 0.5 - zc, 1) + 90) / 2;
    const loop = [["L", [0, z0], [1, z0]],
            ["L", [1, z0], [1, z0 + 0.5]],
            ["A", [1, z0 + 0.5], [rc * cosd(aMid), zc + rc * sind(aMid)], [0, z0 + 1]],
            ["L", [0, z0 + 1], [0, z0]]];
    mkRevolve(context, id + "head", F, plAxis([x, y, 0], [0, 0, 1], [1, 0, 0]), loop);
    paint(context, [id + "head"], name, tok, 1, "abs");
}

// One alliance wall with its driver stations and both OUTFITTER chutes.
function buildAllianceWall(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const wn = msg([A, " alliance wall"]);
    // lower solid panel and upper glazing, both flush with the field-side plane x = 0
    mkBox(context, id + "panel", F, [-WALL_PANEL_T, 0, 0], [0, FIELD_W, WALL_SOLID_H]);
    mkBox(context, id + "glaze", F, [-WALL_GLAZE_T, 0, WALL_SOLID_H], [0, FIELD_W, WALL_H]);
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        const c = CHUTE_Y[i];
        mkBox(context, id + nm("open", i), F, [-WALL_T - 1, c - CHUTE_W / 2, CHUTE_SILL], [1, c + CHUTE_W / 2, CHUTE_SILL + CHUTE_H]);
        bSubtract(context, id + nm("cut", i), [id + "panel", id + "glaze"], [id + nm("open", i)], false);
        // pocket for the OUTFITTER AprilTag panel, which sits flush in the glazing plane
        mkBox(context, id + nm("tagpk", i), F, [-WALL_GLAZE_T - 0.05, c - TAG_PANEL / 2, TAG_Z_OUT - TAG_PANEL / 2],
                [0.1, c + TAG_PANEL / 2, TAG_Z_OUT + TAG_PANEL / 2]);
        bSubtract(context, id + nm("tagcut", i), [id + "glaze"], [id + nm("tagpk", i)], false);
    }
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        softFilletAt(context, id + nm("sill", i), [id + "panel"], F, [[0, CHUTE_Y[i], CHUTE_SILL]], CHUTE_SILL_R, "OUTFITTER sill edge");
    }
    paint(context, [id + "panel"], msg([wn, " lower panel"]), "wall", 1, "plywood");
    paint(context, [id + "glaze"], msg([wn, " glazing"]), "glazing", ALPHA_GLAZING, "polycarbonate");

    // steel frame behind the panels (ref): rails and posts, 2.0 in overall wall thickness
    const fx0 = -WALL_T;
    const fx1 = -WALL_PANEL_T;
    var fr = [];
    mkBox(context, id + "frBot", F, [fx0, 0, 0], [fx1, FIELD_W, WALL_RAIL]);
    mkBox(context, id + "frTop", F, [fx0, 0, WALL_H - WALL_RAIL], [fx1, FIELD_W, WALL_H]);
    fr = [id + "frBot", id + "frTop"];
    const midSpans = [[0, CHUTE_Y[0] - CHUTE_W / 2], [CHUTE_Y[0] + CHUTE_W / 2, CHUTE_Y[1] - CHUTE_W / 2], [CHUTE_Y[1] + CHUTE_W / 2, FIELD_W]];
    for (var i = 0; i < size(midSpans); i += 1)
    {
        mkBox(context, id + nm("frMid", i), F, [fx0, midSpans[i][0], WALL_SOLID_H - 1], [fx1, midSpans[i][1], WALL_SOLID_H + 1]);
        fr = append(fr, id + nm("frMid", i));
    }
    const postY = [0, STATION_Y[0] + STATION_W / 2 + 5, STATION_Y[1] + STATION_W / 2 + 5, FIELD_W - WALL_RAIL];
    for (var i = 0; i < size(postY); i += 1)
    {
        mkBox(context, id + nm("frPostLo", i), F, [fx0, postY[i], WALL_RAIL], [fx1, postY[i] + WALL_RAIL, WALL_SOLID_H - 1]);
        mkBox(context, id + nm("frPostHi", i), F, [fx0, postY[i], WALL_SOLID_H + 1], [fx1, postY[i] + WALL_RAIL, WALL_H - WALL_RAIL]);
        fr = append(fr, id + nm("frPostLo", i));
        fr = append(fr, id + nm("frPostHi", i));
    }
    paint(context, fr, msg([wn, " frame"]), "wall", 1, "steel-frame");

    // driver stations: shelf (clear of the chutes) and E-STOP / A-STOP buttons
    for (var i = 0; i < size(STATION_Y); i += 1)
    {
        const s = STATION_Y[i];
        const span = stationShelfSpan(s);
        const sid = id + nm("station", i + 1);
        mkBox(context, sid + "shelf", F, [-WALL_T - STATION_SHELF_D, span[0], STATION_SHELF_TOP - STATION_SHELF_T],
                [-WALL_T, span[1], STATION_SHELF_TOP]);
        paint(context, [sid + "shelf"], msg([A, " driver station ", i + 1, " shelf"]), "wall", 1, "plywood");
        var by = s + 30;
        if (span[1] < s + 40)
        {
            by = s - 36;
        }
        buildButton(context, sid + "estop", F, -8, by, "estop-red", msg([A, " driver station ", i + 1, " E-STOP"]));
        buildButton(context, sid + "astop", F, -8, by + 6, "alliance-blue", msg([A, " driver station ", i + 1, " A-STOP"]));
    }

    // OUTFITTER chutes: ramp, cheek funnels and the ramp's leg (behind the wall, ref)
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        buildOutfitterRamp(context, id + nm("outfitter", i + 1), F, CHUTE_Y[i], msg([A, " OUTFITTER ", i + 1]));
    }
}

function buildOutfitterRamp(context is Context, id is Id, F, c, name)
{
    const s30 = sind(RAMP_ANGLE);
    const c30 = cosd(RAMP_ANGLE);
    const x0 = -WALL_PANEL_T;                      // back face of the lower panel = sill line
    const half0 = CHUTE_W / 2;
    const half1 = RAMP_FLARE_W / 2;
    // ramp: trapezoid in the 30-degree plane, top surface through the sill line
    const upN = [s30, 0, c30];
    const slope = [-c30, 0, s30];
    mkPrism(context, id + "ramp", F, [[x0, c, CHUTE_SILL], upN, slope],
            [[0, -half0], [RAMP_RUN, -half1], [RAMP_RUN, half1], [0, half0]], -RAMP_T, 0);
    paint(context, [id + "ramp"], msg([name, " chute ramp"]), "wall", 1, "uhmw-ply");
    // leg under the loading end
    const xTop = x0 - RAMP_RUN * c30;              // top surface, loading end
    const xb = xTop - RAMP_T * s30;                // underside corner, loading end
    const zb = CHUTE_SILL + RAMP_RUN * s30 - RAMP_T * c30;
    const xl1 = xb + RAMP_T;
    const zl1 = zb - RAMP_T * tand(RAMP_ANGLE);
    prismXZ(context, id + "leg", F, [[xb, 0], [xl1, 0], [xl1, zl1], [xb, zb]], c - half1 + 0.5, c + half1 - 0.5);
    paint(context, [id + "leg"], msg([name, " ramp leg"]), "wall", 1, "plywood");
    // cheek funnels: vertical plates on the ramp's slanted edges, flaring 30 -> 36 in
    const runX = RAMP_RUN * c30;
    const flare = half1 - half0;
    const L = sqrt(runX * runX + flare * flare);
    const u0 = 0.25;
    for (var sg in [-1, 1])
    {
        const t = [-runX / L, sg * flare / L, 0];
        const n = [flare / L, sg * runX / L, 0];
        const zAt0 = CHUTE_SILL + (u0 * runX / L) * tand(RAMP_ANGLE);
        const zAt1 = CHUTE_SILL + RAMP_RUN * s30;
        const cid = id + nm("cheek", (sg + 1) / 2);
        mkPrism(context, cid, F, [[x0, c + sg * half0, 0], n, t],
                [[u0, sg * (zAt0 - 1)], [L, sg * (zAt1 - 1)], [L, sg * (zAt1 + CHEEK_H)], [u0, sg * (zAt0 + CHEEK_H)]], 0, RAMP_T);
        paint(context, [cid], msg([name, " cheek funnel"]), "wall", 1, "plywood");
    }
}

// ---------------------------------------------------------------- src/41_crag.fs

// =====================================================================================
// CRAG (x2) and its BASE DEPOT — FIELD-CAD-PACKAGE §2, §3, §8.  Part-code dialect.
//
// Local frame: origin at the CRAG centre on the carpet, +x = SHELF FACE outward normal,
// +z up (so the SHELF FACE is x = +24, the PEG FACE x = -24, the SOCKET FACES y = +/-24).
// Blue: +x = world -X.  Red: the same frame rotated 180 degrees about field centre.
// =====================================================================================

function cragFrame(isRed)
{
    if (isRed)
    {
        return frameMake([CRAG_RED[0], CRAG_RED[1], 0], [1, 0, 0], [0, 0, 1]);
    }
    return frameMake([CRAG_BLUE[0], CRAG_BLUE[1], 0], [-1, 0, 0], [0, 0, 1]);
}

// Tier ring let 0.25 in into a square body of half-size h, band z0..z1, broken over
// RING_GAP of face width at the two PEG FACE stations y = +/-gc.  Returns the piece Ids.
function buildRing(context is Context, id is Id, F, h, gc, z0, z1)
{
    const d = RING_DEPTH;
    const g1 = gc + RING_GAP / 2;
    const g0 = gc - RING_GAP / 2;
    const hi = h - d;
    prismXY(context, id + "a", F, [[-h, g1], [-h, h], [h, h], [h, -h], [-h, -h], [-h, -g1], [-hi, -g1],
                [-hi, -hi], [hi, -hi], [hi, hi], [-hi, hi], [-hi, g1]], z0, z1);
    mkBox(context, id + "b", F, [-h, -g0, z0], [-hi, g0, z1]);
    return [id + "a", id + "b"];
}

// Open-topped tube with a closed bottom: outer bottom-face centre b, unit axis a (towards
// the mouth), unit radial r perpendicular to a.  Rim plane at SOCK_LEN along a.
function buildSocketTube(context is Context, id is Id, F, b, a, r)
{
    const ri = SOCK_ID / 2;
    const ro = ri + SOCK_WALL;
    mkRevolve(context, id, F, plAxis(b, a, r),
            [["L", [0, 0], [ro, 0]], ["L", [ro, 0], [ro, SOCK_LEN]], ["L", [ro, SOCK_LEN], [ri, SOCK_LEN]],
                ["L", [ri, SOCK_LEN], [ri, SOCK_WALL]], ["L", [ri, SOCK_WALL], [0, SOCK_WALL]], ["L", [0, SOCK_WALL], [0, 0]]]);
}

// Peg with a hemispherical tip: root point p on the face, unit axis u, unit radial r.
// Modelled PEG_EMBED behind the root, then trimmed flush with the face by `trim`
// (a box on the structure side of the face).
function buildPeg(context is Context, id is Id, F, p, u, r, trim0, trim1)
{
    const pr = PEG_OD / 2;
    const tipBase = PEG_EXP - PEG_TIP_R;
    mkRevolve(context, id + "rod", F, plAxis(p, u, r),
            [["L", [0, -PEG_EMBED], [pr, -PEG_EMBED]], ["L", [pr, -PEG_EMBED], [pr, tipBase]],
                ["A", [pr, tipBase], [PEG_TIP_R * cosd(45), tipBase + PEG_TIP_R * sind(45)], [0, PEG_EXP]],
                ["L", [0, PEG_EXP], [0, -PEG_EMBED]]]);
    mkBox(context, id + "trim", F, trim0, trim1);
    bSubtract(context, id + "flush", [id + "rod"], [id + "trim"], false);
}

function buildCrag(context is Context, id is Id, isRed, opts)
{
    const F = cragFrame(isRed);
    const A = allianceName(isRed);
    const cn = msg([A, " CRAG"]);
    const h = CRAG_S / 2;
    const sh = SPIRE_S / 2;
    const lit = opts["lit"];

    // ---- tower, spire, lantern (hollow panel bodies) -------------------------------
    mkBox(context, id + "tower", F, [-h, -h, 0], [h, h, CRAG_H]);
    shellHollow(context, id + "towerShell", [id + "tower"], CRAG_PANEL_T);
    mkBox(context, id + "spire", F, [-sh, -sh, CRAG_H], [sh, sh, LANTERN_LO]);
    shellHollow(context, id + "spireShell", [id + "spire"], CRAG_PANEL_T);
    mkBox(context, id + "lantern", F, [-sh, -sh, LANTERN_LO], [sh, sh, SPIRE_TOP]);
    shellHollow(context, id + "lanternShell", [id + "lantern"], LANTERN_T);

    // ---- tier rings: 30 and 54 on the tower, 78 on the spire ------------------------
    const r30 = buildRing(context, id + "ring30", F, h, PEG_LAT, RING_Z[0] - RING_W / 2, RING_Z[0] + RING_W / 2);
    const r54 = buildRing(context, id + "ring54", F, h, PEG_LAT, RING_Z[1] - RING_W / 2, RING_Z[1] + RING_W / 2);
    const r78 = buildRing(context, id + "ring78", F, sh, HPEG_LAT, RING78_TOP - RING_W, RING78_TOP);

    // ---- High Peg root bosses (steel, let into the spire and the lantern's lower edge)
    mkBox(context, id + "bossP", F, [-sh, HPEG_LAT - BOSS_W / 2, BOSS_Z[0]], [-sh + BOSS_T, HPEG_LAT + BOSS_W / 2, BOSS_Z[1]]);
    mkBox(context, id + "bossN", F, [-sh, -HPEG_LAT - BOSS_W / 2, BOSS_Z[0]], [-sh + BOSS_T, -HPEG_LAT + BOSS_W / 2, BOSS_Z[1]]);

    // ---- kick-guard: 2 x 2 x 0.125 aluminium angle, flush with the faces -------------
    prismXYHoles(context, id + "kickV", F, rectPts(-h, -h, h, h), [rectPts(-h + KICK_T, -h + KICK_T, h - KICK_T, h - KICK_T)], 0, KICK_H);
    prismXYHoles(context, id + "kickH", F, rectPts(-h + KICK_T, -h + KICK_T, h - KICK_T, h - KICK_T),
            [rectPts(-h + KICK_H, -h + KICK_H, h - KICK_H, h - KICK_H)], 0, KICK_T);
    paint(context, [id + "kickV", id + "kickH"], msg([cn, " kick-guard"]), "crag-accent", 1, "aluminum");
    bUnion(context, id + "kickJoin", [id + "kickV", id + "kickH"]);

    // ---- AprilTag pockets: 9.0 x 9.0 x 0.25, two per face at +/-14, centre Z 17.5 ----
    var pk = [];
    const tz0 = TAG_Z_CRAG - TAG_PANEL / 2;
    const tz1 = TAG_Z_CRAG + TAG_PANEL / 2;
    const tp = TAG_PANEL / 2;
    for (var lat in [-SOCK_LAT, SOCK_LAT])
    {
        const k = (lat + SOCK_LAT) / (2 * SOCK_LAT);
        mkBox(context, id + nm("pkS", k), F, [h - TAG_PANEL_T, lat - tp, tz0], [h + 0.1, lat + tp, tz1]);
        mkBox(context, id + nm("pkP", k), F, [-h - 0.1, lat - tp, tz0], [-h + TAG_PANEL_T, lat + tp, tz1]);
        mkBox(context, id + nm("pkYp", k), F, [lat - tp, h - TAG_PANEL_T, tz0], [lat + tp, h + 0.1, tz1]);
        mkBox(context, id + nm("pkYn", k), F, [lat - tp, -h - 0.1, tz0], [lat + tp, -h + TAG_PANEL_T, tz1]);
        pk = concatenateArrays([pk, [id + nm("pkS", k), id + nm("pkP", k), id + nm("pkYp", k), id + nm("pkYn", k)]]);
    }
    bSubtract(context, id + "towerCut", [id + "tower"], pk, false);
    bSubtract(context, id + "towerGroove", [id + "tower"], concatenateArrays([r30, r54, [id + "kickV"]]), true);
    bSubtract(context, id + "spireCut", [id + "spire"], concatenateArrays([r78, [id + "bossP", id + "bossN"]]), true);
    bSubtract(context, id + "lanternCut", [id + "lantern"], [id + "bossP", id + "bossN"], true);

    paint(context, [id + "tower"], msg([cn, " tower"]), "crag-body", 1, "plywood");
    paint(context, [id + "spire"], msg([cn, " spire"]), "crag-spire", 1, "plywood");
    if (lit)
    {
        paintRGB(context, [id + "lantern"], msg([cn, " SUMMIT BEACON (lit)"]), allianceRGB(isRed), ALPHA_LIT, "polycarbonate");
    }
    else
    {
        paint(context, [id + "lantern"], msg([cn, " SUMMIT BEACON"]), "beacon-lantern", ALPHA_LANTERN, "polycarbonate");
    }
    var ringRGB = PAL["led-dark"];
    if (lit)
    {
        ringRGB = allianceRGB(isRed);
    }
    paintRGB(context, r30, msg([cn, " tier ring 30"]), ringRGB, 1, "acrylic");
    paintRGB(context, r54, msg([cn, " tier ring 54"]), ringRGB, 1, "acrylic");
    paintRGB(context, r78, msg([cn, " tier ring 78"]), ringRGB, 1, "acrylic");
    paint(context, [id + "bossP", id + "bossN"], msg([cn, " High Peg root boss"]), "crag-accent", 1, "steel");

    // ---- SHELF FACE: Shelf 1 / Shelf 2, slot fences, gussets ------------------------
    for (var i = 0; i < 2; i += 1)
    {
        const zt = SHELF_Z[i];
        const grp = id + nm("shelf", i + 1);
        const sid = grp + "slab";
        mkBox(context, sid, F, [h, -h, zt - SHELF_T], [h + SHELF_DEPTH, h, zt]);
        softFilletAt(context, sid + "round", [sid], F, [[h + SHELF_DEPTH, 0, zt], [h + SHELF_DEPTH, 0, zt - SHELF_T]], SHELF_ROUND, "shelf front-edge roundover");
        paint(context, [sid], msg([cn, " Shelf ", i + 1]), "shelf", 1, "plywood");
        var fences = [];
        for (var j = 0; j < size(FENCE_POS); j += 1)
        {
            const fid = grp + nm("fence", j);
            mkBox(context, fid, F, [h, -h + FENCE_POS[j], zt], [h + SHELF_DEPTH - SHELF_ROUND, -h + FENCE_POS[j] + FENCE_W, zt + FENCE_H]);
            fences = append(fences, fid);
        }
        paint(context, fences, msg([cn, " Shelf ", i + 1, " slot fence"]), "shelf", 1, "hardwood");
        var gus = [];
        const zb = zt - SHELF_T;
        for (var j = 0; j < size(GUSSET_Y); j += 1)
        {
            const gid = grp + nm("gusset", j);
            prismXZ(context, gid, F, [[h, zb], [h + GUSSET_LEG, zb], [h, zb - GUSSET_LEG]], GUSSET_Y[j] - GUSSET_T / 2, GUSSET_Y[j] + GUSSET_T / 2);
            gus = append(gus, gid);
        }
        paint(context, gus, msg([cn, " Shelf ", i + 1, " gusset"]), "crag-accent", 1, "aluminum");
    }

    // ---- SOCKET FACES: Low (x = +14, rim 30) and Mid (x = -14, rim 54) on y = +/-24 --
    const s30 = sind(SOCK_TILT);
    const c30 = cosd(SOCK_TILT);
    const ro = SOCK_ID / 2 + SOCK_WALL;
    for (var sgn in [-1, 1])
    {
        const fk = (sgn + 1) / 2;
        const socks = [[SOCK_LAT, LOW_SOCK_Z, "Low"], [-SOCK_LAT, MID_SOCK_Z, "Mid"]];
        for (var q in socks)
        {
            const lat = q[0];
            const zr = q[1];
            const tid = id + nm(nm("sock", q[2]), fk);
            const a = [0, sgn * s30, c30];
            const yb = sgn * (h + SOCK_STANDOFF - SOCK_LEN * s30);
            const zbt = zr - SOCK_LEN * c30;
            buildSocketTube(context, tid, F, [lat, yb, zbt], a, [1, 0, 0]);
            paint(context, [tid], msg([cn, " ", q[2], " Socket"]), "socket", 1, "aluminum");
            // bracket plate in the wedge under the tube, top edge 1.0 in below the rim height
            const dy = yb - sgn * ro * c30;
            const dz = zbt + ro * s30;
            const ztop = zr - 1;
            const cy = dy + sgn * (ztop - dz) / c30 * s30;
            const az = dz + (sgn * (dy - sgn * h)) / c30 * s30;
            const bid = id + nm(nm("brk", q[2]), fk);
            prismYZ(context, bid, F, [[sgn * h, az], [dy, dz], [cy, ztop], [sgn * h, ztop]], lat - SOCK_BRACKET_T / 2, lat + SOCK_BRACKET_T / 2);
            paint(context, [bid], msg([cn, " ", q[2], " Socket bracket"]), "crag-accent", 1, "aluminum");
        }
    }

    // ---- Summit Socket (SHELF FACE, rim 72, 15 degrees) and its mast ----------------
    const s15 = sind(SUM_TILT);
    const c15 = cosd(SUM_TILT);
    const sbx = h + SOCK_STANDOFF - SOCK_LEN * s15;
    const sbz = SUM_SOCK_Z - SOCK_LEN * c15;
    buildSocketTube(context, id + "sockSummit", F, [sbx, 0, sbz], [s15, 0, c15], [0, 1, 0]);
    paint(context, [id + "sockSummit"], msg([cn, " Summit Socket"]), "socket", 1, "aluminum");
    const mh = MAST_S / 2;
    mkBox(context, id + "mastArm", F, [MAST_BASE_X, -mh, CRAG_H], [sbx + mh, mh, CRAG_H + MAST_S]);
    prismXZ(context, id + "mastPost", F, [[sbx - mh, CRAG_H + MAST_S], [sbx + mh, CRAG_H + MAST_S],
                [sbx + mh, sbz - mh * s15 / c15], [sbx - mh, sbz + mh * s15 / c15]], -mh, mh);
    paint(context, [id + "mastArm", id + "mastPost"], msg([cn, " Summit Socket mast"]), "crag-accent", 1, "steel-tube-2x2");
    bUnion(context, id + "mastJoin", [id + "mastArm", id + "mastPost"]);

    // ---- PEG FACE (x = -24): Low and Mid Pegs; spire peg face (x = -10): High Pegs ----
    const u = [-cosd(PEG_ANG), 0, sind(PEG_ANG)];
    var pegs = [];
    for (var zi = 0; zi < 2; zi += 1)
    {
        for (var sgn in [-1, 1])
        {
            const y = sgn * PEG_LAT;
            const z = PEG_Z[zi];
            const pid = id + nm(nm("peg", zi), (sgn + 1) / 2);
            buildPeg(context, pid, F, [-h, y, z], u, [0, 1, 0], [-h, y - 3, z - 4], [-h + 4, y + 3, z + 4]);
            pegs = append(pegs, pid);
        }
    }
    paint(context, [pegs[0], pegs[1]], msg([cn, " Low Peg"]), "rung", 1, "steel");
    paint(context, [pegs[2], pegs[3]], msg([cn, " Mid Peg"]), "rung", 1, "steel");
    var hpegs = [];
    for (var sgn in [-1, 1])
    {
        const y = sgn * HPEG_LAT;
        const pid = id + nm("pegHigh", (sgn + 1) / 2);
        buildPeg(context, pid, F, [-sh, y, HPEG_Z], u, [0, 1, 0], [-sh, y - 3, HPEG_Z - 4], [-sh + 4, y + 3, HPEG_Z + 4]);
        hpegs = append(hpegs, pid);
    }
    paint(context, hpegs, msg([cn, " High Peg"]), "rung", 1, "steel");

    buildDepot(context, id + "depot", F, cn);
}

// BASE DEPOT: U-shaped tray around the SHELF FACE and both shelf-face corners.
function buildDepot(context is Context, id is Id, F, cn)
{
    const h = CRAG_S / 2;
    const x0 = h - DEPOT_WRAP;          // arm ends (x = 8)
    const x1 = h + DEPOT_CH;            // outer leg face of the channel (x = 40)
    const y1 = h + DEPOT_CH;            // outer corner (y = 40)
    const t = DEPOT_LIP_T;
    // floor: the channel footprint, top at Z = 0.25
    prismXY(context, id + "floor", F, [[x0, h], [h, h], [h, -h], [x0, -h], [x0, -y1], [x1, -y1], [x1, y1], [x0, y1]], 0, DEPOT_FLOOR_T);
    paint(context, [id + "floor"], msg([cn, " BASE DEPOT floor"]), "depot", 1, "plywood");
    // lip: 0.75-in wall around the outer boundary, top at Z = 4.0
    prismXY(context, id + "lip", F, [[x0 - t, h], [x0 - t, y1 + t], [x1 + t, y1 + t], [x1 + t, -y1 - t], [x0 - t, -y1 - t],
                [x0 - t, -h], [x0, -h], [x0, -y1], [x1, -y1], [x1, y1], [x0, y1], [x0, h]], 0, DEPOT_LIP_Z);
    const zt = DEPOT_LIP_Z;
    filletAt(context, id + "lipRound", [id + "lip"], F, [
                [x0 - t, (h + y1 + t) / 2, zt], [(x0 + x1) / 2, y1 + t, zt], [x1 + t, 0, zt], [(x0 + x1) / 2, -y1 - t, zt], [x0 - t, -(h + y1 + t) / 2, zt],
                [x0, (h + y1) / 2, zt], [(x0 + x1) / 2, y1, zt], [x1, 0, zt], [(x0 + x1) / 2, -y1, zt], [x0, -(h + y1) / 2, zt]], DEPOT_LIP_R);
    paint(context, [id + "lip"], msg([cn, " BASE DEPOT lip"]), "depot", 1, "plywood");
    // 45-degree entry chamfer strip outside the lip, 1.0-in leg
    const c = DEPOT_CHAMFER;
    const xo = x0 - t;
    const yo = y1 + t;
    const xf = x1 + t;
    prismXY(context, id + "chamfer", F, [[xo - c, h], [xo - c, yo + c], [xf + c, yo + c], [xf + c, -yo - c], [xo - c, -yo - c],
                [xo - c, -h], [xo, -h], [xo, -yo], [xf, -yo], [xf, yo], [xo, yo], [xo, h]], 0, c);
    const m = 0.5;
    prismXZ(context, id + "wedgeX", F, [[xf - m, c + m], [xf + c + m, -m], [xf + c + 2 * m, -m], [xf + c + 2 * m, c + m]], -yo - c - 1, yo + c + 1);
    prismYZ(context, id + "wedgeYp", F, [[yo - m, c + m], [yo + c + m, -m], [yo + c + 2 * m, -m], [yo + c + 2 * m, c + m]], xo - c - 1, xf + c + 1);
    prismYZ(context, id + "wedgeYn", F, [[-yo + m, c + m], [-yo - c - m, -m], [-yo - c - 2 * m, -m], [-yo - c - 2 * m, c + m]], xo - c - 1, xf + c + 1);
    prismXZ(context, id + "wedgeAp", F, [[xo + m, c + m], [xo - c - m, -m], [xo - c - 2 * m, -m], [xo - c - 2 * m, c + m]], h - 4, yo + c + 1);
    prismXZ(context, id + "wedgeAn", F, [[xo + m, c + m], [xo - c - m, -m], [xo - c - 2 * m, -m], [xo - c - 2 * m, c + m]], -yo - c - 1, -h + 4);
    bSubtract(context, id + "chamferCut", [id + "chamfer"], [id + "wedgeX", id + "wedgeYp", id + "wedgeYn", id + "wedgeAp", id + "wedgeAn"], false);
    paint(context, [id + "chamfer"], msg([cn, " BASE DEPOT entry chamfer"]), "depot", 1, "plywood");
}

// ---------------------------------------------------------------- src/42_headwall.fs

// =====================================================================================
// HEADWALL (x2) — FIELD-CAD-PACKAGE §4.  Part-code dialect.
//
// Everything derives from PLANE P: the line {x = 48, z = 0} tilted 15 degrees from vertical,
// top toward the alliance wall.  Plane-P coordinates: w runs up the plane, n is the normal
// toward the field (robots climb the +n side), y is lateral.
//     x = 48 - w sin15 + n cos15,   z = w cos15 + n sin15
// All structure except the rung end brackets lies at n <= -4.0 (TRUSS_CLR).
// =====================================================================================

function hwXZ(w, n)
{
    const s = sind(HW_LEAN);
    const c = cosd(HW_LEAN);
    return [HW_X - w * s + n * c, w * c + n * s];
}

// w of a point in plane P (n = 0) at height z.
function hwW(z)
{
    return z / cosd(HW_LEAN);
}

// (n, w) rectangle -> (x, z) polygon.
function hwRect(n0, n1, w0, w1)
{
    return [hwXZ(w0, n0), hwXZ(w0, n1), hwXZ(w1, n1), hwXZ(w1, n0)];
}

// Hollow 2 x 2 tube running along y, cross-section n0..n1 x w0..w1.
function hwTubeY(context is Context, id is Id, F, n0, n1, w0, w1, y0, y1)
{
    const t = TUBE_WALL;
    prismXZHoles(context, id, F, hwRect(n0, n1, w0, w1), [hwRect(n0 + t, n1 - t, w0 + t, w1 - t)], y0, y1);
}

function buildHeadwall(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const hn = msg([A, " HEADWALL"]);
    const s = sind(HW_LEAN);
    const c = cosd(HW_LEAN);
    const wdir = [-s, 0, c];
    const ndir = [c, 0, s];
    const tw = TUBE_WALL;

    var uprights = [];
    var members = [];
    var rungsAll = [];
    var brackets = [];
    for (var li = 0; li < size(LANE_Y); li += 1)
    {
        const yc = LANE_Y[li];
        const ylo = yc - LANE_W / 2;
        const yhi = yc + LANE_W / 2;
        const lid = id + nm("lane", li + 1);
        // two uprights in the back layer, running up plane P (trimmed to Z 0..84 below)
        const uy = [[ylo + UPRIGHT_INSET, ylo + UPRIGHT_INSET + TUBE_S], [yhi - UPRIGHT_INSET - TUBE_S, yhi - UPRIGHT_INSET]];
        for (var k = 0; k < 2; k += 1)
        {
            const uid = lid + nm("upright", k);
            mkPrismHoles(context, uid, F, [[HW_X, 0, 0], wdir, ndir],
                    rectPts(UPRIGHT_N[0], uy[k][0], UPRIGHT_N[1], uy[k][1]),
                    [rectPts(UPRIGHT_N[0] + tw, uy[k][0] + tw, UPRIGHT_N[1] - tw, uy[k][1] - tw)], -3, hwW(TRUSS_TOP) + 6);
            uprights = append(uprights, uid);
        }
        // front-layer tubes: bottom rail, one rung carrier per rung, top rail
        const my0 = ylo + 0.5;
        const my1 = yhi - 0.5;
        hwTubeY(context, lid + "railBot", F, FRONT_N[0], FRONT_N[1], 2, 2 + TUBE_S, my0, my1);
        hwTubeY(context, lid + "railTop", F, FRONT_N[0], FRONT_N[1], 85, 85 + TUBE_S, my0, my1);
        members = concatenateArrays([members, [lid + "railBot", lid + "railTop"]]);
        const rungNames = ["LEDGE RUNG", "CAMP RUNG", "SUMMIT RUNG"];
        for (var ri = 0; ri < size(RUNG_TOP); ri += 1)
        {
            const zc = RUNG_TOP[ri] - RUNG_OD / 2;
            const wc = hwW(zc);
            const cid = lid + nm("carrier", ri);
            hwTubeY(context, cid, F, FRONT_N[0], FRONT_N[1], wc - TUBE_S / 2, wc + TUBE_S / 2, my0, my1);
            members = append(members, cid);
            // the rung: centreline in plane P, 20.0 long, staggered from the lane centre
            const ya = yc + RUNG_STAGGER[ri] - RUNG_L / 2;
            const rid = lid + nm("rung", ri);
            const rc = hwXZ(wc, 0);
            mkCyl(context, rid, F, plXZ(0), rc, RUNG_OD / 2, -(ya + RUNG_L), -ya);
            paint(context, [rid], msg([hn, " lane ", li + 1, " ", rungNames[ri]]), "rung", 1, "steel");
            rungsAll = append(rungsAll, rid);
            // end brackets: plates within 2.0 in of each rung end, carrier face to 1.0 in past P
            const bys = [[ya + BRACKET_FROM_END, ya + BRACKET_FROM_END + BRACKET_T],
                    [ya + RUNG_L - BRACKET_FROM_END - BRACKET_T, ya + RUNG_L - BRACKET_FROM_END]];
            for (var bi = 0; bi < 2; bi += 1)
            {
                const bid = lid + nm(nm("bracket", ri), bi);
                prismXZ(context, bid, F, hwRect(FRONT_N[1], BRACKET_FRONT, wc - TUBE_S / 2, wc + TUBE_S / 2), bys[bi][0], bys[bi][1]);
                bSubtract(context, bid + "hole", [bid], [rid], true);
                brackets = append(brackets, bid);
            }
        }
    }
    // trim the uprights to Z 0 .. 84 (truss chords end at 84 in vertical)
    mkBox(context, id + "trimLo", F, [-20, HW_Y0 - 10, -30], [80, HW_Y1 + 10, 0]);
    mkBox(context, id + "trimHi", F, [-20, HW_Y0 - 10, TRUSS_TOP], [80, HW_Y1 + 10, TRUSS_TOP + 40]);
    bSubtract(context, id + "trim", uprights, [id + "trimLo", id + "trimHi"], false);
    paint(context, uprights, msg([hn, " upright"]), "truss", 1, "steel");
    paint(context, members, msg([hn, " rail"]), "truss", 1, "steel");
    paint(context, brackets, msg([hn, " rung end bracket"]), "truss-dark", 1, "steel");

    // lower crossbeam (behind the uprights) and the three 15-degree tag wedges
    const wcb = (BEAM_Z - (BEAM_N[0] + BEAM_N[1]) / 2 * s) / c;
    hwTubeY(context, id + "crossbeam", F, BEAM_N[0], BEAM_N[1], wcb - TUBE_S / 2, wcb + TUBE_S / 2, HW_Y0, HW_Y1);
    paint(context, [id + "crossbeam"], msg([hn, " lower crossbeam"]), "truss", 1, "steel");
    const pb = hwXZ(wcb - TUBE_S / 2, BEAM_N[1]);
    const pt = hwXZ(wcb + TUBE_S / 2, BEAM_N[1]);
    const xBack = TAG_HW_X - TAG_PANEL_T;
    var wedges = [];
    for (var li = 0; li < size(LANE_Y); li += 1)
    {
        const wid = id + nm("wedge", li + 1);
        prismXZ(context, wid, F, [pb, [xBack, pb[1]], [xBack, pt[1]], pt], LANE_Y[li] - TAG_PANEL / 2, LANE_Y[li] + TAG_PANEL / 2);
        wedges = append(wedges, wid);
    }
    paint(context, wedges, msg([hn, " tag wedge bracket"]), "truss-dark", 1, "aluminum");
}

// ---------------------------------------------------------------- src/43_tape.fs

// =====================================================================================
// TAPE — FIELD-CAD-PACKAGE §1.2 and §6.  2-in gaffer tape modelled as 0.01-in-thick
// solids on the carpet (Z 0 .. 0.01), line edges on the stated coordinate, inside the zone
// they bound.  Where two tapes cross, the one that governs the line call is kept whole and
// the other is cut around it: APRON > marks > centerline > CENTER CACHE band.
// Part-code dialect.
// =====================================================================================

function tapeBox(context is Context, id is Id, F, x0, y0, x1, y1)
{
    prismXY(context, id, F, rectPts(x0, y0, x1, y1), 0, TAPE_T);
}

// 12-in "X": two 2-in bars crossing at 90 degrees, arms along the diagonals.
function xMarkPts(cx, cy, halfLen, halfW)
{
    const plus = [[halfW, halfLen], [-halfW, halfLen], [-halfW, halfW], [-halfLen, halfW], [-halfLen, -halfW], [-halfW, -halfW],
            [-halfW, -halfLen], [halfW, -halfLen], [halfW, -halfW], [halfLen, -halfW], [halfLen, halfW], [halfW, halfW]];
    const c = cosd(45);
    var out = [];
    for (var p in plus)
    {
        out = append(out, [cx + (p[0] - p[1]) * c, cy + (p[0] + p[1]) * c]);
    }
    return out;
}

// Rounded rectangle loop centred on the origin, half-sizes a x b, corner radius r.
function roundRectLoop(a, b, r)
{
    const k = r * (1 - cosd(45));
    return [["L", [-a + r, -b], [a - r, -b]], ["A", [a - r, -b], [a - k, -b + k], [a, -b + r]],
            ["L", [a, -b + r], [a, b - r]], ["A", [a, b - r], [a - k, b - k], [a - r, b]],
            ["L", [a - r, b], [-a + r, b]], ["A", [-a + r, b], [-a + k, b - k], [-a, b - r]],
            ["L", [-a, b - r], [-a, -b + r]], ["A", [-a, -b + r], [-a + k, -b + k], [-a + r, -b]]];
}

// Alliance tape for one side of the field.  Returns [apronId] for the overlap pass.
function buildAllianceTape(context is Context, id is Id, isRed)
{
    const F = allianceFrame(isRed);
    const A = allianceName(isRed);
    const rgb = allianceRGB(isRed);
    const w = TAPE_W;
    var t = [];
    // BASECAMP / HEADWALL ZONE: X 0-48, Y 90-234 (the wall closes the fourth side)
    tapeBox(context, id + "bcX", F, HW_X - w, HW_Y0, HW_X, HW_Y1);
    tapeBox(context, id + "bcLo", F, 0, HW_Y0, HW_X - w, HW_Y0 + w);
    tapeBox(context, id + "bcHi", F, 0, HW_Y1 - w, HW_X - w, HW_Y1);
    paintRGB(context, [id + "bcX", id + "bcLo", id + "bcHi"], msg([A, " BASECAMP tape"]), rgb, 1, "tape");
    // CLIMB LINE: the X = 48 line carried across the full width, dashed outside BASECAMP
    const dashes = [[0, 6], [54, 60], [66, 72], [78, 84], [240, 246], [252, 258], [264, 270], [318, 324]];
    var cl = [];
    for (var i = 0; i < size(dashes); i += 1)
    {
        tapeBox(context, id + nm("climb", i), F, HW_X - w, dashes[i][0], HW_X, dashes[i][1]);
        cl = append(cl, id + nm("climb", i));
    }
    paintRGB(context, cl, msg([A, " CLIMB LINE tape (dashed)"]), rgb, 1, "tape");
    // OUTFITTER LANES: 36 wide x 48 deep, centred on each chute
    for (var i = 0; i < size(CHUTE_Y); i += 1)
    {
        const c = CHUTE_Y[i];
        const lid = id + nm("lane", i + 1);
        tapeBox(context, lid + "end", F, LANE_TAPE_D - w, c - LANE_TAPE_W / 2, LANE_TAPE_D, c + LANE_TAPE_W / 2);
        tapeBox(context, lid + "lo", F, 0, c - LANE_TAPE_W / 2, LANE_TAPE_D - w, c - LANE_TAPE_W / 2 + w);
        tapeBox(context, lid + "hi", F, 0, c + LANE_TAPE_W / 2 - w, LANE_TAPE_D - w, c + LANE_TAPE_W / 2);
        paintRGB(context, [lid], msg([A, " OUTFITTER LANE tape ", i + 1]), rgb, 1, "tape");
    }
    // CRAG APRON: 36 in off the SHELF and PEG FACES, 20 in off the SOCKET FACES, R20 corners
    const CF = cragFrame(isRed);
    const ax = CRAG_S / 2 + 36;
    const ay = CRAG_S / 2 + 20;
    mkPrismProfile(context, id + "apron", CF, plXY(0), [roundRectLoop(ax, ay, 20), roundRectLoop(ax - w, ay - w, 20 - w)], 0, TAPE_T);
    paintRGB(context, [id + "apron"], msg([A, " CRAG APRON tape"]), rgb, 1, "tape");
    // alliance staging marks: white 12-in X with a 0.5-in alliance-colour border
    var marks = [];
    var borders = [];
    for (var i = 0; i < size(STAGE_Y); i += 1)
    {
        const mid = id + nm("stage", i);
        prismXY(context, mid + "white", F, xMarkPts(STAGE_X, STAGE_Y[i], 6, 1), 0, TAPE_T);
        prismXY(context, mid + "border", F, xMarkPts(STAGE_X, STAGE_Y[i], 6.5, 1.5), 0, TAPE_T);
        bSubtract(context, mid + "cut", [mid + "border"], [mid + "white"], true);
        marks = append(marks, mid + "white");
        borders = append(borders, mid + "border");
    }
    paint(context, marks, msg([A, " staging mark"]), "neutral-white", 1, "tape");
    paintRGB(context, borders, msg([A, " staging mark border"]), rgb, 1, "tape");
    return [id + "apron"];
}

function buildTape(context is Context, id is Id)
{
    const W = worldFrame();
    const w = TAPE_W;
    const aprons = concatenateArrays([buildAllianceTape(context, id + "blue", false), buildAllianceTape(context, id + "red", true)]);
    // FIELD centerline, broken at the two CRAG footprints
    const segs = [[0, CRAG_RED[1] - CRAG_S / 2], [CRAG_RED[1] + CRAG_S / 2, CRAG_BLUE[1] - CRAG_S / 2], [CRAG_BLUE[1] + CRAG_S / 2, FIELD_W]];
    var cl = [];
    for (var i = 0; i < size(segs); i += 1)
    {
        tapeBox(context, id + nm("center", i), W, FIELD_CX - w / 2, segs[i][0], FIELD_CX + w / 2, segs[i][1]);
        cl = append(cl, id + nm("center", i));
    }
    // CENTER CACHE band outline: X 300-348, Y 108-216
    const bx0 = CACHE_X[0];
    const bx1 = CACHE_X[2];
    const by0 = CRAG_RED[1] + CRAG_S / 2;
    const by1 = CRAG_BLUE[1] - CRAG_S / 2;
    tapeBox(context, id + "bandL", W, bx0, by0, bx0 + w, by1);
    tapeBox(context, id + "bandR", W, bx1 - w, by0, bx1, by1);
    tapeBox(context, id + "bandB", W, bx0 + w, by0, bx1 - w, by0 + w);
    tapeBox(context, id + "bandT", W, bx0 + w, by1 - w, bx1 - w, by1);
    const band = [id + "bandL", id + "bandR", id + "bandB", id + "bandT"];
    // CENTER CACHE marks: 3 x 3 grid of 12-in X marks
    var marks = [];
    for (var i = 0; i < 3; i += 1)
    {
        for (var j = 0; j < 3; j += 1)
        {
            const mid = id + nm(nm("cache", i), j);
            prismXY(context, mid, W, xMarkPts(CACHE_X[i], CACHE_Y[j], 6, 1), 0, TAPE_T);
            marks = append(marks, mid);
        }
    }
    // overlap pass: the band stops at the BASE DEPOT trays; everything yields to the APRONS
    const dh = CRAG_S / 2 + 20;         // out to the SOCKET FACE APRON line, so no sliver survives
    const dx0 = CRAG_S / 2 - DEPOT_WRAP - DEPOT_LIP_T - DEPOT_CHAMFER;
    const dx1 = CRAG_S / 2 + DEPOT_CH + DEPOT_LIP_T + DEPOT_CHAMFER;
    mkBox(context, id + "depotB", cragFrame(false), [dx0, -dh, -1], [dx1, dh, 1]);
    mkBox(context, id + "depotR", cragFrame(true), [dx0, -dh, -1], [dx1, dh, 1]);
    bSubtract(context, id + "bandDepot", band, [id + "depotB", id + "depotR"], false);
    bSubtract(context, id + "bandOver", band, concatenateArrays([cl, marks, aprons]), true);
    bSubtract(context, id + "centerOver", cl, concatenateArrays([marks, aprons]), true);
    paint(context, cl, "FIELD centerline tape", "neutral-white", 1, "tape");
    paint(context, band, "CENTER CACHE band tape", "neutral-white", 1, "tape");
    paint(context, marks, "CENTER CACHE mark", "neutral-white", 1, "tape");
}

// ---------------------------------------------------------------- src/44_tags.fs

// =====================================================================================
// APRILTAGS — FIELD-CAD-PACKAGE §7, VISION-GUIDE §1.  26 tags, family 36h11.
// Each panel is 9.0 in square x 0.25 in, its front face in the published tag plane (flush
// with the structure it is let into), carrying an 8.125-in target: a 10 x 10 grid of
// 0.8125-in cells whose outer ring is white and whose inner 8 x 8 is the 6.5-in tag body.
// Red tags are the Blue tags rotated 180 degrees about field centre, ID + 13.
// Part-code dialect.
// =====================================================================================

// [ID, x, y, z (tag centre, on the face), yaw of the facing normal in degrees]
const TAGS_BLUE = [
        [1, 0, 30, 52, 0],
        [2, 0, 294, 52, 0],
        [3, 39, 114, 12, 0],
        [4, 39, 162, 12, 0],
        [5, 39, 210, 12, 0],
        [6, 300, 226, 17.5, 180],
        [7, 300, 254, 17.5, 180],
        [8, 310, 264, 17.5, 90],
        [9, 338, 264, 17.5, 90],
        [10, 310, 216, 17.5, 270],
        [11, 338, 216, 17.5, 270],
        [12, 348, 226, 17.5, 0],
        [13, 348, 254, 17.5, 0]
    ];

// Mounting location of each tag, as the Game Manual's §3.7 table names it.
const TAG_WHERE = ["BLUE OUTFITTER chute", "BLUE OUTFITTER chute", "BLUE HEADWALL lane 1", "BLUE HEADWALL lane 2",
        "BLUE HEADWALL lane 3", "BLUE CRAG SHELF FACE", "BLUE CRAG SHELF FACE", "BLUE CRAG +Y SOCKET FACE",
        "BLUE CRAG +Y SOCKET FACE", "BLUE CRAG -Y SOCKET FACE", "BLUE CRAG -Y SOCKET FACE", "BLUE CRAG PEG FACE",
        "BLUE CRAG PEG FACE", "RED OUTFITTER chute", "RED OUTFITTER chute", "RED HEADWALL lane 1", "RED HEADWALL lane 2",
        "RED HEADWALL lane 3", "RED CRAG SHELF FACE", "RED CRAG SHELF FACE", "RED CRAG -Y SOCKET FACE",
        "RED CRAG -Y SOCKET FACE", "RED CRAG +Y SOCKET FACE", "RED CRAG +Y SOCKET FACE", "RED CRAG PEG FACE",
        "RED CRAG PEG FACE"];

// 36h11 codes for IDs 1..26 (AprilRobotics tag36h11.c, as decimal) and the bit layout.
const TAG36H11 = [59498712231, 59133511713, 60527243497, 64308969905, 65542086003, 1570935333, 4570528323,
        9189644189, 9115345212, 13936729254, 17036128504, 18952582164, 18753773744, 19969498994, 21877611414,
        25427209038, 28093235948, 29808535122, 32336336285, 36431974697, 36184565189, 37418301711, 41967662609,
        43890307829, 47057427331, 48748314607];
const TAG_BIT_X = [1, 2, 3, 4, 5, 2, 3, 4, 3, 6, 6, 6, 6, 6, 5, 5, 5, 4, 6, 5, 4, 3, 2, 5, 4, 3, 4, 1, 1, 1, 1, 1, 2, 2, 2, 3];
const TAG_BIT_Y = [1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 3, 4, 5, 2, 3, 4, 3, 6, 6, 6, 6, 6, 5, 5, 5, 4, 6, 5, 4, 3, 2, 5, 4, 3, 4];

// The 26-tag table in world coordinates: Blue as published, Red by rotation.
function tagTable()
{
    var out = [];
    for (var t in TAGS_BLUE)
    {
        out = append(out, t);
    }
    for (var t in TAGS_BLUE)
    {
        const p = rot180([t[1], t[2], t[3]]);
        var yaw = t[4] + 180;
        if (yaw >= 360)
        {
            yaw = yaw - 360;
        }
        out = append(out, [t[0] + 13, p[0], p[1], p[2], yaw]);
    }
    return out;
}

// [row, col] cells of the 10 x 10 target that are black for tag `tid`.
function tagBlackCells(tid)
{
    const code = TAG36H11[tid - 1];
    var white = [];
    var p = 1;
    for (var i = 0; i < 35; i += 1)
    {
        p = p * 2;
    }
    for (var i = 0; i < 36; i += 1)
    {
        const bit = floor(code / p) - 2 * floor(code / (2 * p));
        if (bit == 1)
        {
            white = append(white, [TAG_BIT_Y[i] + 1, TAG_BIT_X[i] + 1]);
        }
        p = p / 2;
    }
    var black = [];
    for (var r = 1; r < 9; r += 1)
    {
        for (var c = 1; c < 9; c += 1)
        {
            var isWhite = false;
            for (var wc in white)
            {
                if (wc[0] == r && wc[1] == c)
                {
                    isWhite = true;
                }
            }
            if (!isWhite)
            {
                black = append(black, [r, c]);
            }
        }
    }
    return black;
}

function tagFrame(t)
{
    return frameMake([t[1], t[2], t[3]], [cosd(t[4]), sind(t[4]), 0], [0, 0, 1]);
}

function buildTags(context is Context, id is Id, opts)
{
    const hp = TAG_PANEL / 2;
    for (var t in tagTable())
    {
        const F = tagFrame(t);
        const tid = id + nm("tag", t[0]);
        mkBox(context, tid, F, [-TAG_PANEL_T, -hp, -hp], [0, hp, hp]);
        paint(context, [tid], msg(["AprilTag ", t[0], " - ", TAG_WHERE[t[0] - 1]]), "neutral-white", 1, "tag");
        if (opts["decals"])
        {
            tagDecal(context, id + nm("decal", t[0]), [tid], F, [[0, 0, 0], [1, 0, 0], [0, 1, 0]], tagBlackCells(t[0]), 10, TAG_CELL, PAL["tag-black"]);
        }
    }
}

// ---------------------------------------------------------------- src/45_pieces.fs

// =====================================================================================
// SUPPLIES — FIELD-CAD-PACKAGE §6 and §9.  CACHE CRATE, O2 CELL, ROPE COIL; 21 of each.
// One master of each type is modelled at the world origin, copied to every staged pose,
// then deleted.  Each master's density is set from its published weight and its modelled
// volume, so every copy weighs exactly 2.0 / 1.5 / 1.0 lb.  Part-code dialect.
// =====================================================================================

// Local frames: CACHE CRATE centred on the origin; O2 CELL centred, axis along +x;
// ROPE COIL centred, axis along +z.

// O2 CELL revolve profile and the points used to colour its faces.
function cellGeometry()
{
    const rb = CELL_D / 2;
    const hl = CELL_L / 2;
    const rd = (CELL_DOME * CELL_DOME + rb * rb) / (2 * CELL_DOME);   // dome radius, 2.8333
    const vc = hl - rd;                                                 // dome centre, 4.1667
    const rf = CELL_FILLET;
    const uf = rb - rf;                                                 // fillet centre u
    const vf = vc + sqrt((rd - rf) * (rd - rf) - uf * uf);              // fillet centre v, 5.2208
    const eu = uf / (rd - rf);
    const ev = (vf - vc) / (rd - rf);
    const td = [rd * eu, vc + rd * ev];                                 // fillet / dome tangent point
    const bl = sqrt((1 + eu) * (1 + eu) + ev * ev);
    const fm = [uf + rf * (1 + eu) / bl, vf + rf * ev / bl];            // fillet arc midpoint
    const dl = sqrt(eu * eu + (ev + 1) * (ev + 1));
    const dm = [rd * eu / dl, vc + rd * (ev + 1) / dl];                 // dome arc midpoint
    const loop = [["A", [0, -hl], [dm[0], -dm[1]], [td[0], -td[1]]],
            ["A", [td[0], -td[1]], [fm[0], -fm[1]], [rb, -vf]],
            ["L", [rb, -vf], [rb, vf]],
            ["A", [rb, vf], fm, td],
            ["A", td, dm, [0, hl]],
            ["L", [0, hl], [0, -hl]]];
    return { "loop" : loop, "body" : [0, rb, 0], "fillet" : [[fm[1], fm[0], 0], [-fm[1], fm[0], 0]],
            "cap" : [[dm[1], dm[0], 0], [-dm[1], dm[0], 0]], "fullDiameterLength" : 2 * vf };
}

// Build one SUPPLY of `kind` ("crate", "cell", "coil") in frame F, fully styled.
function buildPiece(context is Context, id is Id, kind, F)
{
    if (kind == "crate")
    {
        const hc = CRATE_S / 2;
        mkPillowBox(context, id, F, hc, CRATE_CROWN);
        var ep = [];
        for (var a in [-hc, hc])
        {
            for (var b in [-hc, hc])
            {
                ep = concatenateArrays([ep, [[a, 0, b], [0, a, b], [a, b, 0]]]);
            }
        }
        softFilletAt(context, id + "edges", [id], F, ep, CRATE_FILLET, "CACHE CRATE edge fillets");
        paint(context, [id], "CACHE CRATE", "crate-violet", 1, "plywood");
        massBody(context, [id], "Ripstop nylon over PU foam (CACHE CRATE, effective)", CRATE_LB);
    }
    else if (kind == "cell")
    {
        const g = cellGeometry();
        mkRevolve(context, id, F, plAxis([0, 0, 0], [1, 0, 0], [0, 1, 0]), g["loop"]);
        paint(context, [id], "O2 CELL", "cell-body", 1, "plywood");
        styleFacesAt(context, [id], F, g["cap"], PAL["cell-cap"], 1);
        styleFacesAt(context, [id], F, g["fillet"], PAL["cell-fillet"], 1);
        massBody(context, [id], "Rigid core, EVA sleeve, molded caps (O2 CELL, effective)", CELL_LB);
    }
    else
    {
        const rt = COIL_TUBE / 2;
        mkRevolve(context, id, F, plAxis([0, 0, 0], [0, 0, 1], [1, 0, 0]), [["C", [COIL_OD / 2 - rt, 0], rt]]);
        paint(context, [id], "ROPE COIL", "coil-amber", 1, "plywood");
        massBody(context, [id], "Molded rubber/foam (ROPE COIL, effective)", COIL_LB);
    }
}

function pieceLabel(kind)
{
    if (kind == "crate")
    {
        return "CACHE CRATE";
    }
    if (kind == "cell")
    {
        return "O2 CELL";
    }
    return "ROPE COIL";
}

// Height of the piece frame origin above the surface it rests on.
function restHeight(kind)
{
    if (kind == "crate")
    {
        return CRATE_S / 2 + CRATE_CROWN;
    }
    if (kind == "cell")
    {
        return CELL_D / 2;
    }
    return COIL_TUBE / 2;
}

// Pose [x, y, z-of-surface] -> frame for a resting piece (crates square to the axes,
// cells lying with the axis along +X, coils flat).
function restFrame(kind, x, y, zs)
{
    return frameMake([x, y, zs + restHeight(kind)], [1, 0, 0], [0, 0, 1]);
}

// Two pieces of one type on one alliance staging mark.
function pairOffsets(kind, opts)
{
    if (opts["pairs"] == "STACKED")
    {
        return [[0, 0, 0], [0, 0, 2 * restHeight(kind)]];
    }
    if (kind == "crate")
    {
        return [[-7, 0, 0], [7, 0, 0]];
    }
    if (kind == "cell")
    {
        return [[0, -3, 0], [0, 3, 0]];
    }
    return [[-5.5, 0, 0], [5.5, 0, 0]];
}

// All 63 staged poses: [kind, x, y, zSurface, label].
function supplyPoses(opts)
{
    var out = [];
    // CENTER CACHE — FIELD SETUP CHART (a), rows Y = 138 / 162 / 186, columns X = 300 / 324 / 348
    const latin = [["cell", "coil", "crate"], ["coil", "crate", "cell"], ["crate", "cell", "coil"]];
    for (var j = 0; j < 3; j += 1)
    {
        for (var i = 0; i < 3; i += 1)
        {
            const k = latin[j][i];
            out = append(out, [k, CACHE_X[i], CACHE_Y[j], TAPE_T, msg([pieceLabel(k), " - CENTER CACHE (", CACHE_X[i], ", ", CACHE_Y[j], ")"])]);
        }
    }
    // alliance staging marks — chart (b): Blue 108 crates, 162 cells, 216 coils; Red rotated
    const stageKinds = ["crate", "cell", "coil"];
    for (var isRed in [false, true])
    {
        for (var j = 0; j < 3; j += 1)
        {
            const k = stageKinds[j];
            const offs = pairOffsets(k, opts);
            for (var n = 0; n < 2; n += 1)
            {
                var p = [STAGE_X + offs[n][0], STAGE_Y[j] + offs[n][1], TAPE_T + offs[n][2]];
                if (isRed)
                {
                    p = rot180(p);
                }
                out = append(out, [k, p[0], p[1], p[2], msg([pieceLabel(k), " - ", allianceName(isRed), " staging mark #", n + 1])]);
            }
        }
    }
    // OUTFITTER stock — 7 of each type per alliance, split between the two chutes (ref)
    const stock = [[["crate", -54, [-21, -7, 7, 21]], ["cell", -72, [-7, 0, 7]], ["coil", -88, [-16.5, -5.5, 5.5, 16.5]]],
            [["crate", -54, [-14, 0, 14]], ["cell", -72, [-10.5, -3.5, 3.5, 10.5]], ["coil", -88, [-11, 0, 11]]]];
    for (var isRed in [false, true])
    {
        for (var ci = 0; ci < 2; ci += 1)
        {
            for (var row in stock[ci])
            {
                var n = 0;
                for (var dy in row[2])
                {
                    n += 1;
                    var p = [row[1], CHUTE_Y[ci] + dy, 0];
                    if (isRed)
                    {
                        p = rot180(p);
                    }
                    out = append(out, [row[0], p[0], p[1], p[2], msg([pieceLabel(row[0]), " - ", allianceName(isRed), " OUTFITTER ", ci + 1, " stock #", n])]);
                }
            }
        }
    }
    return out;
}

function buildSupplies(context is Context, id is Id, opts)
{
    const W = worldFrame();
    const kinds = ["crate", "cell", "coil"];
    for (var k in kinds)
    {
        buildPiece(context, id + nm("master", k), k, W);
    }
    var i = 0;
    for (var p in supplyPoses(opts))
    {
        const isStock = p[3] == 0;
        if ((isStock && opts["stock"]) || (!isStock && opts["staged"]))
        {
            i += 1;
            const pid = id + nm("piece", i);
            copyBody(context, pid, [id + nm("master", p[0])], restFrame(p[0], p[1], p[2], p[3]));
            nameBody(context, [pid], p[4]);
        }
    }
    for (var k in kinds)
    {
        bDelete(context, id + nm("drop", k), [id + nm("master", k)]);
    }
}

// ---------------------------------------------------------------- src/48_main.fs

// =====================================================================================
// MAIN — buildField and the dimension self-check.  Part-code dialect.
//
// selfCheck measures the geometry that was just built (bounding boxes in local frames,
// point-to-body distances) and compares it with the CRITICAL values of the master
// dimension ledger.  It runs inside Onshape (feature option "Run dimension self-check")
// and, identically, in verify/run.py against the OpenCascade twin of the kernel.
// =====================================================================================

function buildField(context is Context, id is Id, opts)
{
    if (opts["perimeter"])
    {
        buildCarpet(context, id + "carpet");
        buildGuardrail(context, id + "rail0", 0, opts);
        buildGuardrail(context, id + "rail1", 1, opts);
    }
    if (opts["walls"])
    {
        buildAllianceWall(context, id + "wallBlue", false);
        buildAllianceWall(context, id + "wallRed", true);
    }
    if (opts["crags"])
    {
        buildCrag(context, id + "cragBlue", false, opts);
        buildCrag(context, id + "cragRed", true, opts);
    }
    if (opts["headwalls"])
    {
        buildHeadwall(context, id + "hwBlue", false);
        buildHeadwall(context, id + "hwRed", true);
    }
    if (opts["tape"])
    {
        buildTape(context, id + "tape");
    }
    if (opts["tags"])
    {
        buildTags(context, id + "tags", opts);
    }
    if (opts["staged"] || opts["stock"])
    {
        buildSupplies(context, id + "supplies", opts);
    }
}

// ---- check helpers: every check is [label, measured, expected, tolerance] ----------------

function ck(checks, label, got, want, tol)
{
    return append(checks, [label, got, want, tol]);
}

// Six bounding-box values against six expected values.
function ckBox(checks, label, got, want, tol)
{
    const axes = ["xmin", "ymin", "zmin", "xmax", "ymax", "zmax"];
    var out = checks;
    for (var i = 0; i < 6; i += 1)
    {
        if (want[i] != undefined)
        {
            out = ck(out, msg([label, " ", axes[i]]), got[i], want[i], tol);
        }
    }
    return out;
}

function failures(checks)
{
    var out = [];
    for (var c in checks)
    {
        if (abs(c[1] - c[2]) > c[3])
        {
            out = append(out, msg([c[0], ": measured ", c[1], ", expected ", c[2], " +/- ", c[3]]));
        }
    }
    return out;
}

// Frame for a tube whose mouth centre is r (crag-local), axis a (unit, toward the mouth).
function ckSocket(context is Context, checks, label, F, bodies, r, a, radial)
{
    const T = frameIn(F, r, radial, a);
    const ro = SOCK_ID / 2 + SOCK_WALL;
    var out = ckBox(checks, label, measureBox(context, bodies, T), [-ro, -ro, -SOCK_LEN, ro, ro, 0], 0.005);
    out = ck(out, msg([label, " bore radius at the rim"]), measureDistToPoint(context, bodies, F, r), SOCK_ID / 2, 0.005);
    return out;
}

function selfCheck(context is Context, id is Id, opts)
{
    var ch = [];
    const W = worldFrame();
    if (opts["perimeter"])
    {
        ch = ckBox(ch, "carpet", measureBox(context, [id + "carpet"], W), [0, 0, -CARPET_T, FIELD_L, FIELD_W, 0], 0.001);
        for (var r in ["rail0", "rail1"])
        {
            ch = ck(ch, msg([r, " top rail height"]), measureBox(context, [id + r + "top"], W)[5], GUARD_H, 0.001);
            const led = measureBox(context, [id + r + "ledA"], W);
            ch = ck(ch, msg([r, " FIELD LED lens centre"]), (led[2] + led[5]) / 2, LED_Z, 0.001);
        }
    }
    if (opts["walls"])
    {
        for (var isRed in [false, true])
        {
            const wid = id + nm("wall", sideTag(isRed));
            const F = allianceFrame(isRed);
            const wb = measureBox(context, [wid + "panel", wid + "glaze", wid + "frBot"], F);
            ch = ckBox(ch, msg([allianceName(isRed), " alliance wall"]), wb, [-WALL_T, 0, 0, 0, FIELD_W, WALL_H], 0.001);
            for (var c in CHUTE_Y)
            {
                const lab = msg([allianceName(isRed), " OUTFITTER chute at Y ", c]);
                const zc = CHUTE_SILL + CHUTE_H / 2;
                ch = ck(ch, msg([lab, " half height (sill 24, head 40)"]), measureDistToPoint(context, [wid + "panel", wid + "glaze"], F, [0, c, zc]), CHUTE_H / 2, 0.001);
                ch = ck(ch, msg([lab, " jamb at -15"]), measureDistToPoint(context, [wid + "panel"], F, [-0.2, c - CHUTE_W / 2 + 0.01, zc - 4]), 0.01, 0.001);
                ch = ck(ch, msg([lab, " jamb at +15"]), measureDistToPoint(context, [wid + "panel"], F, [-0.2, c + CHUTE_W / 2 - 0.01, zc - 4]), 0.01, 0.001);
            }
        }
    }
    if (opts["crags"])
    {
        for (var isRed in [false, true])
        {
            const cid = id + nm("crag", sideTag(isRed));
            const F = cragFrame(isRed);
            const A = msg([allianceName(isRed), " CRAG"]);
            const h = CRAG_S / 2;
            ch = ckBox(ch, msg([A, " tower"]), measureBox(context, [cid + "tower"], F), [-h, -h, 0, h, h, CRAG_H], 0.001);
            ch = ckBox(ch, msg([A, " spire + lantern"]), measureBox(context, [cid + "spire", cid + "lantern"], F),
                    [-SPIRE_S / 2, -SPIRE_S / 2, CRAG_H, SPIRE_S / 2, SPIRE_S / 2, SPIRE_TOP], 0.001);
            ch = ckBox(ch, msg([A, " SUMMIT BEACON lantern"]), measureBox(context, [cid + "lantern"], F), [undefined, undefined, LANTERN_LO, undefined, undefined, SPIRE_TOP], 0.001);
            for (var i = 0; i < 2; i += 1)
            {
                const grp = cid + nm("shelf", i + 1);
                const zt = SHELF_Z[i];
                ch = ckBox(ch, msg([A, " Shelf ", i + 1]), measureBox(context, [grp + "slab"], F), [h, -h, undefined, h + SHELF_DEPTH, h, zt], 0.001);
                for (var j = 0; j < size(FENCE_POS); j += 1)
                {
                    const fb = measureBox(context, [grp + nm("fence", j)], F);
                    ch = ckBox(ch, msg([A, " Shelf ", i + 1, " fence ", j]), fb, [undefined, -h + FENCE_POS[j], zt, undefined, -h + FENCE_POS[j] + FENCE_W, zt + FENCE_H], 0.001);
                }
                for (var j = 0; j < 3; j += 1)
                {
                    const lo = measureBox(context, [grp + nm("fence", j)], F)[4];
                    const hi = measureBox(context, [grp + nm("fence", j + 1)], F)[1];
                    ch = ck(ch, msg([A, " Shelf ", i + 1, " slot ", j + 1, " width"]), hi - lo, SLOT_W, 0.001);
                    ch = ck(ch, msg([A, " Shelf ", i + 1, " slot ", j + 1, " centre"]), (hi + lo) / 2, SLOT_CTRS[j], 0.001);
                }
                for (var j = 0; j < size(GUSSET_Y); j += 1)
                {
                    const gb = measureBox(context, [grp + nm("gusset", j)], F);
                    var floorZ = 38;
                    if (i == 0)
                    {
                        floorZ = 19;
                    }
                    ch = ck(ch, msg([A, " Shelf ", i + 1, " gusset ", j, " above its floor (margin >= 0)"]), min(gb[2] - floorZ, 0), 0, 0.0001);
                }
            }
            const s30 = sind(SOCK_TILT);
            const c30 = cosd(SOCK_TILT);
            for (var sgn in [-1, 1])
            {
                const fk = (sgn + 1) / 2;
                ch = ckSocket(context, ch, msg([A, " Low Socket y", sgn]), F, [cid + nm("sockLow", fk)], [SOCK_LAT, sgn * (h + SOCK_STANDOFF), LOW_SOCK_Z], [0, sgn * s30, c30], [1, 0, 0]);
                ch = ckSocket(context, ch, msg([A, " Mid Socket y", sgn]), F, [cid + nm("sockMid", fk)], [-SOCK_LAT, sgn * (h + SOCK_STANDOFF), MID_SOCK_Z], [0, sgn * s30, c30], [1, 0, 0]);
                ch = ck(ch, msg([A, " Low Socket y", sgn, " lowest point"]), measureBox(context, [cid + nm("sockLow", fk)], F)[2], 22.268, 0.001);
            }
            ch = ckSocket(context, ch, msg([A, " Summit Socket"]), F, [cid + "sockSummit"], [h + SOCK_STANDOFF, 0, SUM_SOCK_Z], [sind(SUM_TILT), 0, cosd(SUM_TILT)], [0, 1, 0]);
            const mb = measureBox(context, [cid + "mastArm", cid + "mastPost"], F);
            ch = ck(ch, msg([A, " Summit mast base on the top plate"]), mb[2], CRAG_H, 0.001);
            ch = ck(ch, msg([A, " Summit mast base within 4.0 of the shelf-face edge"]), max(h - mb[0], 4) , 4, 0.0001);
            const u = [-cosd(PEG_ANG), 0, sind(PEG_ANG)];
            const pr = PEG_OD / 2;
            for (var zi = 0; zi < 2; zi += 1)
            {
                for (var sgn in [-1, 1])
                {
                    const lab = msg([A, " peg z", PEG_Z[zi], " y", sgn * PEG_LAT]);
                    const P = frameIn(F, [-h, sgn * PEG_LAT, PEG_Z[zi]], [0, 1, 0], u);
                    ch = ckBox(ch, lab, measureBox(context, [cid + nm(nm("peg", zi), (sgn + 1) / 2)], P), [-pr, -pr, -pr, pr, pr, PEG_EXP], 0.002);
                }
            }
            for (var sgn in [-1, 1])
            {
                const P = frameIn(F, [-SPIRE_S / 2, sgn * HPEG_LAT, HPEG_Z], [0, 1, 0], u);
                ch = ckBox(ch, msg([A, " High Peg y", sgn * HPEG_LAT]), measureBox(context, [cid + nm("pegHigh", (sgn + 1) / 2)], P), [-pr, -pr, -pr, pr, pr, PEG_EXP], 0.002);
            }
            ch = ckBox(ch, msg([A, " tier ring 30"]), measureBox(context, [cid + "ring30"], F), [-h, -h, RING_Z[0] - RING_W / 2, h, h, RING_Z[0] + RING_W / 2], 0.001);
            ch = ckBox(ch, msg([A, " tier ring 54"]), measureBox(context, [cid + "ring54"], F), [-h, -h, RING_Z[1] - RING_W / 2, h, h, RING_Z[1] + RING_W / 2], 0.001);
            ch = ckBox(ch, msg([A, " tier ring 78"]), measureBox(context, [cid + "ring78"], F), [-SPIRE_S / 2, -SPIRE_S / 2, RING78_TOP - RING_W, SPIRE_S / 2, SPIRE_S / 2, RING78_TOP], 0.001);
            const d = cid + "depot";
            const lipOut = h + DEPOT_CH + DEPOT_LIP_T;
            ch = ckBox(ch, msg([A, " BASE DEPOT floor"]), measureBox(context, [d + "floor"], F), [h - DEPOT_WRAP, -h - DEPOT_CH, 0, h + DEPOT_CH, h + DEPOT_CH, DEPOT_FLOOR_T], 0.001);
            ch = ckBox(ch, msg([A, " BASE DEPOT lip"]), measureBox(context, [d + "lip"], F), [h - DEPOT_WRAP - DEPOT_LIP_T, -lipOut, 0, lipOut, lipOut, DEPOT_LIP_Z], 0.001);
            ch = ck(ch, msg([A, " BASE DEPOT channel depth (face to lip)"]), measureDistToPoint(context, [d + "lip"], F, [h, 0, 2]), DEPOT_CH, 0.001);
            ch = ck(ch, msg([A, " BASE DEPOT corner square / arm (16 from the corner, all three ways)"]), measureDistToPoint(context, [d + "lip"], F, [h, h, 2]), DEPOT_WRAP, 0.001);
        }
    }
    if (opts["headwalls"])
    {
        for (var isRed in [false, true])
        {
            const hid = id + nm("hw", sideTag(isRed));
            const F = allianceFrame(isRed);
            const A = msg([allianceName(isRed), " HEADWALL"]);
            const PF = frameIn(F, [HW_X, 0, 0], [cosd(HW_LEAN), 0, sind(HW_LEAN)], [-sind(HW_LEAN), 0, cosd(HW_LEAN)]);
            for (var li = 0; li < size(LANE_Y); li += 1)
            {
                const lid = hid + nm("lane", li + 1);
                for (var ri = 0; ri < size(RUNG_TOP); ri += 1)
                {
                    const zc = RUNG_TOP[ri] - RUNG_OD / 2;
                    const xc = HW_X - zc * tand(HW_LEAN);
                    const y0 = LANE_Y[li] + RUNG_STAGGER[ri] - RUNG_L / 2;
                    ch = ckBox(ch, msg([A, " lane ", li + 1, " rung ", ri]), measureBox(context, [lid + nm("rung", ri)], F),
                            [xc - RUNG_OD / 2, y0, zc - RUNG_OD / 2, xc + RUNG_OD / 2, y0 + RUNG_L, RUNG_TOP[ri]], 0.001);
                }
                var truss = [lid + "upright0", lid + "upright1", lid + "railBot", lid + "railTop", lid + "carrier0", lid + "carrier1", lid + "carrier2"];
                const tb = measureBox(context, truss, PF);
                ch = ck(ch, msg([A, " lane ", li + 1, " truss >= 4.0 behind plane P (margin)"]), min(-TRUSS_CLR - tb[3], 0), 0, 0.0001);
                const ub = measureBox(context, [lid + "upright0", lid + "upright1"], F);
                ch = ck(ch, msg([A, " lane ", li + 1, " uprights end at Z 84"]), ub[5], TRUSS_TOP, 0.001);
                ch = ck(ch, msg([A, " lane ", li + 1, " uprights stand on the carpet"]), ub[2], 0, 0.001);
            }
            const cb = measureBox(context, [hid + "crossbeam"], PF);
            ch = ck(ch, msg([A, " lower crossbeam >= 4.0 behind plane P (margin)"]), min(-TRUSS_CLR - cb[3], 0), 0, 0.0001);
        }
    }
    if (opts["tags"])
    {
        const hp = TAG_PANEL / 2;
        for (var t in tagTable())
        {
            ch = ckBox(ch, msg(["AprilTag ", t[0], " panel"]), measureBox(context, [id + "tags" + nm("tag", t[0])], tagFrame(t)), [-TAG_PANEL_T, -hp, -hp, 0, hp, hp], 0.001);
        }
    }
    if (opts["tape"])
    {
        for (var isRed in [false, true])
        {
            const ab = measureBox(context, [id + "tape" + msgId(isRed) + "apron"], cragFrame(isRed));
            ch = ckBox(ch, msg([allianceName(isRed), " CRAG APRON tape"]), ab, [-CRAG_S / 2 - 36, -CRAG_S / 2 - 20, 0, CRAG_S / 2 + 36, CRAG_S / 2 + 20, TAPE_T], 0.001);
        }
    }
    if (opts["staged"] && opts["stock"])
    {
        ch = ck(ch, "SUPPLY count", countBodies(context, [id + "supplies"]), 63, 0);
    }
    if (opts["staged"])
    {
        const pid = id + "supplies" + "piece1";
        const k0 = supplyPoses(opts)[0];
        ch = ckBox(ch, msg(["first SUPPLY (", k0[4], ")"]), measureBox(context, [pid], W),
                [k0[1] - CELL_L / 2, k0[2] - CELL_D / 2, k0[3], k0[1] + CELL_L / 2, k0[2] + CELL_D / 2, k0[3] + CELL_D], 0.002);
    }
    return ch;
}

function sideTag(isRed)
{
    if (isRed)
    {
        return "Red";
    }
    return "Blue";
}

function msgId(isRed)
{
    if (isRed)
    {
        return "red";
    }
    return "blue";
}

// ---------------------------------------------------------------- src/90_features.fs

// =====================================================================================
// FEATURES — what appears in the Onshape feature menu.
// =====================================================================================

export enum SpCragLighting
{
    annotation { "Name" : "Unlit" }
    UNLIT,
    annotation { "Name" : "Lit (all CAMPS established)" }
    LIT
}

export enum SpFieldLed
{
    annotation { "Name" : "Dark" }
    DARK,
    annotation { "Name" : "Green (FIELD safe)" }
    GREEN,
    annotation { "Name" : "White (FORECAST)" }
    FORECAST,
    annotation { "Name" : "Alliance colour (ROUTE)" }
    ROUTE
}

export enum SpStagingPairs
{
    annotation { "Name" : "Side by side" }
    SIDE_BY_SIDE,
    annotation { "Name" : "Stacked" }
    STACKED
}

export enum SpSupplyKind
{
    annotation { "Name" : "CACHE CRATE" }
    CACHE_CRATE,
    annotation { "Name" : "O2 CELL" }
    O2_CELL,
    annotation { "Name" : "ROPE COIL" }
    ROPE_COIL
}

function spOptions(definition is map) returns map
{
    var led = "DARK";
    if (definition.fieldLed == SpFieldLed.GREEN)
        led = "GREEN";
    else if (definition.fieldLed == SpFieldLed.FORECAST)
        led = "FORECAST";
    else if (definition.fieldLed == SpFieldLed.ROUTE)
        led = "ROUTE";
    return {
            "perimeter" : definition.perimeter,
            "walls" : definition.walls,
            "crags" : definition.crags,
            "headwalls" : definition.headwalls,
            "tape" : definition.tape,
            "tags" : definition.tags,
            "decals" : definition.tags && definition.decals,
            "staged" : definition.staged,
            "stock" : definition.stock,
            "lit" : definition.lighting == SpCragLighting.LIT,
            "fieldLed" : led,
            "pairs" : definition.pairs == SpStagingPairs.STACKED ? "STACKED" : "SIDE"
        };
}

annotation { "Feature Type Name" : "SUMMIT PUSH Field",
        "Feature Type Description" : "Builds the complete SUMMIT PUSH field (always-blue-origin NWU, inches) with names, colours, materials and densities." }
export const summitPushField = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Group Name" : "Build", "Collapsed By Default" : false }
        {
            annotation { "Name" : "Carpet, guardrails and FIELD LEDs", "Default" : true }
            definition.perimeter is boolean;
            annotation { "Name" : "Alliance walls, driver stations, OUTFITTERS", "Default" : true }
            definition.walls is boolean;
            annotation { "Name" : "CRAGS and BASE DEPOTS", "Default" : true }
            definition.crags is boolean;
            annotation { "Name" : "HEADWALLS", "Default" : true }
            definition.headwalls is boolean;
            annotation { "Name" : "Tape", "Default" : true }
            definition.tape is boolean;
            annotation { "Name" : "AprilTag panels", "Default" : true }
            definition.tags is boolean;
            annotation { "Name" : "36h11 decals on the AprilTag panels", "Default" : true }
            definition.decals is boolean;
            annotation { "Name" : "Staged SUPPLIES (CENTER CACHE and staging marks)", "Default" : true }
            definition.staged is boolean;
            annotation { "Name" : "OUTFITTER stock (behind the alliance walls)", "Default" : true }
            definition.stock is boolean;
        }
        annotation { "Group Name" : "Appearance", "Collapsed By Default" : false }
        {
            annotation { "Name" : "CRAG tier rings and SUMMIT BEACON", "Default" : SpCragLighting.UNLIT }
            definition.lighting is SpCragLighting;
            annotation { "Name" : "FIELD LED state", "Default" : SpFieldLed.DARK }
            definition.fieldLed is SpFieldLed;
            annotation { "Name" : "Pieces on each alliance staging mark", "Default" : SpStagingPairs.SIDE_BY_SIDE }
            definition.pairs is SpStagingPairs;
        }
        annotation { "Name" : "Run dimension self-check", "Default" : true }
        definition.selfCheck is boolean;
    }
    {
        const opts = spOptions(definition);
        buildField(context, id, opts);
        if (definition.selfCheck)
        {
            const checks = selfCheck(context, id, opts);
            const fails = failures(checks);
            if (size(fails) == 0)
            {
                reportFeatureInfo(context, id, "SUMMIT PUSH self-check: all " ~ size(checks) ~ " dimension checks pass");
            }
            else
            {
                for (var f in fails)
                {
                    println("SUMMIT PUSH self-check FAILED: " ~ f);
                }
                reportFeatureWarning(context, id, "SUMMIT PUSH self-check: " ~ size(fails) ~ " of " ~ size(checks) ~
                            " dimension checks failed (details in the FeatureScript console)");
            }
        }
    }, {
            "perimeter" : true,
            "walls" : true,
            "crags" : true,
            "headwalls" : true,
            "tape" : true,
            "tags" : true,
            "decals" : true,
            "staged" : true,
            "stock" : true,
            "lighting" : SpCragLighting.UNLIT,
            "fieldLed" : SpFieldLed.DARK,
            "pairs" : SpStagingPairs.SIDE_BY_SIDE,
            "selfCheck" : true
        });

annotation { "Feature Type Name" : "SUMMIT PUSH Game Piece",
        "Feature Type Description" : "One SUMMIT PUSH SUPPLY at the origin, with its official colour and weight." }
export const summitPushGamePiece = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "SUPPLY", "Default" : SpSupplyKind.CACHE_CRATE }
        definition.kind is SpSupplyKind;
        annotation { "Name" : "Rest on the Top plane", "Default" : true }
        definition.rest is boolean;
    }
    {
        var kind = "crate";
        if (definition.kind == SpSupplyKind.O2_CELL)
            kind = "cell";
        else if (definition.kind == SpSupplyKind.ROPE_COIL)
            kind = "coil";
        var F = worldFrame();
        if (definition.rest)
            F = restFrame(kind, 0, 0, 0);
        buildPiece(context, id + "piece", kind, F);
    }, {
            "kind" : SpSupplyKind.CACHE_CRATE,
            "rest" : true
        });
