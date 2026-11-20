"""Search ball-mode fold angles for the legs and arms.

Stop features are disabled during the search (they are sized afterwards from
the chosen angles).  A configuration is accepted only if the leg (or arm) has
zero interference with every other body in ball mode, then the candidate with
the largest minimum clearance is reported.
"""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from robo_rex import hinges
hinges.STOPS_ENABLED = False
from robo_rex import kinematics as K, collide as C
from robo_rex import torso as T, armor as A, legs as L, hinges as HG

print("building geometry (stops disabled)...")
obst = {
    "torso": C.from_solid(T.torso()),
    "rear_shell": C.from_solid(A.rear_shell()),
    "panel_L": C.from_solid(A.front_panel()),
    "axle_L": C.from_solid(HG.axle()),
}
sl = C.from_solid(T.slider()).translate([0, K.SLIDER_POSE["ball"], 0])
obst["slider_L"] = sl
thigh, shin, arm = C.from_solid(L.thigh()), C.from_solid(L.shin()), C.from_solid(L.arm())


def leg_eval(qh, qk):
    Th = K.rot_matrix((0, 0), qh)
    Ts = Th @ K.rot_matrix(K.KNEE, qk)
    t, s = C.xf(thigh, Th), C.xf(shin, Ts)
    v = sum((t ^ o).volume() + (s ^ o).volume() for o in obst.values()) + (t ^ s).volume()
    return v, t, s


best = []
for qh in np.arange(-60, 181, 5.0):
    for qk in np.arange(150, 195, 2.0):
        v, t, s = leg_eval(qh, qk)
        if v < 0.5:
            # bearing pairs (axle, knee lap face) excluded: their gap is fixed by design
            g = min(min(t.min_gap(o, 3), s.min_gap(o, 3))
                    for k, o in obst.items() if k not in ("axle_L", "torso"))
            g = min(g, s.min_gap(obst["torso"], 3), s.min_gap(obst["axle_L"], 3))
            best.append((g, qh, qk))
best.sort(reverse=True)
print("feasible leg folds:", len(best))
for b in best[:12]:
    print("  gap %.2f  hip %+.0f  knee %+.0f" % b)

# ------------------------------------------------------------------ arms ---
QH, QK = K.LEG_BALL
v, t, s = leg_eval(QH, QK)
obst_a = dict(obst, thigh_L=t, shin_L=s)
res = []
for qa in np.arange(-120, 181, 5.0):
    a = C.xf(arm, K.rot_matrix(K.JOINTS["arm_L"]["pivot"], qa))
    vol = sum((a ^ o).volume() for o in obst_a.values())
    if vol < 0.5:
        g = min(a.min_gap(o, 3) for k, o in obst_a.items() if k != "torso")
        res.append((g, qa))
res.sort(reverse=True)
print("feasible arm tucks:", len(res), " best:", [("%.2f" % g, q) for g, q in res[:10]])
