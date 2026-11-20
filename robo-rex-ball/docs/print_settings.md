# Print settings: Creality Ender 3 (220 x 220 x 250 mm, 0.4 mm nozzle)

The STL files in `output/stl/` are already rotated into the orientation the
exporter found best. It searched 86 directions per part for the least
area overhanging more than 45°, with at least 30 mm² of bed contact. Import
them as they are; don't let the slicer re-orient. Per-part overhang and bed
contact areas are in `output/reports/print_manifest.json`.

## Base profile (PLA / PLA+)

| setting | value |
|---|---|
| layer height | 0.20 mm (first layer 0.24 mm) |
| line width | 0.42 mm |
| walls / perimeters | 3 (4 for pins, axles, pole caps) |
| top / bottom layers | 5 / 4 |
| infill | 20 % gyroid (100 % for pins, axles, pole caps, latch sliders) |
| nozzle | 205 °C (PLA), 215 °C (PLA+) |
| bed | 60 °C, PEI or glue stick |
| print speed | 50 mm/s, outer wall 25 mm/s |
| first layer | 20 mm/s |
| part cooling | 100 % after layer 2 |
| retraction (Bowden) | 5 mm at 40 mm/s |
| seam | aligned, rear |
| elephant-foot compensation | 0.15 mm (needed for the 0.3 mm hinge clearances) |

## Supports

Use **tree supports, touching the build plate only**, on these parts. Check
`overhang_area_mm2` in the manifest; anything above about 150 mm² gets
supports:

* `torso`: the axle hub and stop posts stand out of the side faces.
* `rear_shell`, `panel_L`, `panel_R`: 100 mm curved shells. Add a 5 mm brim;
  the bed contact is a thin rim and large thin shells like to warp.
* `thigh_L`, `thigh_R`: the axle sleeve stands proud of the hub.
* `polecap_L/R` and the headed pins: small overhangs under the heads. These
  usually print fine without support at 0.2 mm, but enable support if they
  sag.

Every other part prints without support.

## Pins and axles

* Pins and axles are modelled lying on their D-flat. Print them flat so the
  layers run along the pin's length (much stronger in bending).
* Print 2 spares of every pin. They're tiny and easy to lose.
* The D-flat also keys the pin: rotate it until the flat matches the flat in
  the press-fit hole.

## Calibrate first (about 1 h of printing)

The clearances in `src/robo_rex/params.py` are starting points, not
universal truths. Print the coupons in `output/stl/calibration/` with the
same profile you'll use for the toy:

1. **`cal_pin_gauge` + `cal_test_pins`**
   * Top row: running holes with 0.2 to 0.6 mm diametral clearance. Pick the
     tightest hole a test pin turns in *smoothly*, and set `CLR` to that value.
     The default is 0.3.
   * Bottom row: D-holes with -0.1 to +0.2 mm offset. Pick the one where the
     pin needs a firm push and then stays put. That's your press fit.
2. **`cal_knuckle_fork` + `cal_knuckle_tongue`**: assemble with a test pin.
   The head is held up in dinosaur mode by friction only (about 2 to 3 N·mm).
   If the tongue flops, reduce `CLR` by 0.05 mm for the knuckle holes. If it
   binds, increase it.
3. **`cal_latch_*`**: the slider should click over the 0.3 mm detent with a
   firm thumb push and lock into the notch. Tune `SLIDE` (default 0.35 mm).
4. **`cal_axle_*`**: the stub must press into the block and stay put, and the
   ear ring must turn freely on the stub. Then press the cap seat.

After changing a parameter, regenerate everything:

```bash
python3 scripts/generate_stls.py && python3 scripts/validate_geometry.py
```

## Rough time and material

About 200 g of PLA for the toy plus supports, roughly 14 to 18 h total on a
stock Ender 3 at the settings above. The shells and torso are the long prints
(2 to 3 h each). These are estimates, not slicer output.
