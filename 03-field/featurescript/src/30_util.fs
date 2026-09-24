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
