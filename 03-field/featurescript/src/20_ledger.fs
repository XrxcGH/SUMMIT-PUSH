// =====================================================================================
// LEDGER — every number the field is built from.  Sources: 03-field/FIELD-CAD-PACKAGE.md
// (§10 master dimension ledger and the per-element sections) and
// 03-field/MATERIALS-AND-COLORS.md.  Inches and degrees.  (ref) = reference geometry the
// package leaves free; the value here is this generator's choice.
// =====================================================================================

// ---- field (§0, §1) ---------------------------------------------------------------------
const FIELD_L = 648;
const FIELD_W = 324;
const FIELD_CX = 324;
const CARPET_T = 0.25;          // (ref) carpet thickness, below Z = 0
const TAPE_W = 2;
const TAPE_T = 0.01;
const CLIMB_DASH = 6;           // (ref) CLIMB LINE dash and gap outside BASECAMP

// ---- perimeter (§1.3) --------------------------------------------------------------------
const GUARD_H = 20;
const GUARD_RAIL_H = 2;         // (ref) 2 x 1 in tube: 2 tall, 1 deep
const GUARD_RAIL_D = 1;
const GUARD_POST_PITCH = 81;    // (ref) 8 bays
const GUARD_GLAZE_T = 0.25;
const LED_Z = 19;               // FIELD LED lens centre
const LED_W = 1;
const LED_DEPTH = 0.25;         // (ref) let into the top rail
const LED_BLOCKS = 3;           // lit blocks per alliance segment (manual §3.1.2)
const LED_GAP = 12;             // (ref) dark stretch after each block, so lit blocks read separately (R207)
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
const THROAT_T = 0.25;          // (ref) chute throat liner, carries the opening through the 2.0-in wall
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
const SOCK_LEN = 7;             // along the axis, rim plane to the floor a CELL seats on (DESIGN-SPEC §3:
                                // a seated 14.0 CELL stands 7.0 proud); the closed bottom lies beyond it
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
const FRONT_N = [-6, -4];       // front layer: rung carriers, rails
const BEAM_N = [-10, -8];       // (ref) lower crossbeam layer, set back so the tag wedges and panels sit in front
const UPRIGHT_INSET = 2.5;      // (ref) upright's inner face from the lane edge
const BRACKET_T = 0.25;
const BRACKET_FROM_END = 1;     // bracket plate 1.0-1.25 in from each rung end
const BRACKET_FRONT = 0.5;      // saddle plate reaches 0.5 in in front of plane P, 0.25 behind the rung front
const TAG_HW_X = 39;
const BEAM_Z = 12;

// ---- AprilTags (§7) ----------------------------------------------------------------------
const TAG_PANEL = 9;
const TAG_PANEL_T = 0.25;
const TAG_Z_OUT = 52;
const TAG_CELL = 0.8125;        // 8.125-in target / 10 cells = 6.5-in tag body / 8 cells

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
