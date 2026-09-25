# SUMMIT PUSH — AprilTag & Vision Integration Guide

*Part of the SUMMIT PUSH game package. This guide is subordinate to the Game Manual and the Field CAD Package; where any number here appears to conflict with either, that document governs.*

This document defines the complete AprilTag layout for the SUMMIT PUSH field (**26 tags, tag family 36h11**): tag-center coordinates, facing directions, panel geometry and placement, and the machine-readable `apriltag-field-layout.json`. It also gives software integration guidance for WPILib, PhotonVision, and Limelight, covering MultiTag pose estimation, auto-align transforms for CRAG scoring, FORECAST game-data handling, and simulation.

---

## 1. Tag Standard

| Property | Value |
|---|---|
| Tag family | **36h11** (the WPILib-standard family) |
| Tag body (black square, outer edge of black border) | **6.5 in** (0.1651 m) |
| Target (tag body + required white border) | **8.125 in** square |
| Mounting panel | **9.0 in** square |
| Tag count | **26** (IDs 1–26) |

> *Commentary:* The "tag size" parameter that vision software asks for (PhotonVision, Limelight, WPILib `AprilTagDetector`) is the **black square edge length: 6.5 in = 0.1651 m**. Entering the 8.125-in target size or the 9.0-in panel size corrupts every distance estimate. If measured distances run consistently long, check this first.

### 1.1 Tag geometry in the CAD model

- Each tag is modeled in the field CAD model as a **9.0-in square panel part** carrying a **per-ID decal face**: the 6.5-in black square centered inside its required **8.125-in** white border. The decal is modeled flat and coplanar with the panel face, so the corner geometry that pose estimation depends on is exact by construction.
- The full **8.125-in white border** must stay unobstructed in the model: no adjacent field geometry may overlap or encroach on the white region as seen from the field side. Verify with an interference/clearance check.
- Decal artwork for IDs 1–26 follows the standard WPILib 36h11 set (tag ID *N* uses the standard 36h11 pattern for ID *N*).
- The layout JSON (§4) is the machine-readable form of the same geometry and **drives all simulation**. Validate pipelines in PhotonVision or WPILib simulation against `apriltag-field-layout.json` (§6.8), not against a hand-measured layout.

### 1.2 Field mounting specification

- Each tag is centered on its **9.0-in panel**. The panel is fastened flush to the field structure with its face in the plane specified in §3 (fasteners outside the 8.125-in target).
- **Tag center height (Z)** is measured from the carpet to the center of the 6.5-in black square.
- Tags are mounted **plumb** (tag plane vertical, ±1°) and **square** to their stated facing direction (±1°). Every tag on the field is plumb, so every rotation in the layout file is a pure yaw.
- Field build tolerance on tag centers: **±0.25 in** in position, except CRAG tag panel height, which is held to **±0.15 in** (§1.3). The CAD model has no such allowance: the model and `apriltag-field-layout.json` must agree **exactly**, because MultiTag pose estimation is only as good as the layout's agreement with the JSON.
- CRAG tags sit at a **17.5-in center height**, HEADWALL lane tags at **12 in**, and OUTFITTER tags at **52 in** on the alliance wall above each chute.

### 1.3 CRAG tag height and occlusion

The CRAG tag height is set by occlusion. A 9.0-in panel centered at 17.5 in spans Z 13.00–22.00, and its 8.125-in target spans Z 13.44–21.56.

| Potential obstruction | Extent | Result |
|---|---|---|
| CACHE CRATE standing in the BASE DEPOT | crowned apex at Z = **13.25** (tray floor 0.25 + 0.5 bottom crown + 12.0 cube + 0.5 top crown) | **0.19 in** below the target; clear, with the CRAG panel height held to ±0.15 in (below) |
| ROPE COIL on edge in the BASE DEPOT | top at Z = 10.25 | 3.19 in below the target; clear |
| O2 CELL lying in the BASE DEPOT | top at Z = 5.25 | clear |
| **O2 CELL stood on end in the BASE DEPOT** | **top at Z = 14.25** | **0.81 in into the target band; the only case that is not clear (see below)** |
| Underside of Shelf 1 | Z = 23.25 | 1.25 in above the panel; clear |
| Low Socket tube, lowest point | Z = 22.19, the tube spanning 1.56–10.89 in outboard of the face | 0.63 in above the target; clear from a camera 10–20 in high (item 3 below covers a higher camera) |
| ROPE COIL on a Low Peg | spans Z ≈ 26–36 | above the panel; clear |

