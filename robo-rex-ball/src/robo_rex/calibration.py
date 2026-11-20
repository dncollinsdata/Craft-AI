"""Printable calibration coupons.  Print these first and tune params.CLR,
SLIDE and the press-fit flats before printing the toy."""
import cadquery as cq
from . import params as P
from .geom import d_disc

RUN_CLR = (0.2, 0.3, 0.4, 0.5, 0.6)     # diametral clearance, running holes
PRESS = (-0.10, 0.0, 0.10, 0.20)         # diametral offset, D-holes (neg = interference)


def _notches(body, x, y_edge, n):
    for k in range(n):
        body = body.cut(cq.Workplane().box(0.8, 1.6, 10).translate((x - 1.5 + 1.5 * k, y_edge, 0)))
    return body


def pin_gauge():
    """Plate with running holes (top row) and press D-holes (bottom row).
    Holes are vertical; the part's notch count = column index."""
    plate = cq.Workplane().box(64, 26, 5).translate((0, 0, 2.5))
    for i, c in enumerate(RUN_CLR):
        x = -24 + 12 * i
        plate = plate.cut(cq.Workplane().circle((P.PIN_D + c) / 2).extrude(10).translate((x, 6, -1)))
        plate = _notches(plate, x, 13, i + 1)
    for i, c in enumerate(PRESS):
        x = -18 + 12 * i
        h = d_disc(0, 0, P.PIN_D + c, -1, 10, flat_phi=-90, flat=0.4)
        h = h.rotate((0, 0, 0), (1, 0, 0), 90).translate((x, -6, 10))
        plate = plate.cut(h)
        plate = _notches(plate, x, -13, i + 1)
    return plate


def test_pins():
    """Four D4 x 16 pins on a breakaway-free layout (print on their flats)."""
    out = None
    for i in range(4):
        p = d_disc(0, 0, P.PIN_D, 0, 16, flat_phi=-90, flat=0.4)
        p = p.translate((8 * i, 0, P.PIN_D / 2 - 0.4))
        out = p if out is None else out.union(p)
    return out


def knuckle_coupon():
    """Fork + tongue with the toy's real knuckle dimensions, joined by a
    test pin: checks rotation friction and the V-notch stop."""
    t = P.TONGUE_T / 2
    fork = cq.Workplane().box(20, 2 * P.CB, 14).translate((-6, 0, 0))
    fork = fork.cut(cq.Workplane().box(14, 2 * (t + 0.3), 20).translate((0, 0, 0)))
    fork = fork.cut(d_disc(0, 0, P.PIN_D, -P.CB - 1, P.CB + 1, flat_phi=180, flat=0.4))
    tongue = (cq.Workplane("XZ").circle(P.KNUCKLE_R).extrude(t, both=True)
              .union(cq.Workplane().box(22, 2 * t, 2 * P.KNUCKLE_R).translate((11, 0, 0))))
    tongue = tongue.cut(cq.Workplane("XZ").circle((P.PIN_D + P.CLR) / 2).extrude(10, both=True))
    return fork, tongue.translate((0, 30, 0))


def latch_coupon():
    """Flat replica of the belly latch channel + slider + panel notch."""
    s, w = P.SLIDE, P.LATCH_W / 2
    blk = cq.Workplane().box(18, 20, 8).translate((0, 0, 4))      # x = tangential, z = radial
    blk = blk.cut(cq.Workplane().box(2 * (w + s), 22, 4).translate((0, 0, 8)))
    blk = blk.cut(cq.Workplane().box(2 * (w + 1.5 + s), 22, 2.4).translate((0, 0, 5.0)))
    blk = blk.cut(cq.Workplane().box(2.5, 22, 1.2).translate((0, 0, 3.4)))
    for sg in (1, -1):
        blk = blk.union(cq.Workplane().box(2.6, 0.8, 0.8).translate((0, sg * 7.0, 3.4)))
    slider = (cq.Workplane().box(2 * w, P.LATCH_LEN, 4.2).translate((0, 0, 2.1))
              .union(cq.Workplane().box(2 * (w + 1.5), P.LATCH_LEN - P.LATCH_TRAVEL - 0.4, 1.7)
                     .translate((0, -1.6, 0.85))))
    slider = slider.union(cq.Workplane().box(1.8, 1.6, 1.3).translate((0, -P.LATCH_LEN / 2 + 0.8, -0.6)))
    notch = cq.Workplane().box(24, 14, P.T_OUT).translate((0, 0, P.T_OUT / 2))
    notch = notch.cut(cq.Workplane().box(2 * (w + s), 8, 6).translate((0, -5, 0)))
    return blk, slider.translate((30, 0, 0.6)), notch.translate((0, 30, 0))


def axle_coupon():
    """Short axle stub, D-keyed press block, hinge ear ring and pole-cap seat."""
    stub = d_disc(0, 0, P.AXLE_D, 0, 14, flat_phi=-90, flat=0.5)
    stub = stub.cut(d_disc(0, 0, 4.0, 8, 15, flat_phi=-90, flat=0.4))
    blk = cq.Workplane().box(18, 8, 18).translate((0, 4, 0))
    blk = blk.cut(d_disc(0, 0, P.AXLE_D, -1, 9, flat_phi=-90, flat=0.5))
    ear = cq.Workplane("XZ").circle(P.EAR_R).extrude(-4.6)
    ear = ear.cut(cq.Workplane("XZ").circle((P.AXLE_D + 0.4) / 2).extrude(-10))
    ear = ear.cut(cq.Workplane("XZ").workplane(offset=-4.6).circle(P.POLE_CB_R).extrude(2.2))
    return stub.translate((0, 0, 0)), blk.translate((30, 0, 0)), ear.translate((60, 0, 0))


COUPONS = {
    "cal_pin_gauge": pin_gauge,
    "cal_test_pins": test_pins,
    "cal_knuckle_fork": lambda: knuckle_coupon()[0],
    "cal_knuckle_tongue": lambda: knuckle_coupon()[1],
    "cal_latch_channel": lambda: latch_coupon()[0],
    "cal_latch_slider": lambda: latch_coupon()[1],
    "cal_latch_notch": lambda: latch_coupon()[2],
    "cal_axle_stub": lambda: axle_coupon()[0],
    "cal_axle_block": lambda: axle_coupon()[1],
    "cal_axle_ear": lambda: axle_coupon()[2],
}
