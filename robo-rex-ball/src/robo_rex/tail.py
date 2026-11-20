"""Three-segment tail.  Modelled in ball mode: each segment is a sector of
the rolling spine band.  Knuckle pins sit near the skin so straightening a
joint opens the underside; the V-notch faces close at the dinosaur angle and
act as the mechanical stop."""
from . import params as P
from .geom import sector, ball, shell, slab_y
from .hinges import knuckle_child, knuckle_parent

BOUNDS = (P.PHI_DORSAL_TAIL, P.PHI_TAIL_12, P.PHI_TAIL_23, P.PHI_TAIL_BELLY)


def tail_segment(i):
    """i = 1, 2, 3 (1 = root)."""
    g = P.ANG_GAP / 2
    a0, a1 = BOUNDS[i - 1] + g, BOUNDS[i] - g
    s = sector(P.R_SKIN_IN, P.R + 1, a0, a1, -P.CB, P.CB).intersect(ball(P.R))
    s = s.cut(shell(P.R - 1.5, P.R + 2).intersect(slab_y(P.CB - 1.5, 20)))
    s = s.cut(shell(P.R - 1.5, P.R + 2).intersect(slab_y(-20, -P.CB + 1.5)))
    # armour plate seams across the top and side panel recesses
    am = 0.5 * (a0 + a1)
    s = s.cut(sector(P.R - 0.6, P.R + 1, am - 0.5, am + 0.5, -10, 10))
    for sg in (1, -1):
        y0, y1 = sorted((sg * (P.CB - 0.6), sg * (P.CB + 1)))
        s = s.cut(sector(31.0, 42.0, a0 + 9, a1 - 6, y0, y1))
    s = knuckle_child(s, BOUNDS[i - 1], P.TAIL_DINO[i - 1])
    if i < 3:
        s = knuckle_parent(s, BOUNDS[i], P.TAIL_DINO[i])
    return s
