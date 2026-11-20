"""ROBO REX BALL - single source of truth for every dimension.

Coordinate frame ("ball frame", fixed to the torso):
  origin = ball centre, +X = dinosaur forward, +Y = dinosaur left, +Z = up.
  Every joint in this toy rotates about an axis parallel to Y, so all
  kinematics are planar in XZ.  Angles ("phi") are measured in the XZ plane,
  counter-clockwise when looking from +Y... i.e. phi=0 is +X, phi=90 is +Z.

All lengths in millimetres, all angles in degrees.
Change values here and regenerate; every part is derived from them.
"""

# ---------------------------------------------------------------- sphere ----
R = 50.0                 # outer ball radius (100 mm ball)
T_OUT = 2.8              # front armour panel thickness
GAP = 0.4                # radial gap between nested shells
T_IN = 2.0               # rear shell thickness
R_FP_IN = R - T_OUT                  # 47.2 front panel inner radius
R_RS_OUT = R_FP_IN - GAP             # 46.8 rear shell outer radius
R_RS_IN = R_RS_OUT - T_IN            # 44.8 rear shell inner radius
R_ENV = R_RS_IN - GAP                # 44.4 envelope for folded side-band parts

# ------------------------------------------------------- clearances --------
CLR = 0.3                # moving joint clearance (diametral, on pins)
CLR_FACE = 0.4           # axial gap between rotating faces
SLIDE = 0.35             # sliding clearance (latch slider)
ANG_GAP = 1.0            # angular gap between centre-band skin parts (deg)
MIN_WALL = 1.6

# ------------------------------------------------------------- y layers ----
CB = 9.0                 # centre band half width (torso, head, tail)
Y_PANEL = 9.4            # inner edge of side armour (|y|)
Y_ARM = (9.4, 14.0)      # arm layer
Y_HUB = 14.6             # torso hub half length
Y_THIGH = (15.0, 22.0)   # thigh layer
Y_SHIN = (22.4, 29.4)    # shin layer
Y_FOOT = (22.4, 33.0)    # foot layer
Y_SLEEVE_END = 44.4      # end of thigh sleeve on the axle

# ------------------------------------------------- centre band tiling ------
# Angular boundaries of the parts that form the rolling "spine" band.
PHI_BELLY_HEAD = -14.0
PHI_HEAD_DORSAL = 52.0
PHI_DORSAL_TAIL = 125.0
PHI_TAIL_12 = 125.0 + 115.0 / 3
PHI_TAIL_23 = 125.0 + 2 * 115.0 / 3
PHI_TAIL_BELLY = 240.0
R_SKIN_IN = 27.6         # inner radius of head / tail sectors
R_CORE = 27.2            # torso core disc radius

R_KNUCKLE = 46.3         # radius of head/tail hinge pins (near the skin)
PIN_D = 4.0              # standard hinge pin diameter
KNUCKLE_R = 4.4          # tongue disc radius around a knuckle pin
TONGUE_T = 5.6           # tongue thickness (|y| <= 2.8)

# ----------------------------------------------------------- axle ----------
AXLE_D = 8.0
AXLE_Y = (1.0, 47.6)     # each axle half spans this |y| range
POLE_CB_R = 8.3          # counterbore radius at the poles
POLE_CB_FLOOR = 47.8     # y of counterbore floor
EAR_R = 13.0             # radius of the front panel hinge ear boss
EAR_Y0 = 45.0            # inner face of ear boss
RS_POLE_HOLE = 13.6      # clearance hole in rear shell around the ear
CAP_LUG = (8.0, 10.0, 4.0)   # pole cap stop lug: r_in, r_out, width
CAP_LUG_PHI = -90.0      # direction of the fixed lug (ball frame)

# ------------------------------------------------------- armour ------------
FP_PHI = (-128.0, 70.0)  # front panel coverage in ball mode
RS_LIP = 12.0            # rear shell lip under the front panels (deg)
RS_LIP_BOTTOM = 4.0      # short lip at the bottom keeps the legs' exit clear
RS_PHI = (FP_PHI[1] - RS_LIP, FP_PHI[0] + 360 + RS_LIP_BOTTOM)   # (58, 236)
BRIDGE_PHI = (78.0, 112.0)   # rear shell centre bridge (under dorsal skin)
FP_DINO = 150.0          # front panel rotation into dinosaur mode (folds back like a carapace)

# ------------------------------------------------------- latch -------------
LATCH_PHI = 300.0        # slider location on the belly
LATCH_W = 8.0            # slider width along the surface
LATCH_TRAVEL = 3.6
LATCH_LEN = 7.6          # slider length along y

# --------------------------------------------------------- joints ----------
# head: pivot at the outer corner of the head/dorsal boundary
HEAD_DINO = 40.0         # head rotation ball -> dino (CCW, deg)
JAW_OPEN = -30.0         # jaw opening (deg, relative to skull)
TAIL_DINO = (-20.0, -30.0, -30.0)   # tail joint rotations ball -> dino (at stops)
DINO_PITCH = 25.75       # body pitched nose-up in dino mode so the tail tip
                         # rests on the ground (tripod stance)

# legs (modelled in dinosaur pose)
THIGH_L = 26.0
SHIN_L = 32.0
THIGH_DIR = -68.0
SHIN_DIR = -105.0
FOOT_DROP = 6.5          # ankle centre to sole
FOOT_HEEL = 15.0
FOOT_TOE = 21.0

# arms (modelled in dinosaur pose)
SHOULDER = (25.0, 6.0)   # x, z
ARM_L = 19.0
ARM_DIR = -50.0

# ------------------------------------------------------- printing ----------
BED = (220.0, 220.0, 250.0)
NOZZLE = 0.4
LAYER = 0.2
