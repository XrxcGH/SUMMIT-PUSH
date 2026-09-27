// =====================================================================================
// SCREE (x18) — FIELD-CAD-PACKAGE §1.4.  Part-code dialect.
//
// Nine SCREE PATCHES per alliance on the open carpet round the staging marks.  A patch is a
// 30 x 30 square, sides parallel to the field axes, standing directly on the carpet: four
// half-round ridges (radius 1.75, so 1.75 tall and 3.5 wide at the base) on an 8.0 pitch,
// centerlines 4.0 and 12.0 either side of the patch center, each cut square at the patch
// boundary.  Blue is built from the ledger table; Red is the same table in the alliance frame.
// =====================================================================================

// Local frame of patch p: origin at its center on the carpet, x along the ridge normal, y along
// the ridges (p[3] degrees from +X), z up.
function screeFrame(isRed, p)
{
    return frameIn(allianceFrame(isRed), [p[1], p[2], 0], [sind(p[3]), -cosd(p[3]), 0], [0, 0, 1]);
}

function buildScree(context is Context, id is Id, isRed)
{
    const AF = allianceFrame(isRed);
    const A = allianceName(isRed);
    const r = SCREE_R;
    const hs = SCREE_S / 2;
    // each ridge is drawn one patch width either side of the center, which crosses the patch at any
    // offset and direction (the half-diagonal is 21.2), and then cut square at the patch boundary by
    // a frame that reaches 1.5 patch widths out, past every ridge end (at most 30.9 off at 45 degrees)
    const span = SCREE_S;
    const far = 1.5 * SCREE_S;
    for (var i = 0; i < size(SCREE_PATCHES); i += 1)
    {
        const p = SCREE_PATCHES[i];
        const pid = id + nm("S", i + 1);
        const PF = screeFrame(isRed, p);
        var ridges = [];
        for (var j = 0; j < size(SCREE_OFF); j += 1)
        {
            const d = SCREE_OFF[j];
            const rid = pid + nm("ridge", j + 1);
            // half-round section in the (x, z) plane of the patch frame, flat side on the carpet
            mkPrismProfile(context, rid, PF, plXZ(0), [[["L", [d - r, 0], [d + r, 0]], ["A", [d + r, 0], [d, r], [d - r, 0]]]], -span, span);
            ridges = append(ridges, rid);
        }
        // the carpet round the patch, as a tool: what it removes is the ridge beyond the boundary
        const cid = pid + "clip";
        prismXYHoles(context, cid, AF, rectPts(p[1] - far, p[2] - far, p[1] + far, p[2] + far),
                [rectPts(p[1] - hs, p[2] - hs, p[1] + hs, p[2] + hs)], -1, r + 1);
        bSubtract(context, pid + "cut", ridges, [cid], false);
        for (var j = 0; j < size(ridges); j += 1)
        {
            paint(context, [ridges[j]], msg([A, " SCREE PATCH ", p[0], " ridge ", j + 1]), "scree", 1, "hdpe");
        }
    }
}
