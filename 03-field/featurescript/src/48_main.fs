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