At a 12-in center height, the SHELF FACE pair and the alliance-wall-side tag on each SOCKET FACE would be blocked by any CACHE CRATE standing in the BASE DEPOT, which is a routine game state. HEADWALL lane tags stay at 12 in because that band is clear of every rung and keeps the whole panel at least 4.4 in behind the climbing plane.

> **CACHE CRATE margin: 0.19 in, held by a ±0.15-in height tolerance.** The as-built BASE
> DEPOT tray floor sits 0.25 in above the carpet, so a crowned CRATE standing in the DEPOT
> reaches Z = 13.25 against a target bottom of 13.4375. That margin is smaller than the
> ±0.25-in position tolerance in §1.2, so the CRAG tag panels carry a tighter **height**
> tolerance of **±0.15 in**, checked at field setup alongside the socket bore. Even a panel
> built 0.25 in low would let a CRATE reach only the bottom of the target's white border: the
> black square, which is what a detector finds, starts 0.81 in above the target's bottom edge,
> so on that panel it still clears the CRATE by 0.75 in.
>
> The panel is not moved or shrunk instead. Raising a 9.0-in panel to a 17.75 center puts its
> top edge at 22.25, above the Low Socket tube's lowest point at 22.19. An 8.5-in panel at
> 17.75 would restore 0.44 in of margin, but it cuts the white surround outside the target
> from 0.4375 to 0.1875 in per side and changes a CRITICAL vision dimension and the tag layout.

**The upright-CELL case and the camera-height rule.** An O2 CELL is 14.0 in long, so a CELL stood on its end on the BASE DEPOT tray floor reaches Z = 14.25, 0.81 in above the bottom edge of a CRAG tag target. It is the only SUPPLY in the game that can. This affects four of each CRAG's eight tags (the two on the SHELF FACE and the alliance-wall-side tag on each SOCKET FACE), because those are the three faces the DEPOT tray runs along. The other four (both PEG FACE tags and the peg-face-side SOCKET FACE tag on each side) have no tray in front of them at any height.

Whether the bottom edge is hidden depends on where the camera is. The obstruction is not a point. An O2 CELL's caps are **1.5-in domes** on a 5.0-in body, blended by a **1.0-in fillet** at each junction, so a CELL standing against the face presents a convex surface rising from Z = 12.47 where it touches the face to its apex of Z = 14.25 at 2.5 in out. (The fillet lowers the shoulder from the 12.75 a bare dome would give, which makes the ranges below slightly more generous than an unfilleted part would allow.) The sight line from the camera to the target's bottom edge descends as it approaches the tag, and it grazes that surface **on the flank nearer the face** rather than at the apex. A rule written against the apex alone therefore understates the required camera height, by as much as 5 in at long range. The clearances below are solved against the whole dome:

