"""Plan a collision-free (hip, knee) path for the leg fold with the armour
open.  Builds a joint-space occupancy grid using the real meshes (stops
enabled) and runs a breadth-first search from standing to folded."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from collections import deque
import numpy as np
from robo_rex import hinges
hinges.STOPS_ENABLED = False      # stops are sized from the planned path afterwards
from robo_rex import kinematics as K, collide as C
from robo_rex import torso as T, armor as A, legs as L, hinges as HG, head as HD, tail as TL

q0 = K.pose_q("dino")
q0["pitch"] = 0.0   # plan in the torso frame
q0.update({"head": 0.0, "tail1": 0.0, "tail2": 0.0, "tail3": 0.0,
           "arm_L": K.ARM_BALL, "arm_R": K.ARM_BALL})
Tm = K.transforms(q0)
src = {"torso": T.torso(), "rear_shell": A.rear_shell(), "panel_L": A.front_panel(),
       "axle_L": HG.axle(), "arm_L": L.arm(), "skull": HD.skull(), "jaw": HD.jaw(),
       "tail1": TL.tail_segment(1), "tail2": TL.tail_segment(2), "tail3": TL.tail_segment(3)}
body = {"skull": "head"}
M = {n: C.xf(C.from_solid(w), Tm[body.get(n, n)]) for n, w in src.items()}
th, sh = C.from_solid(L.thigh()), C.from_solid(L.shin())
STEP = 4.0
HMIN = float(os.environ.get("HIP_MIN", -100))
H0 = K.JOINTS["thigh_L"]["dino"]
H = H0 + STEP * np.arange(int((HMIN - H0) / STEP), int((180 - H0) / STEP) + 1)
Kn = np.arange(-8, 196 + 1e-6, STEP)


def free(qh, qk):
    Th = K.rot_matrix((0, 0), qh)
    t = C.xf(th, Th)
    s = C.xf(sh, Th @ K.rot_matrix(K.KNEE, qk))
    for o in M.values():
        if (t ^ o).volume() > 0.5 or (s ^ o).volume() > 0.5:
            return False
    return (t ^ s).volume() <= 0.5


grid = np.zeros((len(H), len(Kn)), bool)
for i, qh in enumerate(H):
    for j, qk in enumerate(Kn):
        grid[i, j] = free(qh, qk)
start = (int(np.argmin(abs(H - H0))), int(np.argmin(abs(Kn - 0))))
if os.environ.get("GOAL"):
    gh, gk = map(float, os.environ["GOAL"].split(","))
else:
    gh, gk = K.LEG_BALL
goal = (int(np.argmin(abs(H - gh))), int(np.argmin(abs(Kn - gk))))
print("free cells %d / %d, start free %s, goal free %s" % (grid.sum(), grid.size, grid[start], grid[goal]))
prev = {start: None}
dq = deque([start])
while dq:
    c = dq.popleft()
    if c == goal:
        break
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (c[0] + di, c[1] + dj)
        if 0 <= n[0] < len(H) and 0 <= n[1] < len(Kn) and grid[n] and n not in prev:
            prev[n] = c
            dq.append(n)
if goal not in prev:
    print("NO PATH")
    sys.exit(1)
path, c = [], goal
while c is not None:
    path.append((float(H[c[0]]), float(Kn[c[1]])))
    c = prev[c]
path.reverse()
# compress to waypoints where direction changes
wp = [path[0]]
for a, b, c in zip(path, path[1:], path[2:]):
    if (b[0] - a[0], b[1] - a[1]) != (c[0] - b[0], c[1] - b[1]):
        wp.append(b)
wp.append(path[-1])
print("waypoints (hip, knee):", wp)
