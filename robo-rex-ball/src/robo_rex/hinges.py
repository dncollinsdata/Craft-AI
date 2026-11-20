"""Printable hinge hardware and reusable joint features.

* Knuckle joints (head, tail): child tongue + parent fork, pin near the skin,
  V-notch above the pin whose faces meet at the dinosaur angle (= hard stop).
* C-hub stops: child gets a ring with a gap, parent gets a post riding in it.
  The post hits the gap ends exactly at the two ends of the joint range.
* D-pins: printed lying on their flat; press-fit in a D-hole, rotate in a
  round hole.  Interference is calibrated with the coupon in calibration.py.
"""
import math
import cadquery as cq
from . import params as P
from .geom import sector, disc, d_disc, pol, ball

G_STOP = 1.0          # angular clearance at stops (deg)
STOPS_ENABLED = True  # fold search temporarily disables stop features


# ------------------------------------------------------------- knuckles ----
def _wedge(apex, phi_b, delta, r=30.0, y=(-12, 12)):
    h = 0.5 * abs(delta) + G_STOP
    return sector(0, r, phi_b - h, phi_b + h, y[0], y[1], c=apex)


def knuckle_parent(shape, phi_b, delta, r_k=P.R_KNUCKLE, cb=P.CB):
    """Cut fork slot, V-notch and press-fit pin hole into the parent."""
    piv = pol(r_k, phi_b)
    t = P.TONGUE_T / 2 + 0.3
    shape = shape.cut(disc(piv[0], piv[1], P.KNUCKLE_R + 0.5, -t, t))
    shape = shape.cut(_wedge(piv, phi_b, delta))
    shape = shape.cut(d_disc(piv[0], piv[1], P.PIN_D, -cb - 1, cb + 1, flat_phi=phi_b + 180))
    return shape


def knuckle_child(shape, phi_b, delta, r_k=P.R_KNUCKLE, cb=P.CB):
    """Add the tongue (with running hole) and cut the V-notch on the child."""
    piv = pol(r_k, phi_b)
    t = P.TONGUE_T / 2
    side = shape.cut(cq.Workplane().box(200, 2 * t, 200))
    side = side.cut(_wedge(piv, phi_b, delta))
    core = shape.intersect(cq.Workplane().box(200, 2 * t, 200))
    tongue = disc(piv[0], piv[1], P.KNUCKLE_R, -t, t).intersect(ball(P.R))
    core = core.union(tongue)
    # tongue notch apex sits 3 mm outboard of the pin so the pin stays enclosed
    ux, uz = pol(1, phi_b)
    apex = (piv[0] + 3.0 * ux, piv[1] + 3.0 * uz)
    core = core.cut(_wedge(apex, phi_b, delta))
    out = side.union(core)
    out = out.cut(disc(piv[0], piv[1], (P.PIN_D + P.CLR) / 2, -cb - 1, cb + 1))
    return out


# ------------------------------------------------------------ C-hub stop ---
def c_hub_stop(pivot, r0, r1, y0, y1, post_span, q_range, post_y=None):
    """Return (child_ring, parent_post).

    post_span: (p0, p1) angular extent of the parent post (parent frame).
    q_range:   (qmin, qmax) joint range.  The child ring gap is sized so the
               post touches the gap ends exactly at qmin and qmax (+G_STOP).
    """
    p0, p1 = post_span
    qmin, qmax = q_range
    if not STOPS_ENABLED:
        tiny = sector(r0, r0 + 0.01, 0, 1, y0, y0 + 0.01, c=pivot)
        return tiny, tiny
    g0 = p0 - qmax - G_STOP
    g1 = p1 - qmin + G_STOP
    ring = sector(r0, r1, g1, g0 + 360.0, y0, y1, c=pivot)
    py = post_y or (y0, y1)
    post = sector(r0 + 0.0, r1, p0, p1, py[0], py[1], c=pivot)
    return ring, post


# ------------------------------------------------------------------ pins ---
def d_pin(length, d=P.PIN_D, head_d=None, head_t=1.2):
    """Pin along +Y starting at y=0, D-flat on -Z (print on the flat)."""
    pin = d_disc(0, 0, d, 0, length, flat_phi=-90, flat=0.4)
    if head_d:
        # head flat flush with the shank flat so the pin lies flat on the bed
        pin = pin.union(d_disc(0, 0, head_d, -head_t, 0.01, flat_phi=-90,
                               flat=head_d / 2 - (d / 2 - 0.4)))
    pin = pin.edges("|Y").fillet(0.2) if False else pin
    return pin


def radial_cyl(phi, r0, r1, d, y=0.0):
    """Cylinder along the radial direction phi (in XZ) at height y."""
    L = r1 - r0
    c = cq.Workplane("YZ").circle(d / 2).extrude(L).translate((r0, y, 0))
    return c.rotate((0, 0, 0), (0, 1, 0), -phi)


# ------------------------------------------------------------------ axle ---
def axle():
    """One half of the main hinge axle, modelled for the +Y side.

    Press-fits (D-key) into the torso hub, carries thigh, front panel ear and
    pole cap.  The D-flat faces -Z and doubles as the print bed face.
    """
    y0, y1 = P.AXLE_Y
    a = d_disc(0, 0, P.AXLE_D, y0, y1, flat_phi=-90, flat=0.5)
    a = a.cut(d_disc(0, 0, 4.0 + 0.0, y1 - 6.0, y1 + 1, flat_phi=-90, flat=0.4))
    return a.edges(">Y or <Y").chamfer(0.4)


def pole_cap():
    """Flush cap with stop lug; its D-peg presses into the axle end (+Y side)."""
    yf = P.POLE_CB_FLOOR
    cap = disc(0, 0, P.POLE_CB_R - 0.25, yf + 0.05, P.R + 1).intersect(ball(P.R))
    r_in, r_out, w = P.CAP_LUG
    half = math.degrees(w / 2 / ((r_in + r_out) / 2))
    lug = sector(r_in - 0.5, r_out, P.CAP_LUG_PHI - half, P.CAP_LUG_PHI + half,
                 yf + 0.05, P.R + 1).intersect(ball(P.R))
    peg = d_disc(0, 0, 4.0, P.AXLE_Y[1] - 5.6, yf + 0.1, flat_phi=-90, flat=0.4)
    return cap.union(lug).union(peg)


def lug_half_angle():
    r_in, r_out, w = P.CAP_LUG
    return math.degrees(w / 2 / ((r_in + r_out) / 2))
