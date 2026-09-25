# -*- coding: utf-8 -*-
"""
Animated glTF from off-line builds: build the moving bodies at a series of times, recover every
part's rigid motion from the builds, and write one .glb whose nodes carry glTF animation channels.

    from animate import export_animation
    export_animation(build_at, times, "motion.glb", static=static_ctx)

build_at(t) is a caller-supplied function returning a kernel_occ.Registry that holds the bodies
that move, posed for time t (for example SUPPLIES placed with copyBody at poses that depend on t);
`static` is an optional Registry of bodies that never move (the field), exported once without
channels.  Nothing in this repository calls export_animation; it is a library entry point.  The
first time is the reference pose: its geometry becomes the nodes' meshes and every later build
contributes one keyframe per node:

  * a body built identically (same construction, same topology) at every time is matched by
    part name; its rigid transform is solved from its vertices (Kabsch; the rms residual must
    stay under 1e-4 in, so a body that deforms between builds is reported, not guessed);
  * a part missing at some times (a SUPPLY picked up, a scored piece appearing) is hidden with a
    STEP scale channel (0 while absent), keeping its last pose.

Coordinates: meshes are written in glTF metres / Y-up like export_glb; a field-frame motion
q' = R q + d becomes p' = A R A^T p + 0.0254 A d with A the axis swap (x, y, z) -> (x, z, -y).
"""
import json
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from OCP.TopAbs import TopAbs_VERTEX  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopoDS import TopoDS  # noqa: E402
from OCP.BRep import BRep_Tool  # noqa: E402

import export_glb as G  # noqa: E402

A = np.array([[1.0, 0, 0], [0, 0, 1.0], [0, -1.0, 0]])      # field -> glTF axes


def _vertices(rec):
    out = []
    for s in rec["solids"]:
        exp = TopExp_Explorer(s, TopAbs_VERTEX)
        while exp.More():
            p = BRep_Tool.Pnt_s(TopoDS.Vertex(exp.Current()))
            out.append((p.X(), p.Y(), p.Z()))
            exp.Next()
    return np.array(out)


def _kabsch(P, Q):
    """R, d minimising |R P + d - Q| (rows are points); returns R, d, rms."""
    cp, cq = P.mean(0), Q.mean(0)
    H = (P - cp).T @ (Q - cq)
    U, S, Vt = np.linalg.svd(H)
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    R = Vt.T @ D @ U.T
    d = cq - R @ cp
    rms = float(np.sqrt(np.mean(np.sum((P @ R.T + d - Q) ** 2, axis=1))))
    return R, d, rms


