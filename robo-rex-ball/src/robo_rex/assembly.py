"""Part registry, mesh cache, posed assemblies and STEP export."""
import os
import hashlib
import inspect
import numpy as np
import cadquery as cq
import trimesh

from . import params as P
from . import kinematics as K
from .geom import mirror_y, pol
from . import torso as T, armor as A, head as H, tail as TL, legs as L, hinges as HG

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(ROOT, "output", "cache")

# name: (builder, body that moves it, quantity printed, description)
PARTS = {
    "torso":      (T.torso, "torso", 1, "Central core: axle hub, pivots, dorsal + belly skin, latch channel"),
    "rear_shell": (A.rear_shell, "rear_shell", 1, "Fixed rear haunch armour (pinned to torso)"),
    "panel_L":    (A.front_panel, "panel_L", 1, "Left swinging front armour panel"),
    "panel_R":    (A.front_panel_R, "panel_R", 1, "Right swinging front armour panel (mirror)"),
    "skull":      (H.skull, "head", 1, "Armoured skull with eyes, brow, nostrils, teeth"),
    "jaw":        (H.jaw, "jaw", 1, "Independently hinged lower jaw with teeth"),
    "tail1":      (lambda: TL.tail_segment(1), "tail1", 1, "Tail root segment"),
    "tail2":      (lambda: TL.tail_segment(2), "tail2", 1, "Tail middle segment"),
    "tail3":      (lambda: TL.tail_segment(3), "tail3", 1, "Tail tip segment"),
    "thigh_L":    (L.thigh, "thigh_L", 1, "Left thigh with hip sleeve and stop ring"),
    "thigh_R":    (lambda: mirror_y(L.thigh()), "thigh_R", 1, "Right thigh (mirror)"),
    "shin_L":     (L.shin, "shin_L", 1, "Left shin with three-toed foot"),
    "shin_R":     (lambda: mirror_y(L.shin()), "shin_R", 1, "Right shin + foot (mirror)"),
    "arm_L":      (L.arm, "arm_L", 1, "Left arm, two blunt claws"),
    "arm_R":      (lambda: mirror_y(L.arm()), "arm_R", 1, "Right arm (mirror)"),
    "slider_L":   (T.slider, "slider_L", 1, "Left latch slider"),
    "slider_R":   (lambda: mirror_y(T.slider()), "slider_R", 1, "Right latch slider (mirror)"),
    "axle_L":     (HG.axle, "axle_L", 1, "Main axle half (left)"),
    "axle_R":     (lambda: mirror_y(HG.axle()), "axle_R", 1, "Main axle half (right)"),
    "polecap_L":  (HG.pole_cap, "polecap_L", 1, "Pole cap with stop lug (left)"),
    "polecap_R":  (lambda: mirror_y(HG.pole_cap()), "polecap_R", 1, "Pole cap with stop lug (right)"),
}

# Hardware placed for STEP / previews only (excluded from collision checks:
# they live in holes that already carry the running clearance).
def _pin_at(xz, y0, length, d=P.PIN_D, head=None):
    p = HG.d_pin(length, d=d, head_d=head)
    return p.translate((xz[0], y0, xz[1]))


PINS = {
    "pin_head":  (lambda: HG.d_pin(2 * P.CB - 0.4), "head", K.JOINTS["head"]["pivot"], -P.CB + 0.2, 1, "D4 x 17.6 knuckle pin"),
    "pin_tail1": (lambda: HG.d_pin(2 * P.CB - 0.4), "tail1", K.JOINTS["tail1"]["pivot"], -P.CB + 0.2, 1, "D4 x 17.6 knuckle pin"),
    "pin_tail2": (lambda: HG.d_pin(2 * P.CB - 0.4), "tail2", K.JOINTS["tail2"]["pivot"], -P.CB + 0.2, 1, "D4 x 17.6 knuckle pin"),
    "pin_tail3": (lambda: HG.d_pin(2 * P.CB - 0.4), "tail3", K.JOINTS["tail3"]["pivot"], -P.CB + 0.2, 1, "D4 x 17.6 knuckle pin"),
    "pin_jaw":   (lambda: HG.d_pin(2 * P.CB - 0.4, d=H.JAW_PIN_D), "jaw", K.JAW_PIVOT, -P.CB + 0.2, 1, "D3 x 17.6 jaw pin"),
}

ORDER = list(PARTS)


def _src_hash():
    h = hashlib.sha1()
    d = os.path.dirname(__file__)
    for f in sorted(os.listdir(d)):
        if f.endswith(".py"):
            h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()[:12]


_SOLIDS = {}


def solid(name):
    if name not in _SOLIDS:
        _SOLIDS[name] = PARTS[name][0]()
    return _SOLIDS[name]


def mesh(name, tol=0.05):
    """Home-frame mesh, cached on disk keyed by the source hash."""
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, f"{name}_{_src_hash()}.stl")
    if not os.path.exists(fn):
        cq.exporters.export(solid(name), fn, tolerance=tol, angularTolerance=0.15)
    return trimesh.load(fn, force="mesh")


def body_of(name):
    return PARTS[name][1]


def posed_meshes(q, names=None):
    Tm = K.transforms(q)
    out = {}
    for n in names or ORDER:
        m = mesh(n).copy()
        m.apply_transform(Tm[body_of(n)])
        out[n] = m
    return out


def location(M):
    from OCP.gp import gp_Trsf
    T = gp_Trsf()
    T.SetValues(*[float(v) for v in np.asarray(M)[:3, :4].flatten()])
    return cq.Location(T)


def posed_solid(name, q):
    M = K.transforms(q)[body_of(name)]
    return solid(name).val().moved(location(M))


def export_step(q, path):
    asm = cq.Assembly(name="robo_rex_ball")
    Tm = K.transforms(q)
    colors = {"panel": "steelblue", "rear": "steelblue", "skull": "orange", "jaw": "orange",
              "tail": "orange", "torso": "gray", "thigh": "darkorange", "shin": "darkorange",
              "arm": "darkorange"}
    for n in ORDER:
        M = Tm[body_of(n)]
        loc = location(M)
        col = next((c for k, c in colors.items() if n.startswith(k)), "lightgray")
        asm.add(solid(n), name=n, loc=loc, color=cq.Color(col))
    asm.save(path)
