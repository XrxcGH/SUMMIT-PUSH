# SUMMIT PUSH — Materials, Colors, and Finishes

**Document:** `03-field/MATERIALS-AND-COLORS.md` · **Geometry authority:** `03-field/FIELD-CAD-PACKAGE.md`

This document specifies the appearance of every ARENA element, so that a field model can be built, rendered, and captured in screenshots without inventing any material or color. It is kept separate from the geometry document. **Nothing here is a rule, and the geometry document governs every dimension.** Section properties appear here only where a render needs them. Where a color affects a rules outcome (alliance tape, bumper covers, piece identification), the manual governs and this document restates it.

The field is built virtually. Materials are named so that a CAD appearance can be assigned and a render reads correctly; they are not a fabrication specification.

---

## 1. Palette

### 1.1 Alliance and neutral

| Token | Hex | Use |
|---|---|---|
| `alliance-blue` | `#1D63C8` | Blue tape, Blue tier rings and beacon, Blue bumper covers, Blue plan-view tint |
| `alliance-blue-dark` | `#0E3F86` | Blue outlines and edges in drawings |
| `alliance-red` | `#CC3333` | Red tape, Red tier rings and beacon, Red bumper covers, Red plan-view tint |
| `alliance-red-dark` | `#8E2020` | Red outlines and edges in drawings |
| `neutral-white` | `#F5F5F5` | Neutral tape marks, FORECAST LED state, AprilTag border |
| `led-green` | `#3FBF4F` | FIELD-safe LED state |

### 1.2 Structure

| Token | Hex | Use |
|---|---|---|
| `crag-body` | `#E9E2D4` | CRAG tower faces |
| `crag-spire` | `#DDD3C0` | CRAG spire faces (below the lantern) |
| `crag-accent` | `#4A3B22` | CRAG edges, kick-guard, shelf and depot framing in drawings |
| `beacon-lantern` | `#FFF3D0` at 35% opacity | The translucent top 12 in of the spire, unlit |
| `truss` | `#8A6D3B` | HEADWALL chords and uprights |
| `truss-dark` | `#5C4823` | HEADWALL outlines |
| `rung` | `#9AA0A6` | HEADWALL rungs, pegs |
| `shelf` | `#8A6D3B` | Shelf slabs and slot fences |
| `socket` | `#9DB8D6` | Socket tubes |
| `depot` | `#7F7F7F` | BASE DEPOT lip and tray |
| `wall` | `#9AA4B2` | Alliance walls, guardrail frame |
| `glazing` | `#DCE8FA` at 25% opacity | Polycarbonate guardrail and alliance-wall glazing |
| `carpet` | `#6E6A63` | Field carpet |

### 1.3 Game pieces

| Piece | Token | Hex | Notes |
|---|---|---|---|
| CACHE CRATE | `crate-violet` | `#7B3FA0` | 62° from alliance blue and 83° from alliance red in hue |
| O2 CELL body | `cell-body` | `#F2F2F0` | |
| O2 CELL caps | `cell-cap` | `#2E8B57` | |
| O2 CELL cap fillet | `cell-fillet` | `#4D4D4D` | the blend band at each cap/body junction |
| ROPE COIL | `coil-amber` | `#D9A441` | |

**Why these colors are locked.** No SUPPLY may be colored in or near either alliance color. A referee, a driver, or a vision pipeline can mis-attribute a piece that reads as blue or red, and the anti-pollution rule (manual §4.4.2) already makes ownership counter-intuitive: a SUPPLY belongs to the CRAG it sits on, whoever placed it. Saturated hues that are far from each other and from both alliance colors remove that source of confusion.

---

## 2. Element-by-element specification

Every ARENA element appears in this table once, grouped by assembly. "CAD §" points to the geometry in `FIELD-CAD-PACKAGE.md`; "Finish" is what a render needs.

