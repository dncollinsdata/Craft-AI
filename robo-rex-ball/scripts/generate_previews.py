"""Render previews of the real CAD meshes (software renderer, matplotlib).

  output/previews/dino_mode.png, dino_side.png, ball_mode.png, ball_front.png,
  exploded.png, transformation_sequence.png, transformation.gif
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import manifold3d as mf
import trimesh
from robo_rex import assembly as AS, kinematics as K, params as P

OUT = os.path.join(AS.ROOT, "output", "previews")
COL = {"panel": "#2f6db5", "rear_shell": "#2a5f9e", "skull": "#f08c2e", "jaw": "#d9741c",
       "tail": "#f08c2e", "torso": "#5b6168", "thigh": "#8a96a3", "shin": "#9aa6b2",
       "arm": "#8a96a3", "slider": "#e8e8e8", "axle": "#cfcfcf", "polecap": "#e0e0e0"}
_LOW = {}


def color(n):
    return np.array(matplotlib.colors.to_rgb(next(c for k, c in COL.items() if n.startswith(k))))


def low(n, tol=0.12):
    """Decimated home-frame mesh for rendering only."""
    if n not in _LOW:
        m = AS.mesh(n)
        man = mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                                  tri_verts=np.asarray(m.faces, np.uint32))).simplify(tol)
        o = man.to_mesh()
        _LOW[n] = trimesh.Trimesh(np.asarray(o.vert_properties)[:, :3], np.asarray(o.tri_verts))
    return _LOW[n]


def posed(q, offsets=None):
    Tm = K.transforms(q)
    out = []
    for n in AS.ORDER:
        m = low(n).copy()
        m.apply_transform(Tm[AS.body_of(n)])
        if offsets and n in offsets:
            m.apply_translation(offsets[n])
        out.append((n, m))
    return out


def render(items, path, elev=18, azim=-60, title=None, lim=None, ground=None, ax=None, size=(8, 6)):
    own = ax is None
    if own:
        fig = plt.figure(figsize=size, dpi=140)
        ax = fig.add_subplot(projection="3d")
    e, a = np.radians(elev), np.radians(azim)
    view = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    light = view + np.array([0.0, 0.0, 0.6]) + 0.4 * np.cross(view, [0, 0, 1])
    light /= np.linalg.norm(light)
    tris, cols = [], []
    for n, m in items:
        nrm = m.face_normals
        I = 0.32 + 0.68 * np.clip(nrm @ light, 0, 1)
        spec = np.clip(nrm @ light, 0, 1) ** 24 * 0.25
        c = np.clip(color(n)[None, :] * I[:, None] + spec[:, None], 0, 1)
        tris.append(m.triangles)
        cols.append(c)
    tris, cols = np.concatenate(tris), np.concatenate(cols)
    ax.add_collection3d(Poly3DCollection(tris, facecolors=cols, edgecolors=cols, linewidths=0.15))
    allv = tris.reshape(-1, 3)
    if ground is not None:      # ground line under the feet
        xs = np.array([allv[:, 0].min() - 10, allv[:, 0].max() + 10])
        for yy in (-40, 40):
            ax.plot(xs, [yy, yy], [ground, ground], color="#999999", lw=0.8)
    c = (allv.max(0) + allv.min(0)) / 2
    r = lim or (allv.max(0) - allv.min(0)).max() / 2 * 1.02
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev, azim)
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=11)
    if own:
        plt.subplots_adjust(0, 0, 1, 0.95)
        plt.savefig(path, facecolor="white")
        plt.close()


def exploded_offsets():
    Tm = K.transforms(K.pose_q("ball"))
    off = {}
    for n in AS.ORDER:
        m = low(n).copy(); m.apply_transform(Tm[AS.body_of(n)])
        c = m.centroid
        v = c / (np.linalg.norm(c) + 1e-9)
        k = 60.0 if n.startswith(("skull", "jaw", "tail")) else 38.0
        if n.startswith(("panel", "polecap", "axle")):
            v = np.array([0.35, np.sign(c[1]), 0.0]); k = 70 if n.startswith("panel") else 105
        if n == "rear_shell":
            v = np.array([-1.0, 0, 0]); k = 55
        if n.startswith(("thigh", "shin", "arm", "slider")):
            v = np.array([0, np.sign(c[1]), -0.25]); k = {"thigh": 42, "shin": 62, "arm": 30, "slider": 85}[n.split("_")[0]]
        if n == "torso":
            k = 0
        off[n] = v * k
    return off


def main():
    os.makedirs(OUT, exist_ok=True)
    qd, qb = K.pose_q("dino"), K.pose_q("ball")
    gz = -61.52
    render(posed(qd), os.path.join(OUT, "dino_mode.png"), 16, -55, "ROBO REX BALL - dinosaur mode", ground=gz)
    render(posed(qd), os.path.join(OUT, "dino_side.png"), 4, -90, "Dinosaur mode, side view (tripod stance)", ground=gz)
    qo = dict(qd); qo["jaw"] = P.JAW_OPEN
    render(posed(qo), os.path.join(OUT, "dino_jaw_open.png"), 12, -35, "Jaw open (independent hinge)", ground=gz)
    render(posed(qb), os.path.join(OUT, "ball_mode.png"), 22, -50, "Ball mode (100 mm)")
    render(posed(qb), os.path.join(OUT, "ball_bottom.png"), -35, -120, "Ball mode from below (latch sliders)")
    render(posed(qb, exploded_offsets()), os.path.join(OUT, "exploded.png"), 24, -62, "Exploded assembly (ball pose)",
           size=(10, 8), lim=92)

    # transformation sequence contact sheet: end of every phase
    frames = [("dino", dict(qd))]
    q = dict(qd)
    for name, target in K.SEQUENCE:
        q.update(target)
        frames.append((name, dict(q)))
    cols = 5
    rows = int(np.ceil(len(frames) / cols))
    fig = plt.figure(figsize=(4 * cols, 4 * rows), dpi=110)
    for i, (name, qq) in enumerate(frames):
        ax = fig.add_subplot(rows, cols, i + 1, projection="3d")
        render(posed(qq), None, 15, -60, f"{i}. {name}", lim=78, ax=ax)
    plt.subplots_adjust(0, 0, 1, 0.97, 0.0, 0.08)
    plt.savefig(os.path.join(OUT, "transformation_sequence.png"), facecolor="white")
    plt.close()

    # animated GIF (dino -> ball)
    from PIL import Image
    imgs = []
    samples = list(K.sequence_samples(4))
    for name, t, qq in samples:
        fn = os.path.join(AS.CACHE, "_frame.png")
        render(posed(qq), fn, 15, -60, name, lim=78, size=(5, 4.2))
        imgs.append(Image.open(fn).convert("P", palette=Image.ADAPTIVE).copy())
    imgs += [imgs[-1]] * 6
    imgs[0].save(os.path.join(OUT, "transformation.gif"), save_all=True, append_images=imgs[1:] + imgs[::-1],
                 duration=180, loop=0)
    print("previews written to", OUT)


if __name__ == "__main__":
    main()
