"""Folding head (skull) and independently hinged jaw.

Both are modelled in ball mode (q = 0).  The skull's outer face is part of the
rolling sphere; in dinosaur mode that face becomes the armoured top of the
skull.  The jaw is the inner part of the head and hinges at the back.
"""
import cadquery as cq
from . import params as P
from .geom import sector, disc, d_disc, ball, pol, rot, slab_y, shell
from .hinges import knuckle_child, c_hub_stop
from .kinematics import JAW_PIVOT

R_SPLIT = 37.0
RAMUS = (37.0, 43.6, 5.6)      # phi start, outer radius, half thickness
RAMUS_END = 47.0
JAW_PIN_D = 3.0
TEETH_SKULL = (2.0, 11.0, 20.0, 29.0)
TEETH_JAW = (6.5, 15.5, 24.5)
JAW_POST = (40.0, 80.0)        # skull stop post direction around the jaw pin
JAW_STOP_R = (3.4, 5.8)


def _head_blank():
    g = P.ANG_GAP / 2
    h = sector(P.R_SKIN_IN, P.R + 1, P.PHI_BELLY_HEAD + g, P.PHI_HEAD_DORSAL - g,
               -P.CB, P.CB).intersect(ball(P.R))
    # stepped armour chamfer along both top edges
    h = h.cut(shell(P.R - 1.5, P.R + 2).intersect(slab_y(P.CB - 1.5, 20)))
    h = h.cut(shell(P.R - 1.5, P.R + 2).intersect(slab_y(-20, -P.CB + 1.5)))
    return knuckle_child(h, P.PHI_HEAD_DORSAL, P.HEAD_DINO)


def _jaw_region(c=0.0):
    g = P.ANG_GAP / 2
    lo = sector(P.R_SKIN_IN - 1, R_SPLIT + c, P.PHI_BELLY_HEAD + g - 2,
                P.PHI_HEAD_DORSAL + 2, -P.CB - 1, P.CB + 1)
    a0, r1, t = RAMUS
    ram = sector(R_SPLIT - 1, r1 + c, a0 - c * 3, RAMUS_END + c * 3, -t - c, t + c)
    reg = lo.union(ram)
    for ph in TEETH_JAW:       # jaw teeth rise into the skull
        for s in (1, -1):
            reg = reg.union(sector(R_SPLIT - 1, R_SPLIT + 1.6 + c, ph - 2.4 - c * 3,
                                   ph + 2.4 + c * 3, *(sorted((s * (5.6 - c), s * (P.CB + 1))))))
    return reg


def _skull_teeth(c=0.0):
    out = None
    for ph in TEETH_SKULL:
        for s in (1, -1):
            t = sector(R_SPLIT - 1.6 - c, R_SPLIT + 1, ph - 2.4 - c * 3, ph + 2.4 + c * 3,
                       *(sorted((s * (5.6 - c), s * (P.CB + 1)))))
            out = t if out is None else out.union(t)
    return out


def _jaw_sweep(c):
    reg = _jaw_region(c)
    sweep = reg
    for a in (-6, -12, -18, -24, -31):
        sweep = sweep.union(rot(reg, JAW_PIVOT, a))
    return sweep


def skull():
    h = _head_blank()
    jaw_sweep = _jaw_sweep(0.3).cut(_skull_teeth())
    s = h.cut(jaw_sweep)
    _, post = c_hub_stop(JAW_PIVOT, *JAW_STOP_R, -6.2, 6.2, JAW_POST, (P.JAW_OPEN, 0.0))
    s = s.union(post.intersect(h))
    s = s.cut(d_disc(*JAW_PIVOT, JAW_PIN_D, -P.CB - 1, P.CB + 1, flat_phi=0, flat=0.4))
    # eyes: recessed sockets with a pupil boss, under a proud brow ridge
    ex, ez = pol(44.5, 30.0)
    for s_ in (1, -1):
        y0, y1 = sorted((s_ * (P.CB - 1.4), s_ * (P.CB + 1)))
        s = s.cut(disc(ex, ez, 3.3, y0, y1))
        y0, y1 = sorted((s_ * (P.CB - 1.4), s_ * (P.CB - 0.7)))
        s = s.union(disc(ex, ez, 1.3, y0, y1))
        # cheek plate recess below the brow (leaves brow ridge proud)
        y0, y1 = sorted((s_ * (P.CB - 0.8), s_ * (P.CB + 1)))
        s = s.cut(sector(R_SPLIT + 0.8, 40.8, 3.0, 26.0, y0, y1))
    # nostrils on the snout
    for yy in (3.2, -3.2):
        nx, nz = pol(P.R, -8.0)
        s = s.cut(cq.Workplane().sphere(1.5).translate((nx, yy, nz)))
    # skull armour seams
    for ph in (10.0, 30.0):
        s = s.cut(sector(P.R - 0.6, P.R + 1, ph - 0.5, ph + 0.5, -7, 7))
    return s


def jaw():
    h = _head_blank()
    j = h.intersect(_jaw_region(0.0)).cut(_skull_teeth(0.7))
    j = j.cut(disc(*JAW_PIVOT, (JAW_PIN_D + P.CLR) / 2, -P.CB - 1, P.CB + 1))
    from .hinges import G_STOP
    g0 = JAW_POST[0] - 0.0 - G_STOP
    g1 = JAW_POST[1] - P.JAW_OPEN + G_STOP
    j = j.cut(sector(JAW_STOP_R[0] - 0.3, JAW_STOP_R[1] + 3, g0, g1, -7, 7, c=JAW_PIVOT))
    # remove the head knuckle tongue from the jaw (it belongs to the skull)
    j = j.cut(disc(*pol(P.R_KNUCKLE, P.PHI_HEAD_DORSAL), P.KNUCKLE_R + 0.6, -10, 10))
    return j
