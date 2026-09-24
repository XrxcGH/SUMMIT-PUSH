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
