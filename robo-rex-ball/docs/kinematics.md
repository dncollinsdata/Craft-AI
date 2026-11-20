# Kinematic model

Generated from `src/robo_rex/kinematics.py`. Frame: origin = ball centre, +X forward, +Y left, +Z up (ball frame, fixed to the torso). **Every revolute axis is parallel to +Y**, so the mechanism is planar. Positive angles rotate +X toward +Z. Each part is modelled at q = 0; the table gives q in each mode. Pivots are listed with all ancestors at their own q = 0.

In dinosaur mode the whole toy is pitched nose-up by 25.75 deg so the tail tip rests on the ground (tripod stance). That pitch is a world orientation, not a joint.

| joint | parent | pivot x, z (mm) | range (deg) | dino | ball | mechanical stops |
|---|---|---|---|---|---|---|
| head | torso | 28.51, 36.48 | 0 .. 40 | 40 | 0 | ball: skull face meets dorsal plate / dino: V-notch faces meet |
| jaw | head | 29.35, 26.43 | -30 .. 0 | 0 | 0 | skull post in a C-gap around the jaw pin (both ends) |
| tail1 | torso | -26.56, 37.93 | -20 .. 0 | -20 | 0 | ball: faces meet / dino: V-notch faces meet |
| tail2 | tail1 | -44.35, 13.28 | -30 .. 0 | -30 | 0 | ball: faces meet / dino: V-notch faces meet |
| tail3 | tail2 | -43.03, -17.09 | -30 .. 0 | -30 | 0 | ball: faces meet / dino: V-notch faces meet |
| arm_L | torso | 25.00, 6.00 | 0 .. 75 | 0 | 75 | torso shoulder post in arm C-ring |
| arm_R | torso | 25.00, 6.00 | 0 .. 75 | 0 | 75 | torso shoulder post in arm C-ring |
| thigh_L | torso | 0.00, 0.00 | -54 .. 0 | -25.75 | -54 | torso hip post in thigh C-ring |
| thigh_R | torso | 0.00, 0.00 | -54 .. 0 | -25.75 | -54 | torso hip post in thigh C-ring |
| shin_L | thigh_L | 9.74, -24.11 | 0 .. 184 | 0 | 184 | thigh bar in shin C-ring (dino stop carries standing load) |
| shin_R | thigh_R | 9.74, -24.11 | 0 .. 184 | 0 | 184 | thigh bar in shin C-ring (dino stop carries standing load) |
| panel_L | torso | 0.00, 0.00 | 0 .. 150 | 150 | 0 | pole-cap lug in ear slot (both ends) |
| panel_R | torso | 0.00, 0.00 | 0 .. 150 | 150 | 0 | pole-cap lug in ear slot (both ends) |

Latch sliders are prismatic along +/-Y: travel 3.6 mm, locked in ball mode, with a 0.3 mm detent bump limiting outward travel.

## Transformation sequence (dino -> ball; reverse it for ball -> dino)

1. **pick up and level body**: pitch -> 0
2. **close jaw**: jaw -> 0
3. **fold head down**: head -> 0
4. **curl tail**: tail1 -> 0, tail2 -> 0, tail3 -> 0
5. **tuck arms**: arm_L -> 75, arm_R -> 75
6. **swing legs back**: thigh_L -> -54, thigh_R -> -54, shin_L -> 64, shin_R -> 64
7. **fold knees**: thigh_L -> -54, thigh_R -> -54, shin_L -> 184, shin_R -> 184
8. **close armour**: panel_L -> 0, panel_R -> 0
9. **slide latches**: slider_L -> 3.6, slider_R -> 3.6

The two-stage leg fold (swing back while bending, then fold the knee) came from a breadth-first search over a hip/knee occupancy grid built from the real meshes (`scripts/plan_leg_path.py`). A straight hip+knee interpolation drives the foot through the opened armour panel.