| Element | CAD § | Material (modeled as) | Color | Finish | Thickness / section |
|---|---|---|---|---|---|
| Field carpet | §0 | Low-pile event carpet | `carpet` | matte, fine directional nap | — |
| Guardrail frame | §1.3 | Aluminum extrusion | `wall` | satin anodized | 2 × 1 in tube |
| Guardrail glazing | §1.3 | Polycarbonate | `glazing` | clear, slight surface sheen | 0.25 in |
| FIELD LED band | §1.3 | Frosted acrylic lens over an LED strip | state-dependent | frosted, self-illuminated | 1.0 in wide |
| Alliance wall, lower | §1.3 | Painted plywood on steel frame | `wall` | matte | 0.75 in |
| Alliance wall, upper glazing | §1.3 | Polycarbonate | `glazing` | clear | 0.25 in |
| Driver station shelf | §1.3 | Painted plywood | `wall` | matte | 0.75 in |
| E-STOP / A-STOP buttons | §1.3 | Molded plastic | red `#CC2020` / blue `#1D63C8` | gloss | ⌀2 in mushroom head |
| Zone tape | §1.2 | Gaffer tape | alliance color | matte | 2 in wide, 0.01 in |
| Neutral marks | §1.2 | Gaffer tape | `neutral-white` | matte | 2 in wide |
| CRAG tower faces | §2.1 | Painted plywood panel on steel frame | `crag-body` | **matte stone texture, appearance only** | 0.75 in panel |
| CRAG spire faces | §2.1 | Painted plywood panel | `crag-spire` | matte stone texture | 0.75 in panel |
| CRAG kick-guard | §2.1 | Aluminum angle | `crag-accent` | satin | 2 × 2 × 0.125 in |
| SUMMIT BEACON lantern | §2.1, §8 | Translucent white polycarbonate | `beacon-lantern`, alliance color when lit | frosted, self-illuminated when lit | 0.25 in |
| Shelf slab | §2.2 | Painted plywood | `shelf` | matte, low friction | 0.75 in |
| Slot fence | §2.2 | Painted hardwood strip | `shelf` | matte | 1.5 × 2.0 in |
| Shelf gusset | §2.2 | Aluminum plate | `crag-accent` | satin | 0.125 in |
| Socket tube | §2.3, §2.4 | Rolled aluminum tube | `socket` | satin inside and out; **no coating that reduces the bore below 6.375 in** | 0.09 in wall |
| Socket bracket | §2.3 | Aluminum plate | `crag-accent` | satin | 0.125 in |
| Summit Socket mast | §2.4 | Steel square tube | `crag-accent` | satin | 2 × 2 in |
| Peg | §2.5 | Steel round bar, fully rounded tip | `rung` | satin, no knurl | ⌀1.5 in |
| High Peg root boss | §2.5 | Steel plate let into the spire | `crag-accent` | satin | 0.25 in, spanning Z 74–80 behind an opaque-backed lantern edge |
| LED tier ring | §2.6, §8 | Frosted acrylic channel over an LED strip | alliance color when lit, dark when unlit | frosted, self-illuminated | 1.0 in wide |
| BASE DEPOT lip | §3 | Painted plywood | `depot` | matte, R0.25 top edge | 0.75 in |
| BASE DEPOT floor | §3 | Painted plywood, laid on the carpet (top at Z = 0.25) | `depot` | matte, low friction | 0.25 in |
| DEPOT entry chamfer | §3 | Painted plywood strip | `depot` | matte | 45°, 1.0 in |
| HEADWALL chord / upright | §4.1 | Steel square tube | `truss` | satin powder | 2 × 2 in |
| HEADWALL rung | §4.1 | Steel round bar | `rung` | satin, no knurl | ⌀1.5 in |
| HEADWALL rung bracket | §4.2 | Steel plate | `truss-dark` | satin | 0.25 in |
| HEADWALL lower crossbeam | §4.1 | Steel square tube | `truss` | satin | 2 × 2 in |
| HEADWALL tag wedge bracket | §4.1 | Solid aluminum | `truss-dark` | satin | 15° wedge, 9.0 in wide, 2.06–2.58 in thick |
| OUTFITTER chute ramp | §5 | UHMW-faced plywood | `wall` | low friction | 0.5 in |
| OUTFITTER cheek funnel | §5 | Painted plywood | `wall` | matte | 0.5 in |
| AprilTag panel | §7 | Printed vinyl on rigid backer | `neutral-white` + tag black `#111111` | **matte, non-glare** | 9.0 in sq × 0.25 in |
| CACHE CRATE | §9.1 | Ripstop-nylon skin over PU foam core | `crate-violet` | matte fabric, slight sheen at the seams | 12.0 in cube |
| O2 CELL | §9.2 | Rigid molded ABS shell and domed caps, no foam | `cell-body` / `cell-cap`, with `cell-fillet` on the R1.0 blend band at each junction | satin rigid plastic | ⌀5.0 × 14.0 in |
| ROPE COIL | §9.3 | Solid molded rubber/foam | `coil-amber` | matte, slightly tacky | 10.0 OD × 2.5 tube |

---

## 3. Appearance rules

1. **Rock is a surface texture only.** The CRAG reads as rock through surface appearance alone: a matte stone texture on planar faces, with **no sculpted relief, taper, displacement, or facets**. Every published height must be exact at every face, which a textured plane guarantees. Keep the texture on the suppressible "cosmetics" layer with the LED rings.
2. **Plan-view tinting is a drafting convention.** `field-top-view.svg` fills the CRAGS in alliance color for legibility. The physical CRAG is `crag-body` tan; only its tape, tier rings, and beacon carry alliance color.
3. **AprilTag panels must be non-glare.** A gloss finish on a tag panel causes vision failures. Keep the full 8.125-in white border unobstructed as seen from the field side.
4. **Nothing on the field may be colored to imitate a game piece, a tier ring, or the SUMMIT BEACON.** The corresponding constraint on ROBOTS is **R207**.
5. **The socket bore is a toleranced dimension.** No paint, powder, or liner may reduce the bore below the lower limit of 6.375 in.
6. **Model both lit and unlit states.** Give the tier rings and the beacon two appearance states so that renders can show a fully lit mountain, which is the clearest single image for explaining the game.

---

## 4. Render checklist

A field render is complete when it correctly shows:

- [ ] Carpet, guardrails, and both alliance walls, with driver stations
- [ ] Both CRAGS with all 17 scoring positions modeled and the BASE DEPOT trays
- [ ] Both HEADWALLS with all nine rungs each, correctly staggered, and the lane tag panels
- [ ] All four OUTFITTER chutes with tag panels
- [ ] All tape: BASECAMP, both CLIMB LINES carried to the full field width, OUTFITTER LANES, both APRONS at the correct 36/20 offsets, the FIELD centerline, the CENTER CACHE band and marks, alliance staging marks
- [ ] All 26 AprilTag panels at their published poses
- [ ] All 63 SUPPLIES in their staged positions, in the Latin-square CENTER CACHE arrangement
- [ ] Tier rings and beacons modeled in both lit and unlit states
- [ ] FIELD LED bands in the guardrail top rails