| Camera height | Clears an upright CELL out to |
|---|---|
| below 13.5 in | never (the camera is below the target's bottom edge) |
| 15 in | 3 in |
| 16 in | 6 in |
| 18 in | 10 in |
| 20 in | 15 in |
| 24 in | 25 in |
| 30 in | 39 in |
| 36 in | 53 in |

For a quick check in the field, `h ≥ 13.44 + 0.81·D/2.5` is the apex-only form. Treat it as a **lower bound that is 1–5 in optimistic**, never as the requirement.

Four consequences follow, none of which changes the low-camera architecture of Section 5:

1. **Final approach is unaffected for a camera near the top of the recommended band.** At 20 in, the whole target is visible within 15 in, which covers close-range alignment only. The as-built tray floor stands every SUPPLY 0.25 in higher than the carpet, which costs about a third of every range in this table. Below about 16 in, a single camera sees the bottom edge clipped from almost any useful range whenever a CELL is stood on end in front of that face, so a design committed to one low camera should place it at **18 in or higher** and treat anything beyond about 10 in of range as localization only.
2. **Long range is already handled.** Section 5.2 treats long-range CRAG detections as localization input only, never as final-approach truth. That guidance exists for midfield traffic, and it covers this case as well.
3. **Never rely on a single CRAG tag.** Every face carries a pair, and MultiTag (§6.4) over both, or over one CRAG face plus a HEADWALL or OUTFITTER tag, degrades gracefully when one tag is partly hidden. The optional second camera at 24–36 in (§5.2) clears the upright CELL out to 25–53 in on its own, but from that height the Low Socket tube can hide part of the tag beneath it (tags 8, 10, 21 and 23), and most of it from close range. Use it alongside the primary camera, not instead of it, on those tags.
4. **Simulate it.** Add a 5 × 14 in occluder standing at the DEPOT in front of one SHELF FACE tag (§6.8) and confirm that the pose solution survives on the remaining tags.

A tag height that cleared an upright CELL outright would need its target bottom above 14.25 in (a center above 18.3 in), but a 9.0-in panel that high has its top edge above 22.8 in: above the Low Socket tube's lowest point at 22.19 in and within 0.5 in of the Shelf 1 underside at 23.25 in. At 17.5 in the panel clears both of those with margin, and it clears every SUPPLY except an O2 CELL balanced on its end.

---

## 2. Field Coordinate System

All coordinates in this guide and in `apriltag-field-layout.json` use the **always-blue-origin NWU** convention:

- **Origin:** the right corner of the **Blue** alliance wall, as seen from the Blue driver stations.
- **+X:** from the Blue wall toward the Red wall (field length, 648 in / 16.4592 m).
- **+Y:** to the left from the Blue driver stations' perspective (field width, 324 in / 8.2296 m).
- **+Z:** up from the carpet.
- **Yaw:** rotation about +Z, with **0° = facing +X** (toward the Red wall), measured counter-clockwise viewed from above. A tag's yaw is the direction its **face normal** points. A camera sees the tag head-on when it looks in the opposite direction.

There is **one canonical layout**. It is 180° rotationally symmetric about field center (324, 162): every Red tag *N* (14 ≤ N ≤ 26) is the 180° rotation of Blue tag *N − 13* about field center. Do **not** flip or re-origin the layout for the Red alliance. Keep the blue origin and transform *target* poses per current WPILib alliance-handling practice (see §6.1).

---

## 3. Tag Placement Table (26 tags)

Coordinates are **tag centers in inches**, field frame per §2. Yaw is the facing direction of the tag face (0° = +X).

### 3.1 Blue alliance tags (IDs 1–13)

| ID | Structure | Face / location | X (in) | Y (in) | Z (in) | Yaw (°) |
|---:|---|---|---:|---:|---:|---:|
| 1 | Blue OUTFITTER | Alliance wall, above the Y = 30 chute | 0 | 30 | 52 | 0 |
| 2 | Blue OUTFITTER | Alliance wall, above the Y = 294 chute | 0 | 294 | 52 | 0 |
| 3 | Blue HEADWALL | Lane 1 center, lower crossbeam | 39 | 114 | 12 | 0 |
| 4 | Blue HEADWALL | Lane 2 (center), lower crossbeam | 39 | 162 | 12 | 0 |
| 5 | Blue HEADWALL | Lane 3 center, lower crossbeam | 39 | 210 | 12 | 0 |
| 6 | Blue CRAG | SHELF FACE (−X face), −Y side of the face centerline | 300 | 226 | 17.5 | 180 |
| 7 | Blue CRAG | SHELF FACE (−X face), +Y side of the face centerline | 300 | 254 | 17.5 | 180 |
| 8 | Blue CRAG | +Y SOCKET FACE, alliance-wall side | 310 | 264 | 17.5 | 90 |
| 9 | Blue CRAG | +Y SOCKET FACE, peg-face side | 338 | 264 | 17.5 | 90 |
| 10 | Blue CRAG | −Y SOCKET FACE, alliance-wall side | 310 | 216 | 17.5 | 270 |
| 11 | Blue CRAG | −Y SOCKET FACE, peg-face side | 338 | 216 | 17.5 | 270 |
| 12 | Blue CRAG | PEG FACE (+X face), −Y side | 348 | 226 | 17.5 | 0 |
| 13 | Blue CRAG | PEG FACE (+X face), +Y side | 348 | 254 | 17.5 | 0 |

### 3.2 Red alliance tags (IDs 14–26)

| ID | Structure | Face / location | X (in) | Y (in) | Z (in) | Yaw (°) |
|---:|---|---|---:|---:|---:|---:|
| 14 | Red OUTFITTER | Alliance wall, above the Y = 294 chute | 648 | 294 | 52 | 180 |
| 15 | Red OUTFITTER | Alliance wall, above the Y = 30 chute | 648 | 30 | 52 | 180 |
| 16 | Red HEADWALL | Lane 1 center, lower crossbeam | 609 | 210 | 12 | 180 |
| 17 | Red HEADWALL | Lane 2 (center), lower crossbeam | 609 | 162 | 12 | 180 |
| 18 | Red HEADWALL | Lane 3 center, lower crossbeam | 609 | 114 | 12 | 180 |
| 19 | Red CRAG | SHELF FACE (+X face), +Y side of the face centerline | 348 | 98 | 17.5 | 0 |
| 20 | Red CRAG | SHELF FACE (+X face), −Y side of the face centerline | 348 | 70 | 17.5 | 0 |
| 21 | Red CRAG | −Y SOCKET FACE, alliance-wall side | 338 | 60 | 17.5 | 270 |
| 22 | Red CRAG | −Y SOCKET FACE, peg-face side | 310 | 60 | 17.5 | 270 |
| 23 | Red CRAG | +Y SOCKET FACE, alliance-wall side | 338 | 108 | 17.5 | 90 |
| 24 | Red CRAG | +Y SOCKET FACE, peg-face side | 310 | 108 | 17.5 | 90 |
| 25 | Red CRAG | PEG FACE (−X face), +Y side | 300 | 98 | 17.5 | 180 |
| 26 | Red CRAG | PEG FACE (−X face), −Y side | 300 | 70 | 17.5 | 180 |

> *Example:* A Blue robot auto-aligning an O2 CELL insertion on the Blue CRAG's −Y SOCKET FACE should expect tags **10** and **11** (yaw 270°, face normal −Y: the face pointing into the inter-CRAG corridor, toward field center). Tag 10 (X = 310) sits under the **Low Socket**; tag 11 (X = 338) sits under the **Mid Socket** (§6.6). Detecting tags 23/24 instead means the camera is looking at the **Red** CRAG; abort and re-localize.

### 3.3 Geometry derivation

The values above follow from the locked field geometry, and entrants reproducing the field in CAD from the drawing set can verify them:

- **CRAG faces.** Each CRAG has a 48 × 48 in footprint centered at (324, 240) Blue / (324, 84) Red, so each face plane lies **24 in** from the CRAG center. Blue faces: SHELF FACE at X = 300 (faces −X, toward the Blue wall → yaw 180), PEG FACE at X = 348 (yaw 0), SOCKET FACES at Y = 264 (yaw 90) and Y = 216 (yaw 270).
- **Two tags per face**, centers offset **±14 in** from the face centerline along the face, at **Z = 17.5 in**. On the shelf and peg faces the offsets are in Y (240 ± 14 = 226, 254); on the socket faces they are in X (324 ± 14 = 310, 338).
- **OUTFITTER tags** are centered directly above each chute (chute centers (0, 30) and (0, 294) Blue; mirrored Red), tag center at **Z = 52 in**, tag face in the alliance-wall plane (X = 0 Blue → yaw 0; X = 648 Red → yaw 180).
- **HEADWALL tags** are centered on each 48-in lane (Blue lane centers Y = 114, 162, 210) at **Z = 12 in**, mounted plumb on the truss lower crossbeam through a 15° wedge bracket, tag face plane **X = 39 (Blue) / X = 609 (Red)**. Plane P, the inclined climbing plane, is at X = 48 − Z·tan 15° for Blue, so a plumb panel at X = 39 clears P by 4.42 in (measured normal to P) at its top edge (Z = 16.5) and by 6.75 in at its bottom edge (Z = 7.5), satisfying the ≥ 4.0 in structure clearance in FIELD-CAD-PACKAGE §4.1. No part of the panel enters the climbing volume.
- **Red = rotated Blue.** Every Red tag pose is the Blue tag pose (ID − 13) mapped by (x, y, yaw) → (648 − x, 324 − y, yaw + 180°). This also serves as a model-verification check: measure the Blue tag poses in the CAD model, then check Red against the rotation.

---

## 4. The Layout File: `apriltag-field-layout.json`

The canonical machine-readable layout ships alongside this guide at `04-vision/apriltag-field-layout.json`. It uses the **WPILib AprilTagFieldLayout schema**:

```json
{
  "tags": [
    {
      "ID": 1,
      "pose": {
        "translation": { "x": 0.0, "y": 0.762, "z": 1.3208 },
        "rotation": {
          "quaternion": { "W": 1.0, "X": 0.0, "Y": 0.0, "Z": 0.0 }
        }
      }
    }
  ],
  "field": { "length": 16.4592, "width": 8.2296 }
}
```

- **Units are meters** (inches × 0.0254, exact). Field: length 16.4592 m (54 ft), width 8.2296 m (27 ft).
- **Rotations are quaternions.** Every SUMMIT PUSH tag is plumb, so all rotations are pure yaw: W = cos(yaw/2), Z = sin(yaw/2), X = Y = 0.

| Yaw | W | X | Y | Z |
|---:|---:|---:|---:|---:|
| 0° | 1.0 | 0.0 | 0.0 | 0.0 |
| 90° | 0.7071067811865476 | 0.0 | 0.0 | 0.7071067811865476 |
| 180° | 0.0 | 0.0 | 0.0 | 1.0 |
| 270° | −0.7071067811865476 | 0.0 | 0.0 | 0.7071067811865476 |

The JSON is generated from the inch table in §3, and the two **match exactly**.

---

## 5. Camera Selection and Mounting

### 5.1 Low tag heights

The eight tags on each CRAG are mounted at a **17.5-in center height** and the HEADWALL lane tags at **12 in**. Both heights are low, for three reasons:

1. **Clear of scoring geometry in every game state.** Nothing at those heights conflicts with shelves (24/42 in), socket rims (30/54/72 in), pegs (30/54/78 in), the DEPOT lip (4 in), or a crowned CACHE CRATE standing in the DEPOT (apex 13.25 in, clearing the target by 0.19 in). No SUPPLY in a scoring position occludes a tag, with one exception anywhere on the FIELD: an O2 CELL stood on its end in the BASE DEPOT, which §1.3 budgets and prices in camera height.
2. **Visible at point-blank range.** The final 12 in of an approach is where alignment matters most. A low tag stays inside a low camera's vertical field of view all the way to bumper contact; a high tag leaves the top of the frame just when it is needed.
3. **Minimal skew at close range.** A camera at roughly tag height views the tag face-on, which is the best case for corner extraction and single-tag pose stability.

### 5.2 Recommendations

- **Primary alignment camera:** mounted **10–20 in above the carpet**, facing forward through or beside the scoring mechanism, pitch within ±10° of level. This frames the CRAG tags (17.5 in) and the HEADWALL lane tags (12 in) from 10 ft down to bumper contact. If it is the ROBOT's only camera, put it at **18 in or higher** within that band; below about 16 in it cannot see over an O2 CELL stood on end in the DEPOT (§1.3).
- **Localization camera (optional second camera):** mounted higher (24–36 in) with a wide field of view, angled slightly down or level, for mid-field pose estimation off the OUTFITTER tags (52 in). Two cameras feeding one pose estimator is a common architecture on high-performing robots.
- **Occlusion budget:** midfield traffic in the corridor regularly blocks CRAG tags at long range. Autos should acquire the destination face's tag pair by roughly 6 ft out, and should treat long-range detections as localization input only, never as final-approach truth.
- Global-shutter cameras at ≥50 fps with exposure locked low are recommended; otherwise the white FORECAST LEDs, the alliance-color tier rings, and the SUMMIT BEACON drive auto-exposure into smear.

> *Commentary:* A common failure at offseason events is a single high-mounted camera that sees everything at range and nothing at the moment of scoring. The SUMMIT PUSH tag layout is designed for a low front camera, so a single-camera design should mount its camera low.

---

## 6. Software Integration

### 6.1 WPILib: loading the layout

Deploy `apriltag-field-layout.json` with the robot code and load it. The `AprilTagFieldLayout(Path)` constructor declares a checked `IOException`, so it must be caught or declared:

```java
import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.wpilibj.Filesystem;
import java.io.IOException;
import java.nio.file.Path;

public static AprilTagFieldLayout loadSummitPushLayout() {
  Path path = Filesystem.getDeployDirectory().toPath()
      .resolve("apriltag-field-layout.json");
  try {
    return new AprilTagFieldLayout(path);
  } catch (IOException e) {
    throw new RuntimeException("SUMMIT PUSH tag layout missing from deploy/", e);
  }
}
```

Place the file in `src/main/deploy/`. The layout already uses the always-blue-origin convention, so **do not call** `setOrigin(...)` **to flip it for Red**. Keep all robot poses blue-origin for the entire MATCH, and mirror *target/waypoint* poses for the Red alliance in code. The 180° rotational symmetry makes that a one-line transform about field center:

```java
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Translation2d;

private static final Translation2d FIELD_CENTER = new Translation2d(8.2296, 4.1148);

public static Pose2d mirrorForRed(Pose2d bluePose) {
  return new Pose2d(
      bluePose.getTranslation().rotateAround(FIELD_CENTER, Rotation2d.k180deg),
      bluePose.getRotation().rotateBy(Rotation2d.k180deg));
}
```

`Translation2d.rotateAround(Translation2d, Rotation2d)` is available in current WPILib; on an older release, subtract the center, rotate, and add it back. `fieldLayout.getTagPose(int id)` returns an `Optional<Pose3d>` for use in transform chains (§6.6); check `isPresent()` before unwrapping.

### 6.2 PhotonVision

1. Flash the coprocessor, connect the camera, and calibrate intrinsics **at the resolution that will run** (calibration is per-resolution).
2. Create an AprilTag pipeline: family **36h11**, tag size **0.1651 m** (6.5 in, the black square; see §1).
3. Upload the layout: *Settings → AprilTag Field Layout → Import*, and select `apriltag-field-layout.json`. This is required for MultiTag.
4. Enable **MultiTag** (Pipeline → 3D → MultiTag PNP on coprocessor).
5. On the robot side, use `PhotonPoseEstimator` with strategy `MULTI_TAG_PNP_ON_COPROCESSOR` (fallback `LOWEST_AMBIGUITY`), constructed with the same `AprilTagFieldLayout` object from §6.1 and the measured robot-to-camera `Transform3d`.
6. Feed the resulting `EstimatedRobotPose` into the drivetrain's pose estimator (`SwerveDrivePoseEstimator.addVisionMeasurement(...)`) with standard deviations scaled by tag count and distance.

### 6.3 Limelight

Limelight consumes field maps in its own `.fmap` format. Build the SUMMIT PUSH map once and share it across the alliance:

1. Open the Limelight **Map Builder** tool and import or enter the 26 tag poses (meters, blue-origin NWU, the same numbers as the JSON; current versions convert the WPILib JSON directly).
2. Set tag size **165.1 mm**, family 36h11.
3. Upload the resulting `.fmap` in the Limelight web UI (*Settings → Field Map Upload*).
4. Use the **MegaTag2** botpose (`botpose_orb_wpiblue`) for localization: seed it with gyro yaw via `SetRobotOrientation(...)` every loop, and read the blue-origin botpose regardless of alliance.

### 6.4 MultiTag pose estimation

The layout puts **two coplanar tags** in view for every high-value action:

- Each CRAG face carries a **tag pair 28 in apart** (centers ±14 in). At final-approach distances both tags are in frame, and a two-tag PNP solve on a known baseline is far better conditioned than a single-tag solve: the pair fixes the target plane's yaw, which is the degree of freedom a single planar tag resolves worst. Expect roughly 1 in and 1° of pose noise inside 5 ft with a calibrated camera. (A two-tag solve does not remove planar-target ambiguity in principle; at these baselines it constrains the solution enough that the wrong branch is rejected by reprojection error.)
- OUTFITTER and HEADWALL tags are single tags; treat them as localization beacons rather than precision references. During the ENDGAME approach, the HEADWALL tag confirms *which lane* the robot is entering (tags 3/4/5 Blue, 16/17/18 Red). Lane centering to ±2 in off a single HEADWALL tag at short range is realistic and sufficient, because the climb itself is a mechanical task.
- MultiTag across *structures* (a CRAG pair plus an OUTFITTER tag in a wide-FOV frame) is useful when it occurs, but a design should not depend on it.

> *Example:* In AUTO, a Blue robot heading for the CENTER CACHE localizes off tags 6/7 (Blue CRAG SHELF FACE) while driving up-field, corrects its pose estimate when both tags resolve at about 8 ft, and branches on the FORECAST (§6.7) to either the shelf approach (stay on 6/7) or a socket approach (transition to the 8/9 or 10/11 pair as it rounds the CRAG).

### 6.5 Which tags are whose

Score on the robot's **own** CRAG only: SUPPLIES SCORED on a CRAG count for that CRAG's alliance regardless of who placed them (Game Manual §4.4.2). Filter auto-align targeting to the alliance's own tag IDs:

| Alliance | OUTFITTER | HEADWALL | CRAG |
|---|---|---|---|
| Blue | 1, 2 | 3, 4, 5 | 6–13 |
| Red | 14, 15 | 16, 17, 18 | 19–26 |

Reject opponent-structure detections in targeting logic; they remain useful for localization.

### 6.6 Auto-align: tag → target transforms

For each CRAG face, express the goal pose as a fixed `Transform3d` from a tag (or the tag-pair midpoint) to the scoring feature, then chain: `goalPose = fieldLayout.getTagPose(id) ⊕ tagToTarget ⊖ robotToMechanism`.

Offsets below are given **from the tag-pair midpoint** of the face, the point on the face centerline at Z = 17.5 (for example, the Blue SHELF FACE midpoint is (300, 240, 17.5)). **"Lateral"** is along the face, positive toward the higher-numbered tag of the pair. **"Out"** is along the face's outward normal, positive away from the CRAG center; in a WPILib tag frame this is the +X component of the `tagToTarget` `Transform3d`. **"Up"** is ΔZ. In the HEADWALL table below, the offsets are to each rung's **centerline** (rung center Z = top − 0.75 for the 1.5-in OD rung), matching the derived rung positions in FIELD-CAD-PACKAGE §4.1, rather than to the rung top given in the row label.

**SHELF FACE** (tags 6/7 Blue; 19/20 Red; CACHE CRATES, flat placement):

| Feature | Lateral (in) | Out (in) | Up (in) | Notes |
|---|---:|---:|---:|---|
| Shelf 1 slot centers (top surface 24 in) | −15.5 / 0 / +15.5 | **+7.0** | +6.5 | four 1.5-in fences and three 14.0-in slots across the 48-in face put the outer centers at ±15.5, 1.5 in outboard of the tags |
| Shelf 2 slot centers (top surface 42 in) | −15.5 / 0 / +15.5 | **+7.0** | +24.5 | same lateral pattern |
| **Summit Socket rim center** (72 in) | 0 | **+8.0** | **+54.5** | on the CRAG centerline, 8.0 in outboard of the SHELF FACE plane; tube tilted 15° from vertical, tilting outward |

**SOCKET FACES** (tags 8/9 and 10/11 Blue; 21/22 and 23/24 Red; O2 CELLS, inserted from above). Each socket rim center is **directly above one tag of the pair, standing 8.0 in off the face plane**: the **Low Socket** (rim 30 in) above the alliance-wall-side tag (8, 10, 21, 23), and the **Mid Socket** (rim 54 in) above the peg-face-side tag (9, 11, 22, 24):

| Feature | Lateral from its tag (in) | Out (in) | Up from its tag (in) | Rim tilt |
|---|---:|---:|---:|---|
| Low Socket rim center | 0 | **+8.0** | +12.5 | tube 30° from vertical, tilting outward |
| Mid Socket rim center | 0 | **+8.0** | +36.5 | tube 30° from vertical, tilting outward |

The **8.0-in standoff is a locked CRITICAL dimension** (FIELD-CAD-PACKAGE §2.3) and must appear in the `tagToTarget` transform. Worked example: Blue tag 8 sits at (310, 264, 17.5); its Low Socket rim center is at **(310, 272, 30)**, not (310, 264, 30). The 6.50 ± 0.125 in ID gives 0.75 in of radial clearance per side around the 5.0-in CELL. That clearance is the insertion tolerance; it does not replace the standoff.

**PEG FACE** (tags 12/13 Blue; 25/26 Red; ROPE COILS on 1.5-in pegs angled 45° up). Peg roots lie in their mounting face:

| Feature | Lateral (in, from pair midpoint) | Out (in) | Up (in) | Notes |
|---|---:|---:|---:|---|
| Low Pegs ×2 (root 30 in) | ±14.0 | 0 | +12.5 | directly above the tags |
| Mid Pegs ×2 (root 54 in) | ±14.0 | 0 | +36.5 | directly above the tags |
| High Pegs ×2 (root 78 in) | ±7.0 | **−14.0** | +60.5 | on the spire, whose peg face is 14.0 in inboard of the tower's peg face |

A peg's tip is 7.07 in farther out and 7.07 in higher than its root (10.0 in exposed at 45°).

**HEADWALL** (tags 3/4/5 Blue; 16/17/18 Red; tag at lane center, Z = 12, on the plumb tag plane at X = 39 / 609). The truss leans 15° toward the alliance wall, so the rungs step **behind** the tag plane with height. These values are for approach planning only; the climb relies on superstructure sensing rather than vision.

| Rung | Behind the tag plane (in) | Up from the tag (in) | Lateral from lane center (in) |
|---|---:|---:|---:|
| LEDGE (top 30 in) | **−1.2** (i.e. 1.2 in *in front of* the tag plane) | +17.25 | **−12.0** |
| CAMP (top 54 in) | **+5.3** | +41.25 | **+12.0** |
| SUMMIT (top 78 in) | **+11.7** | +65.25 | **−12.0** |

The lateral column is the same in **every lane** (the stagger alternates by rung, never by lane; FIELD-CAD-PACKAGE §4.1), so one set of offsets serves all three lanes on both ALLIANCES, with +Y to the right of the lane center from the approaching ROBOT's point of view (the left as seen from that alliance's driver stations). Red is the 180° rotation about field center and carries the same signs relative to its own lane centers.

