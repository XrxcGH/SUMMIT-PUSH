# Authoring guide — SUMMIT PUSH FeatureScript generator

How the generator is put together, and the rules every source file follows. Read this before
editing anything under `src/`.

## Layout

| File | Role | Language |
|---|---|---|
| `src/00_header.fs` | version header, import, banner | FeatureScript |
| `src/10_kernel.fs` | the **only** code that calls the Onshape standard library | FeatureScript |
| `src/20_ledger.fs` | every dimension, the palette, the materials | part-code dialect |
| `src/30_util.fs` | shared helpers (planes, boxes, frames, painting) | part-code dialect |
| `src/40_field.fs` … `src/45_pieces.fs` | the field elements | part-code dialect |
| `src/48_main.fs` | `buildField` and the dimension self-check | part-code dialect |
| `src/90_features.fs` | the features that appear in Onshape's menu | FeatureScript |
| `verify/kernel_occ.py` | OpenCascade twin of `10_kernel.fs` — same names, same semantics | Python |
| `verify/fs2py.py` | lints the dialect and transpiles it to Python | Python |
| `verify/scope_lint.py` | FeatureScript scope rules the Python twin cannot see | Python |
| `verify/onshape_lint.py` | the Feature Studio editor's own warnings, reproduced off-line | Python |
| `verify/run.py`, `verify/run_checks.py`, `verify/checks/*.py` | off-line build and checks | Python |

`build.py` concatenates `src/*.fs` in name order into `SummitPushField.fs` (the file users paste
into a Feature Studio), lints the dialect, fails on any warning the Onshape editor would show
(an unused declaration, a variable set but never read), and, when a checkout of the
FeatureScript standard library is available (`--std PATH`, `$FS_STD` or `.fs-std/`), checks
every std call, enum member and name collision against it.

## The part-code dialect

Files `src/2x`–`src/4x` are written so that they mean the same thing in FeatureScript and, after
`verify/fs2py.py`, in Python. The lint enforces:

- plain numbers only — **inches and degrees**; the kernel adds units. No `^`, `~`, `%`, `?:`, `++`.
- statements end in `;`; block braces stand alone on their own lines (Allman style).
- control flow: `for (var i = A; i < B; i += S)`, `for (var x in ARRAY)`, `if (...)` / `else if (...)` / `else`.
- declarations: `var x = ...;`, `const x = ...;`, `function name(context is Context, id is Id, a, b)`.
- maps are indexed `m["key"]`, never `m.key`; strings only as literals and through `nm(s, i)` / `msg([...])`.
- no variable may shadow a std-library name (`plane`, `line`, `box`, `vector`, `size`, …) or a reserved word of either language.
- a variable declared inside a block must not be used outside it (FeatureScript is block-scoped; Python is not — the lint cannot see this, so be careful).
- vectors for arithmetic are `vector(x, y, z)`; plain arrays `[x, y]` are for points passed to the kernel.

## Kernel API (plain numbers; identical in `10_kernel.fs` and `kernel_occ.py`)

Frames and planes

- `frameMake(o, x, z)` — world frame; `frameIn(F, o, x, z)` — frame given in F's coordinates.
- a local plane `pl = [origin, normal, xDir]` in F coordinates; sketch coordinates (u, v) run along xDir and normal × xDir. Helpers in `30_util.fs`: `plXY(z0)` (u,v = x,y; extrude +z), `plYZ(x0)` (u,v = y,z; extrude +x), `plXZ(y0)` (u,v = x,z; extrude −y), `plAxis(o, axis, radial)` (for revolves: v along `axis`).

Shapes (each creates exactly one body under `id`; never create a body under another body's id)

- `mkPrism(ctx, id, F, pl, pts, d0, d1)` — polygon extruded d0..d1 along the plane normal.
- `mkPrismHoles(ctx, id, F, pl, outer, holes, d0, d1)`; `mkPrismProfile(ctx, id, F, pl, loops, d0, d1)` with loops of segments `["L", a, b]`, `["A", a, mid, b]`, `["C", centre, r]`.
- `mkCyl(ctx, id, F, pl, c, r, d0, d1)`; `mkRevolve(ctx, id, F, pl, loop)` — full revolve about the plane's v axis.
- `mkPillowBox(ctx, id, F, h, crown)`; `mkBox(ctx, id, F, p0, p1)` and `prismXY/XZ/YZ` (util).

Booleans and finishing

- `bSubtract(ctx, id, targets, tools, keepTools)`, `bUnion(ctx, id, bodies)` (style every input first), `bDelete`.
- `removeSlivers(ctx, id, bodies, minVolume)` — delete the tiny bodies a boolean can leave behind.
- `shellHollow(ctx, id, bodies, t)`.
- `filletAt(ctx, id, bodies, F, pts, r)` — fillet the edges through the local points; `softFilletAt(..., label)` warns instead of failing (use it for decoration).
- `copyBody(ctx, id, src, F)` — copy a body modelled about the world origin into frame F.

Appearance and properties

- `paint(ctx, bodies, name, paletteToken, alpha, materialKey)`; `paintRGB(...)`; `styleBody(...)`; `nameBody`.
- `styleFacesAt(ctx, bodies, F, pts, rgb, alpha)` — colour individual faces.
- `tagDecal(ctx, id, bodies, F, pl, black, cells, s, rgb)` — paint an AprilTag's black cells onto its panel face by splitting the face; the geometry stays coplanar.
- `massBody(ctx, bodies, materialName, massLb)` — density set so the body weighs exactly `massLb`.
- `numberSharedNames(ctx, bodies)` — suffix " 1", " 2", … onto parts that share a name.
- `groupParts(ctx, id, bodies, name)` — group finished bodies into one open composite part (call last).
- `kWarn(ctx, id, message)` — append a warning to the feature's own status (sub-operation warnings are not shown).

Measurement (used by self-checks): `measureBox(ctx, bodies, F)`, `measureVolume`, `measureDistToPoint`, `measureDist`, `countBodies`.

## Conventions every element follows

- **Every body is named, coloured and given a material.** Names read as `<ALLIANCE> <ELEMENT> <part>`, e.g. `BLUE CRAG Low Socket`.
- **CRITICAL dimensions are never touched by decoration.** Robot-interaction surfaces (shelf tops, socket bores and rims, pegs, rungs, lip, tags) keep their exact geometry. Rock on the CRAG is a texture, never geometry (MATERIALS-AND-COLORS §3 rule 1): no relief on CRAG faces.
- Decoration uses `softFilletAt`, so a failure only warns.
- Every Id prefix is one contiguous run of operations (std `context.fs`): never go back to an element's Id after another element has started. A self-check probe gets its own top-level Id.
- No two bodies may share volume (contact is fine), and every body must stay valid. `verify/run.py` checks both.
- Red is always Blue rotated 180° about (324, 162) — build with the alliance frame, never by hand.

## Verifying a change

```
git clone https://github.com/javawizard/onshape-std-library-mirror 03-field/featurescript/.fs-std   # once
python 03-field/featurescript/build.py                 # assemble, lint, Onshape warnings, std API check
python 03-field/featurescript/verify/run.py            # build, self-check, palette, tags, supplies, interference
python 03-field/featurescript/verify/run_checks.py     # the independent element checks in verify/checks/
python 03-field/featurescript/verify/render.py         # PNG views in renders/
```

The Studio targets FeatureScript 2960; check out the mirror's `Version 2960.0` commit if its head
has moved on.

All must pass before a change is committed.