def _quat(R):
    """Unit quaternion [x, y, z, w] of a rotation matrix."""
    t = np.trace(R)
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        w, x, y, z = 0.25 * s, (R[2, 1] - R[1, 2]) / s, (R[0, 2] - R[2, 0]) / s, (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = math.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w, x, y, z = (R[2, 1] - R[1, 2]) / s, 0.25 * s, (R[0, 1] + R[1, 0]) / s, (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = math.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w, x, y, z = (R[0, 2] - R[2, 0]) / s, (R[0, 1] + R[1, 0]) / s, 0.25 * s, (R[1, 2] + R[2, 1]) / s
    else:
        s = math.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w, x, y, z = (R[1, 0] - R[0, 1]) / s, (R[0, 2] + R[2, 0]) / s, (R[1, 2] + R[2, 1]) / s, 0.25 * s
    q = np.array([x, y, z, w])
    return q / np.linalg.norm(q)


def _parts(ctx):
    """part name -> record holding exactly that part (multi-solid records are split)."""
    out = {}
    for k, rec in ctx.bodies.items():
        names = rec.get("solid_names")
        if names:
            for i, s in enumerate(rec["solids"]):
                out[names[i]] = dict(rec, solids=[s], name=names[i], decal=None)
        else:
            out[rec["name"] or "/".join(k)] = rec
    return out


def export_animation(build_at, times, path, static=None, extras=None, log=print):
    times = [float(t) for t in times]
    ref = _parts(build_at(times[0]))
    refv = {n: _vertices(r) for n, r in ref.items()}
    track = {n: [] for n in ref}               # name -> [(t, R, d, present)]
    problems = []
    for t in times:
        cur = ref if t == times[0] else _parts(build_at(t))
        for n in ref:
            if n not in cur:
                last = track[n][-1] if track[n] else (t, np.eye(3), np.zeros(3), False)
                track[n].append((t, last[1], last[2], False))
                continue
            V = refv[n] if cur is ref else _vertices(cur[n])
            if V.shape != refv[n].shape:
                problems.append("%s: topology changes at t = %g (%d vs %d vertices)" % (n, t, len(V), len(refv[n])))
                last = track[n][-1] if track[n] else (t, np.eye(3), np.zeros(3), True)
                track[n].append((t, last[1], last[2], True))
                continue
            R, d, rms = _kabsch(refv[n], V)
            if rms > 1e-4:
                problems.append("%s: not rigid at t = %g (rms %.2e in)" % (n, t, rms))
            track[n].append((t, R, d, True))
        extra = sorted(set(cur) - set(ref))
        if extra:
            problems.append("t = %g: parts absent from the reference build are not animated: %s" % (t, extra[:5]))
        log("  sampled t = %6.2f s (%d parts)" % (t, len(cur)))

    g = G._Glb()
    roots = []
    if static is not None:
        for n, rec in _parts(static).items():
            i = g.add_body(rec, n)
            if i is not None:
                roots.append(i)
    channels, samplers = [], []
    tin = g.accessor(np.array(times, dtype=np.float32).reshape(-1, 1), 5126, "SCALAR", None, True)
    g.views[-1].pop("target", None)
    moving = 0
    for n, rec in ref.items():
        node = g.add_body(rec, n)
        if node is None:
            continue
        roots.append(node)
        tr = track[n]
        moves = any(np.abs(R - np.eye(3)).max() > 1e-9 or np.abs(d).max() > 1e-9 for (_, R, d, _) in tr)
        hides = any(not p for (_, _, _, p) in tr)
        if not moves and not hides:
            continue
        moving += 1
        T = np.array([G.IN * (A @ d) for (_, _, d, _) in tr], dtype=np.float32)
        Q = np.array([_quat(A @ R @ A.T) for (_, R, _, _) in tr], dtype=np.float32)
        for i in range(1, len(Q)):                      # keep quaternions on one hemisphere
            if np.dot(Q[i], Q[i - 1]) < 0:
                Q[i] = -Q[i]
        for arr, typ, pathname, interp in ((T, "VEC3", "translation", "LINEAR"), (Q, "VEC4", "rotation", "LINEAR")):
            out = g.accessor(arr, 5126, typ, None)
            g.views[-1].pop("target", None)
            samplers.append({"input": tin, "output": out, "interpolation": interp})
            channels.append({"sampler": len(samplers) - 1, "target": {"node": node, "path": pathname}})
        if hides:
            S = np.array([[1, 1, 1] if p else [0, 0, 0] for (_, _, _, p) in tr], dtype=np.float32)
            out = g.accessor(S, 5126, "VEC3", None)
            g.views[-1].pop("target", None)
            samplers.append({"input": tin, "output": out, "interpolation": "STEP"})
            channels.append({"sampler": len(samplers) - 1, "target": {"node": node, "path": "scale"}})
        # the node's rest pose is the first keyframe
        tr0 = track[n][0]
        g.nodes[node]["translation"] = [float(x) for x in G.IN * (A @ tr0[2])]
        g.nodes[node]["rotation"] = [float(x) for x in _quat(A @ tr0[1] @ A.T)]
    doc_extras = dict(extras or {})
    doc_extras["problems"] = problems
    _write_with_animation(g, path, roots, channels, samplers, doc_extras)
    return {"nodes": len(roots), "moving": moving, "problems": problems, "keyframes": len(times)}


def _write_with_animation(g, path, roots, channels, samplers, extras):
    doc = {"asset": {"version": "2.0", "generator": "SUMMIT PUSH off-line twin (animate.py)"},
           "scene": 0, "scenes": [{"nodes": roots}], "nodes": g.nodes, "meshes": g.meshes,
           "materials": g.materials, "accessors": g.accessors, "bufferViews": g.views,
           "buffers": [{"byteLength": len(g.bin)}], "extras": extras}
    if channels:
        doc["animations"] = [{"name": "MOTION", "channels": channels, "samplers": samplers}]
    js = json.dumps(doc, separators=(",", ":")).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    while len(g.bin) % 4:
        g.bin.append(0)
    total = 12 + 8 + len(js) + 8 + len(g.bin)
    with open(path, "wb") as fh:
        fh.write(struct.pack("<III", 0x46546C67, 2, total))
        fh.write(struct.pack("<II", len(js), 0x4E4F534A))
        fh.write(js)
        fh.write(struct.pack("<II", len(g.bin), 0x004E4942))
        fh.write(g.bin)
