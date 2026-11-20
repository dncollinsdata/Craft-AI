"""Kinematic model: every moving part, its pivot, axis, range, poses, stops.

All revolute axes are parallel to +Y, so a joint is fully described by a pivot
(x, z) and an angle.  Positive angles are counter-clockwise in the XZ plane
(+X rotates towards +Z).  Each part's geometry is modelled at q = 0 ("home");
`ball` and `dino` give the joint angle in each mode.  Pivots are expressed in
world coordinates with every ancestor at its own home.
"""
import numpy as np
from . import params as P
from .geom import pol

_PH = pol(P.R_KNUCKLE, P.PHI_HEAD_DORSAL)
_PT1 = pol(P.R_KNUCKLE, P.PHI_DORSAL_TAIL)
_PT2 = pol(P.R_KNUCKLE, P.PHI_TAIL_12)
_PT3 = pol(P.R_KNUCKLE, P.PHI_TAIL_23)
JAW_PIVOT = pol(39.5, 42.0)
KNEE = pol(P.THIGH_L, P.THIGH_DIR)
ANKLE = (KNEE[0] + pol(P.SHIN_L, P.SHIN_DIR)[0], KNEE[1] + pol(P.SHIN_L, P.SHIN_DIR)[1])

# Ball-mode leg/arm angles were found with scripts/search_folds.py (collision
# search inside the envelope) and are frozen here.
LEG_BALL = (-54.0, 184.0)
LEG_MID = (-54.0, 64.0)        # waypoint from scripts/plan_leg_path.py      # (hip, knee) rotation from standing pose
ARM_BALL = 75.0

JOINTS = {
    #  name        parent    pivot      home  ball    dino   (min, max)   axis
    "head":    dict(parent="torso", pivot=_PH, ball=0.0, dino=P.HEAD_DINO,
                    range=(0.0, P.HEAD_DINO), home="ball"),
    "jaw":     dict(parent="head", pivot=JAW_PIVOT, ball=0.0, dino=0.0,
                    range=(P.JAW_OPEN, 0.0), home="closed"),
    "tail1":   dict(parent="torso", pivot=_PT1, ball=0.0, dino=P.TAIL_DINO[0],
                    range=(P.TAIL_DINO[0], 0.0), home="ball"),
    "tail2":   dict(parent="tail1", pivot=_PT2, ball=0.0, dino=P.TAIL_DINO[1],
                    range=(P.TAIL_DINO[1], 0.0), home="ball"),
    "tail3":   dict(parent="tail2", pivot=_PT3, ball=0.0, dino=P.TAIL_DINO[2],
                    range=(P.TAIL_DINO[2], 0.0), home="ball"),
    "arm_L":   dict(parent="torso", pivot=P.SHOULDER, ball=ARM_BALL, dino=0.0,
                    range=(0.0, ARM_BALL), home="dino"),
    "arm_R":   dict(parent="torso", pivot=P.SHOULDER, ball=ARM_BALL, dino=0.0,
                    range=(0.0, ARM_BALL), home="dino"),
    "thigh_L": dict(parent="torso", pivot=(0.0, 0.0), ball=LEG_BALL[0], dino=-P.DINO_PITCH,
                    range=(LEG_BALL[0], 0.0), home="dino"),
    "thigh_R": dict(parent="torso", pivot=(0.0, 0.0), ball=LEG_BALL[0], dino=-P.DINO_PITCH,
                    range=(LEG_BALL[0], 0.0), home="dino"),
    "shin_L":  dict(parent="thigh_L", pivot=KNEE, ball=LEG_BALL[1], dino=0.0,
                    range=(0.0, LEG_BALL[1]), home="dino"),
    "shin_R":  dict(parent="thigh_R", pivot=KNEE, ball=LEG_BALL[1], dino=0.0,
                    range=(0.0, LEG_BALL[1]), home="dino"),
    "panel_L": dict(parent="torso", pivot=(0.0, 0.0), ball=0.0, dino=P.FP_DINO,
                    range=(0.0, P.FP_DINO), home="ball"),
    "panel_R": dict(parent="torso", pivot=(0.0, 0.0), ball=0.0, dino=P.FP_DINO,
                    range=(0.0, P.FP_DINO), home="ball"),
}
# prismatic latch sliders (move along +/-Y)
SLIDERS = {"slider_L": +1, "slider_R": -1}
SLIDER_POSE = {"ball": P.LATCH_TRAVEL, "dino": 0.0}

