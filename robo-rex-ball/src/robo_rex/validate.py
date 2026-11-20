"""Software validation: integrity, interference, envelope, path, stops,
standing stability, rolling surface and printability."""
import math
import numpy as np
import trimesh
from scipy.spatial import ConvexHull
from . import assembly as AS, kinematics as K, collide as C, printing as PR, params as P

PLA = 1.24e-3        # g / mm^3
INFILL = 0.20
SKIN = 1.2           # 3 perimeters x 0.4 mm


# ----------------------------------------------------------- integrity ------
def part_integrity(name):
    w = AS.solid(name)
    m = AS.mesh(name)
    th = PR.thickness_samples(m, n=1200)
    return dict(
        brep_valid=bool(w.val().isValid()), solids=len(w.solids().vals()),
        watertight=bool(m.is_watertight), winding=bool(m.is_winding_consistent),
        nonmanifold_edges=PR.nonmanifold_edges(m), volume_cm3=round(m.volume / 1000, 2),
        euler=int(m.euler_number),
        thick_p01=round(float(np.percentile(th, 1)), 2) if len(th) else None,
        thick_frac_below_1p2=round(float(np.mean(th < 1.2)), 4) if len(th) else None,
    )


# ------------------------------------------------------------- poses --------
def static_overlaps(mode):
    return [(a, b, round(v, 2)) for a, b, v in C.overlaps(K.pose_q(mode))]


def envelope_ball():
    out = C.outside_sphere(K.pose_q("ball"), r=P.R + 0.05)
    return {k: round(v, 2) for k, v in out.items() if v > 0.05}


def path_check(max_step_deg=1.5):
    """Adaptive sampling of the whole dino->ball sequence (both directions
    are the same set of states)."""
    q = K.pose_q("dino")
    hits, n_states = [], 0
    for name, target in K.SEQUENCE:
        start = dict(q)
        span = max(abs(v - start[j]) for j, v in target.items())
        steps = max(2, int(math.ceil(span / max_step_deg)))
        for i in range(1, steps + 1):
            t = i / steps
            for j, v in target.items():
                q[j] = start[j] + (v - start[j]) * t
            n_states += 1
            for a, b, v in C.overlaps(q):
                hits.append((name, round(t, 3), a, b, round(v, 2)))
    return hits, n_states


def jaw_sweep(step=1.0):
    """Open the jaw through its whole range in dinosaur mode."""
    lo, hi = K.JOINTS["jaw"]["range"]
    hits = []
    for a in np.arange(hi, lo - 1e-9, -step):
        q = K.pose_q("dino")
        q["jaw"] = float(a)
        hits += [(float(a), x, y, round(v, 3)) for x, y, v in C.overlaps(q)]
    return hits


# --------------------------------------------------------------- stops ------
STOP_TESTS = {
    # joint: (pose used for others, child part, parent part)
    "head": ("ball", "skull", "torso"),
    "jaw": ("dino", "jaw", "skull"),
    "tail1": ("ball", "tail1", "torso"),
    "tail2": ("ball", "tail2", "tail1"),
    "tail3": ("ball", "tail3", "tail2"),
    "arm_L": ("dino", "arm_L", "torso"),
    "thigh_L": ("dino", "thigh_L", "torso"),
    "shin_L": ("dino", "shin_L", "thigh_L"),
    "panel_L": ("ball", "panel_L", "polecap_L"),
}


