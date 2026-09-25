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

// One-character strings of s ("AB" -> ["A", "B"]), for the pixel font.
function chars(s is string) returns array
{
    return splitIntoCharacters(s);
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
    // as std enclose.fs: evaluate the sheets before the enclose, delete them after
    const tools = qUnion(evaluateQuery(context, qUnion(sheets)));
    opEnclose(context, id + "ex", { "entities" : qUnion(sheets) });
    opDeleteBodies(context, id + "dl", { "entities" : tools });
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

// Delete every body of `bodies` smaller than minVolume (cubic inches) — the slivers a boolean
// can leave, which would otherwise show up as separate parts.
function removeSlivers(context is Context, id is Id, bodies is array, minVolume is number)
{
    var small = [];
    for (var b in evaluateQuery(context, kQ(bodies)))
    {
        if (evVolume(context, { "entities" : b }) < minVolume * inch ^ 3)
            small = append(small, b);
    }
    if (size(small) > 0)
        opDeleteBodies(context, id, { "entities" : qUnion(small) });
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
        kWarn(context, id, "reference roundover skipped - " ~ label);
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

// Give every part of `bodies` a unique name: parts that share a name get " 1", " 2", ... in
// creation order.  Call once, after every body has been named.
function numberSharedNames(context is Context, bodies is array)
{
    const parts = evaluateQuery(context, kQ(bodies));
    var names = [];
    var total = {};
    for (var p in parts)
    {
        const n = getProperty(context, { "entity" : p, "propertyType" : PropertyType.NAME });
        names = append(names, n);
        if (total[n] == undefined)
            total[n] = 0;
        total[n] += 1;
    }
    var seen = {};
    for (var i = 0; i < size(parts); i += 1)
    {
        const n = names[i];
        if (total[n] > 1)
        {
            if (seen[n] == undefined)
                seen[n] = 0;
            seen[n] += 1;
            setProperty(context, { "entities" : parts[i], "propertyType" : PropertyType.NAME, "value" : n ~ " " ~ seen[n] });
        }
    }
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
        kWarn(context, id, "AprilTag decal could not be applied; the panel is built without it");
    }
}

// ---------- warnings that reach the feature -------------------------------------------------
// Onshape shows only the top-level feature's status, so helpers append their warnings to it
// (id[0] is the feature's own id); summitPushField merges them with the self-check result.
function kWarn(context is Context, id is Id, message is string)
{
    const top = newId() + id[0];
    const prev = getFeatureWarning(context, top);
    var text = message;
    if (prev is string)
        text = prev ~ "; " ~ message;
    reportFeatureWarning(context, top, text);
}

// Equal-offset chamfer on the edges of `bodies` through the local points `pts`.
function chamferAt(context is Context, id is Id, bodies is array, F is CoordSystem, pts is array, d is number)
{
    var qs = [];
    for (var p in pts)
    {
        qs = append(qs, qContainsPoint(qOwnedByBody(kQ(bodies), EntityType.EDGE), kPt(F, p)));
    }
    opChamfer(context, id, { "entities" : qUnion(qs), "chamferType" : ChamferType.EQUAL_OFFSETS, "width" : d * inch, "tangentPropagation" : true });
}

function softChamferAt(context is Context, id is Id, bodies is array, F is CoordSystem, pts is array, d is number, label is string)
{
    try silent
    {
        chamferAt(context, id, bodies, F, pts, d);
    }
    catch (e)
    {
        kWarn(context, id, "decorative chamfer skipped - " ~ label);
    }
}

// Solid loft through planar profiles, in order.  Each profile is [pl, loop]: a local plane
// and one closed loop of segments on it (see kSketchLoops).
function mkLoft(context is Context, id is Id, F is CoordSystem, profiles is array)
{
    var regions = [];
    var sketches = [];
    for (var i = 0; i < size(profiles); i += 1)
    {
        const skId = id + ("sk" ~ i);
        const sk = newSketchOnPlane(context, skId, { "sketchPlane" : kPlane(F, profiles[i][0], 0) });
        kSketchLoops(sk, [profiles[i][1]]);
        skSolve(sk);
        regions = append(regions, qSketchRegion(skId, true));
        sketches = append(sketches, qCreatedBy(skId, EntityType.BODY));
    }
    opLoft(context, id + "lf", { "profileSubqueries" : regions, "bodyType" : ToolBodyType.SOLID });
    opDeleteBodies(context, id + "dl", { "entities" : qUnion(sketches) });
}

// Paint rectangles [u0, v0, u1, v1] onto the face(s) of `bodies` lying in plane pl (numbers,
// lettering, stripes).  The face is split, so the decal is exact and coplanar; rectangles
// must not overlap.  A failure leaves the face plain and warns.
function faceDecal(context is Context, id is Id, bodies is array, F is CoordSystem, pl is array, rects is array, rgb is array)
{
    const P = kPlane(F, pl, 0);
    const skId = id + "sk";
    try silent
    {
        const sk = newSketchOnPlane(context, skId, { "sketchPlane" : P });
        for (var i = 0; i < size(rects); i += 1)
        {
            const r = rects[i];
            skRectangle(sk, "r" ~ i, { "firstCorner" : k2([r[0], r[1]]), "secondCorner" : k2([r[2], r[3]]) });
        }
        skSolve(sk);
        opSplitFace(context, id + "sp", {
                    "faceTargets" : qCoincidesWithPlane(qOwnedByBody(kQ(bodies), EntityType.FACE), P),
                    "edgeTools" : qCreatedBy(skId, EntityType.EDGE)
                });
        opDeleteBodies(context, id + "dl", { "entities" : qCreatedBy(skId, EntityType.BODY) });
        var qs = [];
        for (var r in rects)
        {
            const c = [(r[0] + r[2]) / 2, (r[1] + r[3]) / 2];
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
        kWarn(context, id, "decal skipped");
    }
}

// Group bodies into one open composite part (the parts list shows one entry; the members
// stay selectable).  Call last: members must not be modified afterwards.
function groupParts(context is Context, id is Id, bodies is array, name is string)
{
    opCreateCompositePart(context, id, { "bodies" : kQ(bodies), "closed" : false });
    setProperty(context, { "entities" : qCompositePartTypeFilter(qCreatedBy(id, EntityType.BODY), CompositePartType.OPEN),
                "propertyType" : PropertyType.NAME, "value" : name });
}

// ---------- measurement (used by the dimension self-check) --------------------------------

// 1 if the (AprilTag) decal split the panel's face, else 0.
function decalApplied(context is Context, bodies is array) returns number
{
    return size(evaluateQuery(context, qOwnedByBody(kQ(bodies), EntityType.FACE))) > 6 ? 1 : 0;
}

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
