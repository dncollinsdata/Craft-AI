"""Export every printable part as STL (print-oriented), plus STEP files.

Outputs
  output/stl/<part>.stl            one file per printed component
  output/stl/calibration/*.stl     calibration coupons
  output/step/parts/<part>.step    native B-rep of each part (modelling frame)
  output/step/robo_rex_ball_{ball,dino}.step   full assemblies
  output/reports/print_manifest.json
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import cadquery as cq
import trimesh
from robo_rex import assembly as AS, kinematics as K, printing as PR, calibration as CAL
from robo_rex import hinges as HG, legs as L, torso as T, params as P, head as H

OUT = os.path.join(AS.ROOT, "output")
FLAT_ON_BED = {"axle_L", "axle_R"}          # modelled lying on their D-flat


def stl_of(wp, tol=0.02):
    fn = os.path.join(AS.CACHE, "_tmp_export.stl")
    os.makedirs(AS.CACHE, exist_ok=True)
    cq.exporters.export(wp, fn, tolerance=tol, angularTolerance=0.1)
    return trimesh.load(fn, force="mesh")


def hardware():
    """Pins: (builder, quantity, description)."""
    return {
        "pin_knuckle_d4x17": (lambda: HG.d_pin(2 * P.CB - 0.4), 4, "Head + 3 tail knuckle pins (D-flat press in fork)"),
        "pin_jaw_d3x17": (lambda: HG.d_pin(2 * P.CB - 0.4, d=H.JAW_PIN_D), 1, "Jaw hinge pin"),
        "pin_knee_d4_headed": (L.knee_pin, 2, "Knee pin with head"),
        "pin_shoulder_d4_headed": (L.shoulder_pin, 2, "Shoulder pin with head"),
        "pin_bridge_d3x10": (T.bridge_pin, 2, "Radial pins: rear shell bridge to torso"),
    }


def main():
    os.makedirs(os.path.join(OUT, "stl", "calibration"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "step", "parts"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "reports"), exist_ok=True)
    manifest = {}

    jobs = [(n, AS.solid(n), 1, AS.PARTS[n][3], "part") for n in AS.ORDER]
    jobs += [(n, f(), q, d, "hardware") for n, (f, q, d) in hardware().items()]
    jobs += [(n, f(), 1, "calibration coupon", "calibration") for n, f in CAL.COUPONS.items()]

    for name, wp, qty, desc, kind in jobs:
        m = stl_of(wp)
        if kind == "hardware" or name in FLAT_ON_BED or name.startswith("cal_"):
            M = np.eye(4)
            over, bed = PR.overhang_stats(PR.place_on_bed(m, M))
        else:
            M, over, bed = PR.best_orientation(m)
        pm = PR.place_on_bed(m, M)
        sub = "calibration" if kind == "calibration" else ""
        fn = os.path.join(OUT, "stl", sub, f"{name}.stl")
        pm.export(fn)
        if kind != "calibration":
            cq.exporters.export(wp, os.path.join(OUT, "step", "parts", f"{name}.step"))
        manifest[name] = dict(
            kind=kind, qty=qty, description=desc, file=os.path.relpath(fn, AS.ROOT),
            volume_cm3=round(pm.volume / 1000, 2), extents_mm=[round(v, 1) for v in pm.extents],
            fits_ender3=PR.fits_bed(pm), overhang_area_mm2=round(over, 0),
            bed_contact_mm2=round(bed, 0), watertight=bool(pm.is_watertight),
            rotation=np.round(M[:3, :3], 4).tolist())
        print(f"{name:24s} vol {pm.volume/1000:6.2f} cm3  ext {np.round(pm.extents,1)}  "
              f"overhang {over:6.0f} mm2  bed {bed:5.0f} mm2  watertight {pm.is_watertight}")

    for mode in ("ball", "dino"):
        AS.export_step(K.pose_q(mode), os.path.join(OUT, "step", f"robo_rex_ball_{mode}.step"))
    json.dump(manifest, open(os.path.join(OUT, "reports", "print_manifest.json"), "w"), indent=1)
    print("wrote", len(manifest), "files")


if __name__ == "__main__":
    main()
