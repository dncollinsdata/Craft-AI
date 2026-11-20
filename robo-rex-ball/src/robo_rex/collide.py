"""Fast interference / clearance checks with manifold3d."""
import itertools
import numpy as np
import manifold3d as mf
from . import assembly as AS
from . import kinematics as K

_BASE = {}
VOL_TOL = 0.5          # mm^3 of overlap tolerated as tessellation noise


def base(name):
    if name not in _BASE:
        m = AS.mesh(name)
        mesh = mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                       tri_verts=np.asarray(m.faces, np.uint32))
        man = mf.Manifold(mesh)
        if man.status() != mf.Error.NoError:
            raise RuntimeError(f"{name}: not a valid manifold ({man.status()})")
        _BASE[name] = man
    return _BASE[name]


def posed(q, names=None):
    Tm = K.transforms(q)
    out = {}
    for n in names or AS.ORDER:
        M = Tm[AS.body_of(n)][:3, :4]
        out[n] = base(n).transform(M.tolist())
    return out


def _bbox_overlap(a, b, pad=0.0):
    (a0, a1), (b0, b1) = _bb(a), _bb(b)
    return np.all(a0 - pad <= b1) and np.all(b0 - pad <= a1)


def _bb(m):
    bb = m.bounding_box()
    return np.array(bb[:3]), np.array(bb[3:])


def overlaps(q, names=None, pairs=None, tol=VOL_TOL):
    """Return list of (a, b, overlap_volume) above tolerance."""
    M = posed(q, names)
    keys = list(M)
    out = []
    for a, b in (pairs or itertools.combinations(keys, 2)):
        if not _bbox_overlap(M[a], M[b]):
            continue
        v = (M[a] ^ M[b]).volume()
        if v > tol:
            out.append((a, b, v))
    return out


def gaps(q, pairs, search=3.0):
    """Minimum distance for each pair (capped at `search`)."""
    M = posed(q, {n for p in pairs for n in p})
    return {(a, b): M[a].min_gap(M[b], search) for a, b in pairs}


def outside_sphere(q, names=None, r=50.0):
    """Volume of each part lying outside the sphere of radius r."""
    M = posed(q, names)
    S = mf.Manifold.sphere(r, 256)
    return {n: (m - S).volume() for n, m in M.items()}


def from_solid(wp, tol=0.08):
    """Manifold straight from a CadQuery object (no disk cache)."""
    import tempfile, os, trimesh, cadquery as cq
    fd, fn = tempfile.mkstemp(suffix=".stl")
    os.close(fd)
    cq.exporters.export(wp, fn, tolerance=tol, angularTolerance=0.2)
    m = trimesh.load(fn, force="mesh")
    os.remove(fn)
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                               tri_verts=np.asarray(m.faces, np.uint32)))


def xf(man, M):
    return man.transform(np.asarray(M)[:3, :4].tolist())