# Parts rigidly attached to a joint body (pins live in the part they are
# press-fitted into).
ATTACH = {
    "rear_shell": "torso", "axle_L": "torso", "axle_R": "torso",
    "polecap_L": "torso", "polecap_R": "torso",
}


def rot_matrix(pivot, ang):
    a = np.radians(ang)
    c, s = np.cos(a), np.sin(a)
    px, pz = pivot
    M = np.eye(4)
    M[0, 0], M[0, 2], M[2, 0], M[2, 2] = c, -s, s, c
    M[0, 3] = px - c * px + s * pz
    M[2, 3] = pz - s * px - c * pz
    return M


def pose_q(mode):
    q = {j: d[mode] for j, d in JOINTS.items()}
    q["pitch"] = P.DINO_PITCH if mode == "dino" else 0.0
    q.update({s: SLIDER_POSE[mode] for s in SLIDERS})
    return q


def transforms(q):
    """World transform (4x4) of every body for joint values q."""
    # "pitch" orients the whole toy in the world (dino stance); it has no
    # effect on relative positions, so collisions are independent of it.
    T = {"torso": rot_matrix((0.0, 0.0), q.get("pitch", 0.0))}

    def get(name):
        if name in T:
            return T[name]
        if name in SLIDERS:
            M = np.eye(4)
            M[1, 3] = SLIDERS[name] * q.get(name, 0.0)
            T[name] = get("torso") @ M
            return T[name]
        if name in ATTACH:
            T[name] = get(ATTACH[name])
            return T[name]
        j = JOINTS[name]
        T[name] = get(j["parent"]) @ rot_matrix(j["pivot"], q.get(name, 0.0))
        return T[name]

    for n in list(JOINTS) + list(SLIDERS) + list(ATTACH):
        get(n)
    return T


# Transformation sequence, DINO -> BALL.  Each phase moves the listed joints
# linearly from their current value to the target.  Ball -> dino is the
# exact reverse.
SEQUENCE = [
    ("pick up and level body", {"pitch": 0.0}),
    ("close jaw", {"jaw": 0.0}),
    ("fold head down", {"head": 0.0}),
    ("curl tail", {"tail1": 0.0, "tail2": 0.0, "tail3": 0.0}),
    ("tuck arms", {"arm_L": ARM_BALL, "arm_R": ARM_BALL}),
    ("swing legs back", {"thigh_L": LEG_MID[0], "thigh_R": LEG_MID[0],
                         "shin_L": LEG_MID[1], "shin_R": LEG_MID[1]}),
    ("fold knees", {"thigh_L": LEG_BALL[0], "thigh_R": LEG_BALL[0],
                    "shin_L": LEG_BALL[1], "shin_R": LEG_BALL[1]}),
    ("close armour", {"panel_L": 0.0, "panel_R": 0.0}),
    ("slide latches", {"slider_L": P.LATCH_TRAVEL, "slider_R": P.LATCH_TRAVEL}),
]


def sequence_samples(steps_per_phase=12):
    """Yield (phase_name, t, q) along the dino->ball path."""
    q = pose_q("dino")
    yield ("dino", 0.0, dict(q))
    for name, target in SEQUENCE:
        start = dict(q)
        for i in range(1, steps_per_phase + 1):
            t = i / steps_per_phase
            for j, v in target.items():
                q[j] = start[j] + (v - start[j]) * t
            yield (name, t, dict(q))
