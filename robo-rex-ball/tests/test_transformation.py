"""Kinematic checks: path, stops, standing, rolling."""
import numpy as np
from robo_rex import kinematics as K, validate as V, params as P


def test_home_transforms_identity():
    q = {j: 0.0 for j in K.JOINTS}
    T = K.transforms(q)
    for j in K.JOINTS:
        assert np.allclose(T[j], np.eye(4))


def test_rotation_matrix_is_ccw_about_pivot():
    M = K.rot_matrix((10.0, 0.0), 90.0)
    p = M @ np.array([20.0, 0.0, 0.0, 1.0])
    assert np.allclose(p[:3], [10.0, 0.0, 10.0])


def test_poses_within_ranges():
    for j, d in K.JOINTS.items():
        lo, hi = d["range"]
        assert lo - 1e-9 <= d["dino"] <= hi + 1e-9 and lo - 1e-9 <= d["ball"] <= hi + 1e-9


def test_collision_free_path():
    hits, n = V.path_check(max_step_deg=3.0)
    assert n > 100 and hits == []


def test_jaw_opens_freely():
    assert V.jaw_sweep(step=3.0) == []


def test_every_joint_has_working_stops():
    bad = {j: r for j, r in V.stop_check(step=0.5).items() if not r["stops_ok"]}
    assert not bad, bad


def test_dino_stands_on_feet_and_tail():
    s = V.standing()
    assert s["stable"] and s["com_margin_mm"] > 2
    assert set(s["ground_contacts"]) == {"shin_L", "shin_R", "tail3"}
    assert s["knee_stop_carries"] and s["tail_load_N"] > 0
    assert 110 <= s["length_mm"] <= 150


def test_ball_rolls_on_continuous_spine():
    r = V.rolling(n_dirs=2000)
    assert r["r_max"] <= P.R + 0.05
    assert r["sagittal_frac_ge_49"] >= 0.95
    assert r["frac_r_ge_46_5"] >= 0.97
