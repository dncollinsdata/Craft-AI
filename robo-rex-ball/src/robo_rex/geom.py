"""Small CadQuery helpers.  Everything here builds real B-rep solids."""
import math
import cadquery as cq


def _plane(y1):
    # local (u, v) -> world (X, Z); extrusion goes towards -Y
    return cq.Plane(origin=(0, y1, 0), xDir=(1, 0, 0), normal=(0, -1, 0))


def pol(r, a):
    return (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))


def prism_xz(pts, y0, y1):
    """Polygon given in (x, z), extruded between y0 and y1."""
    return cq.Workplane(_plane(y1)).polyline(pts).close().extrude(y1 - y0)


def sector(r0, r1, a0, a1, y0, y1, c=(0.0, 0.0)):
    """Annular sector in XZ (exact arcs) extruded along Y."""
    cx, cz = c
    am = 0.5 * (a0 + a1)
    P = lambda r, a: (cx + pol(r, a)[0], cz + pol(r, a)[1])
    wp = cq.Workplane(_plane(y1))
    if r0 <= 1e-6:
        wp = wp.moveTo(cx, cz).lineTo(*P(r1, a0)).threePointArc(P(r1, am), P(r1, a1)).close()
    else:
        wp = (wp.moveTo(*P(r0, a0)).lineTo(*P(r1, a0))
              .threePointArc(P(r1, am), P(r1, a1)).lineTo(*P(r0, a1))
              .threePointArc(P(r0, am), P(r0, a0)).close())
    return wp.extrude(y1 - y0)


def disc(cx, cz, r, y0, y1):
    return cq.Workplane(_plane(y1)).center(cx, cz).circle(r).extrude(y1 - y0)


def d_disc(cx, cz, d, y0, y1, flat_phi=-90.0, flat=0.5):
    """D-shaped cylinder along Y (a pin or a keyed hole). The flat sits
    `flat` mm inside the circle in direction flat_phi."""
    c = disc(cx, cz, d / 2, y0, y1)
    big = 4 * d
    ux, uz = pol(1, flat_phi)
    off = d / 2 - flat + big / 2
    box = cq.Workplane().box(big, (y1 - y0) + 2, big).translate(
        (cx + ux * off, 0.5 * (y0 + y1), cz + uz * off))
    return c.cut(box)


def ball(r):
    return cq.Workplane().sphere(r)


def shell(r_in, r_out):
    return ball(r_out).cut(ball(r_in))


def slab_y(y0, y1, size=300):
    return cq.Workplane().box(size, y1 - y0, size).translate((0, 0.5 * (y0 + y1), 0))


def rot(shape, pivot, ang):
    """Rotate CCW in the XZ plane (phi increases) about a Y-parallel axis."""
    px, pz = pivot
    return shape.rotate((px, 0, pz), (px, 1, pz), -ang)


def mirror_y(shape):
    return shape.mirror("XZ")


def wedge_xz(c, a0, a1, r=200.0, y0=-60, y1=60):
    """Pie wedge (for angular trimming) centred at c."""
    return sector(0, r, a0, a1, y0, y1, c)


def safe_union(*shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out.union(s)
    return out


def largest_solid(wp):
    """Keep only the biggest solid (drops slivers left by trimming)."""
    sols = wp.solids().vals()
    if len(sols) <= 1:
        return wp
    best = max(sols, key=lambda s: s.Volume())
    return cq.Workplane().add(best)
