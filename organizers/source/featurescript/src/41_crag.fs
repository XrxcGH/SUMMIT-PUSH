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

// Length of a socket tube along its axis, rim plane to the outer bottom face: the SOCK_LEN
// bore a CELL seats in, plus the closed bottom.
function sockOverall()
{
    return SOCK_LEN + SOCK_WALL;
}

// Open-topped tube with a closed bottom: outer bottom-face centre b, unit axis a (towards
// the mouth), unit radial r perpendicular to a.  Floor at SOCK_WALL, rim plane at
// sockOverall() along a, so the bore is SOCK_LEN deep.
function buildSocketTube(context is Context, id is Id, F, b, a, r)
{
    const ri = SOCK_ID / 2;
    const ro = ri + SOCK_WALL;
    const L = sockOverall();
    mkRevolve(context, id, F, plAxis(b, a, r),
            [["L", [0, 0], [ro, 0]], ["L", [ro, 0], [ro, L]], ["L", [ro, L], [ri, L]],
                ["L", [ri, L], [ri, SOCK_WALL]], ["L", [ri, SOCK_WALL], [0, SOCK_WALL]], ["L", [0, SOCK_WALL], [0, 0]]]);
}

// Peg with a hemispherical tip: root point p on the face, unit axis u, unit radial r.
// Modelled PEG_EMBED behind the root, then trimmed flush with the face by the box
// trim0..trim1 (on the structure side of the face).
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
    // (on the suppressible "cosmetics" layer, FIELD-CAD-PACKAGE §2.7 / §8: with cosmetics off the
    // faces stay flush and solid)
    const cosm = opts["cosmetics"];
    var r30 = [];
    var r54 = [];
    var r78 = [];
    if (cosm)
    {
        r30 = buildRing(context, id + "ring30", F, h, PEG_LAT, RING_Z[0] - RING_W / 2, RING_Z[0] + RING_W / 2);
        r54 = buildRing(context, id + "ring54", F, h, PEG_LAT, RING_Z[1] - RING_W / 2, RING_Z[1] + RING_W / 2);
        r78 = buildRing(context, id + "ring78", F, sh, HPEG_LAT, RING78_TOP - RING_W, RING78_TOP);
    }

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
    if (cosm)
    {
        paintRGB(context, r30, msg([cn, " tier ring 30"]), ringRGB, 1, "acrylic");
        paintRGB(context, r54, msg([cn, " tier ring 54"]), ringRGB, 1, "acrylic");
        paintRGB(context, r78, msg([cn, " tier ring 78"]), ringRGB, 1, "acrylic");
    }
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
        var side = "guardrail side";
        if (sgn > 0)
        {
            side = "center side";
        }
        const socks = [[SOCK_LAT, LOW_SOCK_Z, "Low"], [-SOCK_LAT, MID_SOCK_Z, "Mid"]];
        for (var q in socks)
        {
            const lat = q[0];
            const zr = q[1];
            const tid = id + nm(nm("sock", q[2]), fk);
            const a = [0, sgn * s30, c30];
            const yb = sgn * (h + SOCK_STANDOFF - sockOverall() * s30);
            const zbt = zr - sockOverall() * c30;
            buildSocketTube(context, tid, F, [lat, yb, zbt], a, [1, 0, 0]);
            paint(context, [tid], msg([cn, " ", q[2], " Socket (", side, ")"]), "socket", 1, "aluminum");
            // bracket plate in the wedge under the tube, top edge 1.0 in below the rim height
            const dy = yb - sgn * ro * c30;
            const dz = zbt + ro * s30;
            const ztop = zr - 1;
            const cy = dy + sgn * (ztop - dz) / c30 * s30;
            const az = dz + (sgn * (dy - sgn * h)) / c30 * s30;
            const bid = id + nm(nm("brk", q[2]), fk);
            prismYZ(context, bid, F, [[sgn * h, az], [dy, dz], [cy, ztop], [sgn * h, ztop]], lat - SOCK_BRACKET_T / 2, lat + SOCK_BRACKET_T / 2);
            paint(context, [bid], msg([cn, " ", q[2], " Socket bracket (", side, ")"]), "crag-accent", 1, "aluminum");
        }
    }

    // ---- Summit Socket (SHELF FACE, rim 72, 15 degrees) and its mast ----------------
    const s15 = sind(SUM_TILT);
    const c15 = cosd(SUM_TILT);
    const sbx = h + SOCK_STANDOFF - sockOverall() * s15;
    const sbz = SUM_SOCK_Z - sockOverall() * c15;
    buildSocketTube(context, id + "sockSummit", F, [sbx, 0, sbz], [s15, 0, c15], [0, 1, 0]);
    paint(context, [id + "sockSummit"], msg([cn, " Summit Socket"]), "socket", 1, "aluminum");
    // mast (§2.4): an arm on the top plate from 4.0 in inside the shelf-face edge, then a post
    // leaning out 15 degrees on the tube's own axis to the closed bottom, square to its face
    const mh = MAST_S / 2;
    const zArm = CRAG_H + MAST_S;
    const pHi = [sbx + mh * c15, sbz - mh * s15];            // post corners on the tube's bottom face
    const pLo = [sbx - mh * c15, sbz + mh * s15];
    const xHi = pHi[0] - (pHi[1] - zArm) * s15 / c15;       // ... and where their edges meet the arm top
    const xLo = pLo[0] - (pLo[1] - zArm) * s15 / c15;
    mkBox(context, id + "mastArm", F, [MAST_BASE_X, -mh, CRAG_H], [xHi, mh, zArm]);
    prismXZ(context, id + "mastPost", F, [[xLo, zArm], [xHi, zArm], pHi, pLo], -mh, mh);
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
    const pegSide = [" (guardrail side)", " (center side)"];
    for (var k = 0; k < 2; k += 1)
    {
        paint(context, [pegs[k]], msg([cn, " Low Peg", pegSide[k]]), "rung", 1, "steel");
        paint(context, [pegs[k + 2]], msg([cn, " Mid Peg", pegSide[k]]), "rung", 1, "steel");
    }
    var hpegs = [];
    for (var sgn in [-1, 1])
    {
        const y = sgn * HPEG_LAT;
        const pid = id + nm("pegHigh", (sgn + 1) / 2);
        buildPeg(context, pid, F, [-sh, y, HPEG_Z], u, [0, 1, 0], [-sh, y - 3, HPEG_Z - 4], [-sh + 4, y + 3, HPEG_Z + 4]);
        hpegs = append(hpegs, pid);
    }
    for (var k = 0; k < 2; k += 1)
    {
        paint(context, [hpegs[k]], msg([cn, " High Peg", pegSide[k]]), "rung", 1, "steel");
    }

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
