"""Transforming armour: two swinging front panels and the fixed rear shell."""
import math
import cadquery as cq
from . import params as P
from .geom import sector, disc, ball, shell, slab_y, wedge_xz, mirror_y, pol
from .hinges import lug_half_angle, G_STOP, radial_cyl
from .torso import BRIDGE_PINS


def _deg(mm, r):
    return math.degrees(mm / r)


def front_panel():
    """Left (+Y) front armour panel, modelled closed (ball mode)."""
    p = shell(P.R_FP_IN, P.R).intersect(slab_y(P.Y_PANEL, P.R + 1))
    p = p.intersect(wedge_xz((0, 0), P.FP_PHI[0], P.FP_PHI[1]))
    ear = disc(0, 0, P.EAR_R, P.EAR_Y0, P.R + 1).intersect(ball(P.R))
    p = p.union(ear)
    # running hole on the axle, counterbore and stop-lug slot for the pole cap
    p = p.cut(disc(0, 0, (P.AXLE_D + 0.4) / 2, 40, P.R + 1))
    p = p.cut(disc(0, 0, P.POLE_CB_R, P.POLE_CB_FLOOR, P.R + 1))
    h = lug_half_angle()
    a0 = P.CAP_LUG_PHI - h - P.FP_DINO - G_STOP
    a1 = P.CAP_LUG_PHI + h + G_STOP
    r_in, r_out, _ = P.CAP_LUG
    p = p.cut(sector(r_in - 1.0, r_out + 0.4, a0, a1, P.POLE_CB_FLOOR, P.R + 1))
    # latch notch (slider enters here when locked)
    half = _deg(P.LATCH_W / 2 + P.SLIDE, 48.5)
    p = p.cut(sector(P.R_FP_IN - 0.5, P.R + 1, P.LATCH_PHI - 360 - half,
                     P.LATCH_PHI - 360 + half, P.Y_PANEL - 1,
                     1.0 + P.LATCH_LEN + P.LATCH_TRAVEL + 0.4))
    # layered armour plate grooves (0.6 deep): meridians and latitudes
    for ph in (-80.0, -45.0, -10.0, 25.0, 50.0):
        p = p.cut(sector(P.R - 0.6, P.R + 1, ph - 0.5, ph + 0.5, 12, 44))
    for yy in (22.0, 34.0):
        g = shell(P.R - 0.6, P.R + 1).intersect(slab_y(yy - 0.5, yy + 0.5))
        p = p.cut(g.intersect(wedge_xz((0, 0), P.FP_PHI[0] + 4, P.FP_PHI[1] - 4)))
    return p


def rear_shell():
    """Fixed rear shell (haunch armour) - one piece, pinned to the torso."""
    s = shell(P.R_RS_IN, P.R_RS_OUT)
    sides = s.intersect(wedge_xz((0, 0), P.RS_PHI[0], P.RS_PHI[1]))
    sides = sides.cut(slab_y(-P.Y_PANEL, P.Y_PANEL))
    bridge = s.intersect(wedge_xz((0, 0), *P.BRIDGE_PHI)).intersect(
        slab_y(-P.Y_PANEL - 0.5, P.Y_PANEL + 0.5))
    r = sides.union(bridge)
    r = r.cut(disc(0, 0, P.RS_POLE_HOLE, -60, 60))
    for ph in BRIDGE_PINS:
        r = r.cut(radial_cyl(ph, 40.0, 51.0, 3.3))
    # stiffening rim bead on the lower free edge
    return r


def front_panel_R():
    return mirror_y(front_panel())
