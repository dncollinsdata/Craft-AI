"""Print-orientation search and printability metrics for an FDM printer."""
import numpy as np
import trimesh
from . import params as P

OVERHANG_DEG = 45.0


def _candidates(n_fib=80):
    dirs = []
    for v in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
        dirs += [np.array(v, float), -np.array(v, float)]
    i = np.arange(n_fib) + 0.5
    phi = np.arccos(1 - 2 * i / n_fib)
    th = np.pi * (1 + 5 ** 0.5) * i
    dirs += list(np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1))
    return dirs


def rot_to_down(d):
    """Rotation matrix taking direction d onto -Z."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    return trimesh.geometry.align_vectors(d, [0, 0, -1])


def overhang_stats(m, bed_tol=0.4):
    n = m.face_normals
    c = m.triangles_center
    zmin = m.bounds[0, 2]
    area = m.area_faces
    lim = -np.cos(np.radians(90 - OVERHANG_DEG))   # nz below this = overhang
    over = (n[:, 2] < lim) & (c[:, 2] > zmin + bed_tol)
    bed = (n[:, 2] < -0.995) & (c[:, 2] <= zmin + bed_tol)
    return float(area[over].sum()), float(area[bed].sum())


def best_orientation(mesh):
    best = None
    for d in _candidates():
        M = rot_to_down(d)
        m = mesh.copy()
        m.apply_transform(M)
        over, bed = overhang_stats(m)
        h = m.extents[2]
        score = over + 0.05 * h * 10 + (300.0 if bed < 30 else 0.0)
        if best is None or score < best[0]:
            best = (score, M, over, bed)
    _, M, over, bed = best
    return M, over, bed


def place_on_bed(mesh, M):
    m = mesh.copy()
    m.apply_transform(M)
    lo, hi = m.bounds
    m.apply_translation([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
    return m


def fits_bed(m):
    ext = np.sort(m.extents[:2])
    bed = np.sort(np.array(P.BED[:2]))
    return bool(np.all(ext <= bed) and m.extents[2] <= P.BED[2])


def thickness_samples(m, n=1500, seed=0):
    """Local wall thickness by casting a ray inward from sampled faces."""
    rng = np.random.default_rng(seed)
    prob = m.area_faces / m.area_faces.sum()
    idx = rng.choice(len(m.faces), size=min(n, len(m.faces) * 4), p=prob)
    origins = m.triangles_center[idx] - m.face_normals[idx] * 1e-3
    dirs = -m.face_normals[idx]
    locs, ray_idx, _ = m.ray.intersects_location(origins, dirs, multiple_hits=False)
    t = np.full(len(idx), np.nan)
    d = np.linalg.norm(locs - origins[ray_idx], axis=1)
    t[ray_idx] = d
    return t[~np.isnan(t)]


def nonmanifold_edges(m):
    from trimesh.grouping import group_rows
    e = m.edges_sorted
    ok = group_rows(e, require_count=2)
    return int(len(e) - 2 * len(ok))


def clean_mesh(m):
    """Make a tessellation watertight: merge coincident seam vertices with
    manifold3d (OCC sometimes leaves unshared vertices along tangent seams)
    and rebuild a guaranteed-manifold mesh."""
    import manifold3d as mf
    if m.is_watertight and nonmanifold_edges(m) == 0:
        return m
    mm = mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                 tri_verts=np.asarray(m.faces, np.uint32))
    mm.merge()
    man = mf.Manifold(mm)
    if man.status() != mf.Error.NoError:
        m2 = m.copy()
        m2.merge_vertices(digits_vertex=4)
        return m2
    out = man.to_mesh()
    return trimesh.Trimesh(np.asarray(out.vert_properties)[:, :3], np.asarray(out.tri_verts), process=True)