**OUTFITTER** (tags 1/2, 14/15; tag centered above the chute): the chute opening is 30 in wide × 16 in tall with its sill at 24 in, so its center sits **20 in directly below the tag center**. This is useful for auto-driving to the human-player feed station inside the OUTFITTER LANE.

> *Commentary:* Publish these transforms as constants rather than as numbers scattered through commands. One `FieldConstants` class holding the tag-pair midpoints and feature offsets, generated from the same geometry as the JSON, means that a revision of the field geometry is absorbed by retuning one file instead of every auto.

### 6.7 Reading the FORECAST (game data)

At T = 0 of AUTO, the FMS broadcasts the FORECAST as the game-specific message: **`"W"`** (WHITEOUT; PRIORITY SUPPLY: CACHE CRATES), **`"I"`** (ICEFALL; O2 CELLS), or **`"G"`** (GALE; ROPE COILS). The PRIORITY SUPPLY's AUTO placement points are doubled *and* ROPED UP requires two of it, so an auto that pursues ROPED UP must branch three ways:

```java
import edu.wpi.first.wpilibj.DriverStation;

public enum Forecast { WHITEOUT, ICEFALL, GALE, UNKNOWN }

public static Forecast getForecast() {
  String msg = DriverStation.getGameSpecificMessage();
  if (msg == null || msg.isEmpty()) {
    return Forecast.UNKNOWN;   // not yet broadcast — poll again
  }
  switch (msg.charAt(0)) {
    case 'W': return Forecast.WHITEOUT;  // Crates doubled; ROPED UP needs 2 crates
    case 'I': return Forecast.ICEFALL;   // O2 Cells doubled; ROPED UP needs 2 cells
    case 'G': return Forecast.GALE;      // Rope Coils doubled; ROPED UP needs 2 coils
    default:  return Forecast.UNKNOWN;
  }
}
```