def stop_check(scan=8.0, step=0.5):
    """For every joint: verify both ends of the range are free and find the
    angle at which the hard stop actually engages beyond each end."""
    res = {}
    for j, (mode, child, parent) in STOP_TESTS.items():
        lo, hi = K.JOINTS[j]["range"]

        def ov(val):
            q = K.pose_q(mode)
            if j in ("tail2", "tail3"):
                q.update({"tail1": 0, "tail2": 0, "tail3": 0})
            q[j] = val
            return sum(v for *_, v in C.overlaps(q, names=[child, parent], tol=0.05))

        row = {"range": (lo, hi), "free_at_lo": ov(lo) == 0, "free_at_hi": ov(hi) == 0}
        for end, sgn, lim in (("lo", -1, lo), ("hi", 1, hi)):
            hit = None
            d = step
            while d <= scan:
                if ov(lim + sgn * d) > 0:
                    hit = round(lim + sgn * d, 2)
                    break
                d += step
            row[f"stop_{end}_at"] = hit
        row["stops_ok"] = bool(row["free_at_lo"] and row["free_at_hi"] and
                               row["stop_lo_at"] is not None and row["stop_hi_at"] is not None and
                               abs(row["stop_lo_at"] - lo) <= 3.0 and abs(row["stop_hi_at"] - hi) <= 3.0)
        res[j] = row
    return res


# ------------------------------------------------------------ clearance -----
CLEAR_PAIRS = [("skull", "torso"), ("skull", "jaw"), ("tail1", "torso"), ("tail1", "tail2"),
               ("tail2", "tail3"), ("tail3", "torso"), ("thigh_L", "torso"),
               ("shin_L", "thigh_L"), ("shin_L", "rear_shell"), ("shin_L", "panel_L"),
               ("arm_L", "torso"), ("panel_L", "rear_shell"), ("panel_L", "torso"),
               ("slider_L", "torso"), ("slider_L", "panel_L"), ("skull", "panel_L"),
               ("thigh_L", "axle_L")]


def clearances(mode):
    g = C.gaps(K.pose_q(mode), CLEAR_PAIRS, search=5.0)
    return {f"{a}/{b}": round(v, 2) for (a, b), v in g.items()}


# ------------------------------------------------------------- mass ---------
def part_mass(m):
    shell_v = min(m.volume, m.area * SKIN)
    return PLA * (shell_v + INFILL * (m.volume - shell_v))


def mass_props(mode):
    M = AS.posed_meshes(K.pose_q(mode))
    tot, mom = 0.0, np.zeros(3)
    per = {}
    for n, m in M.items():
        mm = part_mass(m)
        per[n] = (mm, m.center_mass)
        tot += mm
        mom += mm * m.center_mass
    return tot, mom / tot, per, M


def standing(tilt_tol=0.3):
    tot, com, per, M = mass_props("dino")
    zmin = min(m.bounds[0, 2] for m in M.values())
    contact = {n: m for n, m in M.items() if m.bounds[0, 2] < zmin + tilt_tol}
    pts = np.vstack([m.vertices[m.vertices[:, 2] < zmin + tilt_tol][:, :2] for m in contact.values()])
    hull = ConvexHull(pts)
    eq = hull.equations          # a x + b y + c <= 0 inside
    margin = float(-np.max(eq[:, :2] @ com[:2] + eq[:, 2]))
    # tripod statics in the XZ plane (forces per side halved for joints)
    g = 9.81e-3
    W = {n: per[n][0] * g for n in M}
    feet = [n for n in contact if n.startswith("shin")]
    tailc = [n for n in contact if n.startswith("tail")]
    xt = float(np.mean(np.vstack([M[n].vertices[M[n].vertices[:, 2] < zmin + tilt_tol] for n in tailc])[:, 0])) if tailc else None
    upper = [n for n in M if not n.startswith(("thigh", "shin"))]
    W_up = sum(W[n] for n in upper)
    x_up = sum(W[n] * per[n][1][0] for n in upper) / W_up
    # torso balances on the hip pin + tail contact: moments about the hip (x=0)
    N_tail = W_up * x_up / xt if xt else 0.0
    knee_x = float(K.transforms(K.pose_q("dino"))["thigh_L"][:3, :3] @ np.array([K.KNEE[0], 0, K.KNEE[1]]))[0] \
        if False else float((K.transforms(K.pose_q("dino"))["thigh_L"] @ np.array([K.KNEE[0], 0, K.KNEE[1], 1]))[0])
    W_th = W["thigh_L"]
    x_th = per["thigh_L"][1][0]
    hip_load = (W_up - N_tail) / 2           # vertical load per hip
    tau_knee = (0 - knee_x) * (-hip_load) + (x_th - knee_x) * (-W_th)
    out_static = dict(
        tail_contact=bool(tailc), tail_contact_x=round(xt, 1) if xt else None,
        tail_load_N=round(N_tail, 4), tail_load_frac=round(N_tail / sum(W.values()), 3),
        upper_com_x=round(x_up, 2),
        hip_moment_needed_Nmm=0.0 if tailc and N_tail > 0 else round(x_up * W_up / 2, 3),
        knee_torque_Nmm=round(tau_knee, 3),
        knee_stop_carries=bool(tau_knee > 0),   # CCW on thigh -> shin pushed to q<0 (blocked)
    )
    return dict(
        mass_g=round(tot, 1), com=np.round(com, 2).tolist(), ground_z=round(zmin, 2),
        ground_contacts=sorted(contact), support_x=(round(pts[:, 0].min(), 1), round(pts[:, 0].max(), 1)),
        support_y=(round(pts[:, 1].min(), 1), round(pts[:, 1].max(), 1)),
        com_margin_mm=round(margin, 2), stable=bool(margin > 2.0), **out_static,
        length_mm=round(max(m.bounds[1, 0] for m in M.values()) - min(m.bounds[0, 0] for m in M.values()), 1),
        height_mm=round(max(m.bounds[1, 2] for m in M.values()) - zmin, 1),
        width_mm=round(max(m.bounds[1, 1] for m in M.values()) - min(m.bounds[0, 1] for m in M.values()), 1),
    )


