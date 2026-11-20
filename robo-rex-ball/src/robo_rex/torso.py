"""Central core: carries the axle, every pivot, the dorsal skin, the belly
skin and the latch channel."""
import math
import cadquery as cq
from . import params as P
from .geom import sector, disc, d_disc, ball, pol, mirror_y
from .hinges import knuckle_parent, c_hub_stop, radial_cyl
from .kinematics import LEG_BALL, ARM_BALL

HIP_POST = (200.0, 232.0)     # torso post that limits thigh rotation
SHOULDER_POST = (140.0, 172.0)
HIP_RING = (8.0, 15.0)
SHOULDER_RING = (5.0, 8.2)
BRIDGE_PINS = (87.0, 103.0)


def _local_box(t0, t1, r0, r1, y0, y1, phi):
    """Box given in (tangential, radial) coords about direction phi."""
    b = cq.Workplane().box(r1 - r0, y1 - y0, t1 - t0).translate(
        (0.5 * (r0 + r1), 0.5 * (y0 + y1), 0.5 * (t0 + t1)))
    return b.rotate((0, 0, 0), (0, 1, 0), -phi)


def latch_channel():
    s = P.SLIDE
    w = P.LATCH_W / 2
    # thumb-head slots stop 4.4 mm from the centreline so the rolling spine
    # stays closed; the flange channel runs underneath, full width
    top = _local_box(-w - s, w + s, 48.2, 52.0, 4.4, 10, P.LATCH_PHI).union(
        _local_box(-w - s, w + s, 48.2, 52.0, -10, -4.4, P.LATCH_PHI))
    fl = _local_box(-w - 1.5 - s, w + 1.5 + s, 46.0, 48.4, -10, 10, P.LATCH_PHI)
    groove = _local_box(-1.25, 1.25, 44.9, 46.1, -10, 10, P.LATCH_PHI)
    return top.union(fl).union(groove)


def detent_bumps():
    """0.3 mm bumps in the slider groove: slider peg clicks over them."""
    out = None
    for sgn in (1, -1):
        b = _local_box(-1.3, 1.3, 44.8, 45.6, sgn * 7.0 - 0.4, sgn * 7.0 + 0.4, P.LATCH_PHI)
        out = b if out is None else out.union(b)
    return out


def torso():
    y = P.CB
    g = P.ANG_GAP / 2
    band = disc(0, 0, P.R_CORE, -y, y)
    band = band.union(sector(P.R_CORE - 1, P.R + 1, P.PHI_HEAD_DORSAL + g,
                             P.PHI_DORSAL_TAIL - g, -y, y))
    band = band.union(sector(P.R_CORE - 1, P.R + 1, P.PHI_TAIL_BELLY + g,
                             360 + P.PHI_BELLY_HEAD - g, -y, y))
    band = band.intersect(ball(P.R))
    t = band.union(disc(0, 0, 7.0, -P.Y_HUB, P.Y_HUB))

    # stop posts (hip: both sides, shoulder: both sides)
    for sgn in (1, -1):
        _, hp = c_hub_stop((0, 0), *HIP_RING, y - 0.5, P.Y_HUB, HIP_POST,
                           (LEG_BALL[0], 0.0))
        _, sp = c_hub_stop(P.SHOULDER, *SHOULDER_RING, y - 0.5, P.Y_ARM[1],
                           SHOULDER_POST, (0.0, ARM_BALL))
        if sgn < 0:
            hp, sp = mirror_y(hp), mirror_y(sp)
        t = t.union(hp).union(sp)

    # axle bore: D-keyed press fit for both axle halves
    t = t.cut(d_disc(0, 0, P.AXLE_D, -20, 20, flat_phi=-90, flat=0.5))
    # rear shell bridge seat + radial pins
    seat = ball(P.R_FP_IN).cut(ball(P.R_RS_IN - 0.4)).intersect(
        sector(0, 60, P.BRIDGE_PHI[0] - 0.5, P.BRIDGE_PHI[1] + 0.5, -10, 10))
    t = t.cut(seat)
    for ph in BRIDGE_PINS:
        t = t.cut(radial_cyl(ph, 39.0, 51.0, 3.0))
    # knuckle forks for head and tail
    t = knuckle_parent(t, P.PHI_HEAD_DORSAL, P.HEAD_DINO)
    t = knuckle_parent(t, P.PHI_DORSAL_TAIL, P.TAIL_DINO[0])
    # shoulder pin blind holes (press)
    sx, sz = P.SHOULDER
    for sgn in (1, -1):
        h = d_disc(sx, sz, P.PIN_D, 3.5, 9.5, flat_phi=-90, flat=0.4)
        t = t.cut(h if sgn > 0 else mirror_y(h))
    # latch channel and detents
    t = t.cut(latch_channel())
    t = t.union(detent_bumps())
    # decorative belly armour grooves (0.6 mm deep, keep rolling surface)
    for ph in (262.0, 284.0, 326.0):
        t = t.cut(sector(P.R - 0.6, P.R + 1, ph - 0.6, ph + 0.6, -10, 10))
    # dorsal grooves
    for ph in (66.0, 120.0):
        t = t.cut(sector(P.R - 0.6, P.R + 1, ph - 0.6, ph + 0.6, -10, 10))
    return t


def slider():
    """Latch slider for the +Y side, modelled in the unlocked position."""
    s = P.SLIDE
    w = P.LATCH_W / 2
    y0 = 1.0
    head = _local_box(-w, w, 47.5, 52.0, y0 + 3.8 + s, y0 + 8.0, P.LATCH_PHI)
    fl = _local_box(-w - 1.5, w + 1.5, 46.0 + s, 48.4 - s, y0, y0 + 4.4, P.LATCH_PHI)
    peg = _local_box(-0.9, 0.9, 45.3, 46.6, y0, y0 + 1.6, P.LATCH_PHI)
    sl = head.union(fl).union(peg).intersect(ball(P.R)).intersect(
        ball(P.R).translate((0, -P.LATCH_TRAVEL, 0)))   # flush when locked
    for k in range(2):   # thumb grip grooves
        yy = y0 + 5.4 + 1.4 * k
        sl = sl.cut(_local_box(-w - 1, w + 1, P.R - 0.5, P.R + 1, yy - 0.4, yy + 0.4,
                               P.LATCH_PHI))
    return sl


def bridge_pin():
    from .hinges import d_pin
    return d_pin(10.5, d=3.0)