Implementation notes:

- The message may be **empty until the moment AUTO starts**. Poll in `autonomousInit()` *and* re-check in the first iterations of `autonomousPeriodic()`; select the branch on the first valid read and latch it. Never block waiting for it.
- Always implement a **default branch** (treat `UNKNOWN` as the highest-expected-value path). A robot that does nothing because the string was late scores nothing.
- **Offseason fallback:** without FMS, the FORECAST comes from the published card-draw procedure (Game Manual §4.3.1), and FIELD STAFF set the game data manually in the driver-station practice-match settings or through the offseason FMS tool. The code path is identical; test all three letters plus the empty string in every practice session.
- The ROUTE DECLARATION is **not** game data. The alliance chooses it during setup, so it is known before the MATCH. Hard-code it per MATCH from the drive team's pick; only the FORECAST arrives at runtime.

### 6.8 Simulation

The layout JSON works unmodified in desktop simulation:

- **WPILib sim:** load the same `AprilTagFieldLayout` in simulation and publish robot and vision poses to a `Field2d` widget. AdvantageScope can render the tag poses and both estimates in 3D by loading the JSON as a custom AprilTag layout asset alongside a custom field model.
- **PhotonVision sim (`photonlib` `VisionSystemSim`):** call `visionSim.addAprilTags(fieldLayout)` with the loaded layout and add a `PhotonCameraSim` with the real camera's calibration and the robot-to-camera transform. The entire auto-align stack, including the low-camera framing of the 17.5-in CRAG tags and all three FORECAST branches, can then be developed and regression-tested on the desktop.
- **Occlusion case to simulate:** place a 5 × 14 in cylinder upright on the DEPOT tray floor (Z = 0.25) immediately in front of one SHELF FACE tag. It represents an O2 CELL stood on end in the BASE DEPOT, the one SUPPLY that reaches into a CRAG tag's target band (§1.3). Confirm that the pose estimator falls back to the face's other tag, or to MultiTag across faces, rather than emitting a bad single-tag pose.
- Because there is **one canonical layout** (no per-venue field variants), simulation and the competition field share this single file, and it must match the field CAD model exactly. Version it in the robot repository.

---

## 7. Quick Reference

| Item | Value |
|---|---|
| Family / count | 36h11, 26 tags (IDs 1–26) |
| Tag size parameter | **0.1651 m** (6.5 in black square) |
| Panel / target | 9.0 in panel, 8.125 in target |
| CRAG tag centers | Z = 17.5 in, ±14 in from the face centerline, face planes 24 in from CRAG center |
| HEADWALL tag centers | Z = 12 in, lane centers, plumb tag plane at X = 39 (Blue) / 609 (Red) |
| OUTFITTER tag centers | Z = 52 in, above chute centers, on the wall plane |
| Blue IDs | 1–2 OUTFITTER, 3–5 HEADWALL, 6–13 CRAG |
| Red IDs | 14–15 OUTFITTER, 16–18 HEADWALL, 19–26 CRAG (= Blue rotated 180°, ID + 13) |
| Socket standoff (in every socket transform) | **8.0 in** along the face normal |
| Shelf slot lateral centers | −15.5 / 0 / +15.5 in |
| Coordinate frame | Always-blue-origin NWU, meters in JSON, field 16.4592 × 8.2296 m |
| FORECAST game data | `"W"` / `"I"` / `"G"` via `getGameSpecificMessage()` |
