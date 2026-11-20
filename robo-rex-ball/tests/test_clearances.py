"""Static geometry checks: integrity, interference, envelope, clearances."""
import pytest
from robo_rex import assembly as AS, collide as C, kinematics as K, validate as V, params as P


@pytest.mark.parametrize("name", AS.ORDER)
def test_part_is_single_valid_watertight_solid(name):
    r = V.part_integrity(name)
    assert r["brep_valid"] and r["solids"] == 1
    assert r["watertight"] and r["nonmanifold_edges"] == 0
    assert r["volume_cm3"] > 0


@pytest.mark.parametrize("mode", ["dino", "ball"])
def test_no_interference(mode):
    assert C.overlaps(K.pose_q(mode)) == []


def test_ball_fits_100mm_sphere():
    assert V.envelope_ball() == {}


def test_running_clearances_ball():
    g = V.clearances("ball")
    # bearing / sliding fits designed at >= 0.2 mm
    for pair in ("thigh_L/axle_L", "panel_L/rear_shell", "slider_L/torso", "skull/panel_L"):
        assert g[pair] >= 0.19, (pair, g[pair])


def test_print_volume():
    import numpy as np
    for n in AS.ORDER:
        ext = np.sort(AS.mesh(n).extents)
        assert ext[-1] <= 220 and ext[0] <= 250