# ------------------------------------------------------------- rolling ------
def rolling(n_dirs=6000):
    M = AS.posed_meshes(K.pose_q("ball"))
    allm = trimesh.util.concatenate(list(M.values()))
    i = np.arange(n_dirs) + 0.5
    phi = np.arccos(1 - 2 * i / n_dirs)
    th = np.pi * (1 + 5 ** 0.5) * i
    D = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    r = _outer_radius(allm, D)
    # sagittal great circle (forward roll about Y) and the side circle (roll about X)
    a = np.radians(np.arange(0, 360, 0.5))
    Ds = np.stack([np.cos(a), np.full_like(a, 0.02), np.sin(a)], 1)   # off the y=0 mesh seam
    rs = _outer_radius(allm, Ds)
    Dl = np.stack([np.zeros_like(a), np.cos(a), np.sin(a)], 1)
    rl = _outer_radius(allm, Dl)
    tot, com, _, _ = mass_props("ball")
    return dict(
        frac_r_ge_49=round(float(np.mean(r >= 49.0)), 4),
        frac_r_ge_46_5=round(float(np.mean(r >= 46.5)), 4),
        r_min=round(float(r.min()), 2), r_max=round(float(r.max()), 2),
        sagittal_frac_ge_49=round(float(np.mean(rs >= 49.0)), 4),
        sagittal_max_gap_deg=_max_gap(rs >= 49.0, 0.5),
        lateral_frac_ge_46_5=round(float(np.mean(rl >= 46.5)), 4),
        lateral_max_gap_deg=_max_gap(rl >= 46.5, 0.5),
        com_offset_mm=round(float(np.linalg.norm(com)), 2), com=np.round(com, 2).tolist(),
        mass_g=round(tot, 1),
    )


def _outer_radius(m, D):
    O = np.zeros_like(D)
    locs, idx, _ = m.ray.intersects_location(O, D, multiple_hits=True)
    r = np.zeros(len(D))
    d = np.linalg.norm(locs, axis=1)
    np.maximum.at(r, idx, d)
    return r


def _max_gap(mask, step):
    if mask.all():
        return 0.0
    m = np.concatenate([mask, mask])
    best = run = 0
    for v in m:
        run = 0 if v else run + 1
        best = max(best, run)
    return round(min(best, len(mask)) * step, 1)
