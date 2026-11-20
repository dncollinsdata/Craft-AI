"""Legs (thigh + shin/foot) and arms, modelled in the standing pose for the
+Y side.  The -Y side is the mirror image."""
import math
import cadquery as cq
from . import params as P
from .geom import sector, disc, d_disc, pol, prism_xz
from .hinges import c_hub_stop
from .kinematics import KNEE, ANKLE, LEG_BALL, ARM_BALL
from .torso import HIP_POST, HIP_RING, SHOULDER_POST, SHOULDER_RING


def _bar(p0, p1, w0, w1, y0, y1):
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dz)
    nx, nz = -dz / L, dx / L
    pts = [(p0[0] + nx * w0 / 2, p0[1] + nz * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + nz * w1 / 2),
           (p1[0] - nx * w1 / 2, p1[1] - nz * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - nz * w0 / 2)]
    return prism_xz(pts, y0, y1)


# ------------------------------------------------------------------ thigh --
def thigh():
    y0, y1 = P.Y_THIGH
    t = disc(0, 0, 11.0, y0, y1)                      # big mechanical thigh hub
    t = t.union(_bar((0, 0), KNEE, 16.0, 11.0, y0, y1))
    t = t.union(disc(*KNEE, 6.5, y0, y1))
    t = t.union(disc(0, 0, 6.0, y1 - 0.1, P.Y_SLEEVE_END))   # axle sleeve
    ring, _ = c_hub_stop((0, 0), *HIP_RING, P.Y_ARM[0], y0 + 0.1, HIP_POST, (LEG_BALL[0], 0.0))
    t = t.union(ring)
    t = t.cut(disc(0, 0, (P.AXLE_D + 0.4) / 2, 0, P.R))
    t = t.cut(d_disc(*KNEE, P.PIN_D, y0 - 1, y1 + 1, flat_phi=P.THIGH_DIR, flat=0.4))
    # piston-style decoration: recessed slots on the outer face
    for k, f in enumerate((0.38, 0.62)):
        cx, cz = KNEE[0] * f, KNEE[1] * f
        t = t.cut(disc(cx, cz, 2.2, y1 - 0.8, y1 + 1))
    for a in range(0, 360, 60):
        cx, cz = pol(8.5, a)
        t = t.cut(disc(cx, cz, 1.0, y0 - 1, y0 + 0.7))   # rivet ring, inner face
    return t


# ------------------------------------------------------------- shin + foot --
KNEE_POST = (50.0, 174.0)     # angular extent of the thigh bar seen from the knee


def shin():
    y0, y1 = P.Y_SHIN
    s = disc(*KNEE, 6.5, y0, y1)
    s = s.union(_bar(KNEE, ANKLE, 11.0, 9.0, y0, y1))
    s = s.union(disc(*ANKLE, 5.5, y0, y1))
    ring, _ = c_hub_stop(KNEE, 6.9, 10.2, P.Y_THIGH[0] + 0.4, y0 + 0.1, KNEE_POST,
                         (0.0, LEG_BALL[1]))
    s = s.union(ring)
    # foot: body + three blunt clawed toes + heel spur
    ax, az = ANKLE
    zs = az - P.FOOT_DROP
    fy0, fy1 = P.Y_FOOT
    body = prism_xz([(ax - P.FOOT_HEEL, zs), (ax + 8, zs), (ax + 8, zs + 5.0),
                     (ax + 2, az + 2.5), (ax - 6, az + 2.5), (ax - P.FOOT_HEEL, zs + 3.5)],
                    fy0, fy1)
    s = s.union(body)
    toes = [((fy0 + fy1) / 2 - 1.6, (fy0 + fy1) / 2 + 1.6, P.FOOT_TOE),
            (fy0, fy0 + 3.0, P.FOOT_TOE - 4.0), (fy1 - 3.0, fy1, P.FOOT_TOE - 4.0)]
    for ta, tb, L in toes:
        toe = prism_xz([(ax + 6, zs), (ax + L - 1.5, zs), (ax + L, zs + 1.5),
                        (ax + L - 2.5, zs + 3.4), (ax + 6, zs + 4.6)], ta, tb)
        s = s.union(toe)
    s = s.union(prism_xz([(ax - P.FOOT_HEEL - 3.5, zs), (ax - P.FOOT_HEEL + 1, zs),
                          (ax - P.FOOT_HEEL + 1, zs + 3.0)], fy0 + 3.5, fy1 - 3.5))
    # knee pin: round running hole + counterbore for the pin head on the outside
    s = s.cut(disc(*KNEE, (P.PIN_D + P.CLR) / 2, y0 - 8, y1 + 1))
    s = s.cut(disc(*KNEE, 3.7, y1 - 1.2, y1 + 1))
    # shin armour groove
    s = s.cut(_bar((KNEE[0] * 0.7 + ANKLE[0] * 0.3, KNEE[1] * 0.7 + ANKLE[1] * 0.3),
                   (KNEE[0] * 0.25 + ANKLE[0] * 0.75, KNEE[1] * 0.25 + ANKLE[1] * 0.75),
                   1.2, 1.2, y1 - 0.6, y1 + 1))
    return s


# ------------------------------------------------------------------- arm ---
def arm():
    y0, y1 = P.Y_ARM
    sx, sz = P.SHOULDER
    elbow = (sx + pol(9.0, -95)[0], sz + pol(9.0, -95)[1])
    wrist = (elbow[0] + pol(9.5, -15)[0], elbow[1] + pol(9.5, -15)[1])
    a = disc(sx, sz, 4.7, y0, y1)
    ring, _ = c_hub_stop(P.SHOULDER, 4.6, SHOULDER_RING[1], y0, y1, SHOULDER_POST, (0.0, ARM_BALL))
    a = a.union(ring)
    a = a.union(_bar((sx, sz), elbow, 6.0, 5.0, y0, y1)).union(disc(*elbow, 2.8, y0, y1))
    a = a.union(_bar(elbow, wrist, 5.0, 4.2, y0, y1))
    # two blunt fingers
    for fa in (-35.0, 5.0):
        tip = (wrist[0] + pol(4.5, fa)[0], wrist[1] + pol(4.5, fa)[1])
        a = a.union(_bar(wrist, tip, 2.6, 1.8, y0 + 0.6, y1 - 0.6))
        a = a.union(disc(*tip, 0.9, y0 + 0.6, y1 - 0.6))
    a = a.cut(disc(sx, sz, (P.PIN_D + P.CLR) / 2, y0 - 1, y1 + 1))
    a = a.cut(disc(sx, sz, 3.7, y1 - 1.2, y1 + 1))
    return a


def knee_pin():
    from .hinges import d_pin
    # shank runs from inside the thigh (press) through the shin; head outside
    return d_pin(P.Y_SHIN[1] - 1.2 - (P.Y_THIGH[0] + 0.5), head_d=7.0)


def shoulder_pin():
    from .hinges import d_pin
    return d_pin(P.Y_ARM[1] - 1.2 - 4.0, head_d=7.0)
