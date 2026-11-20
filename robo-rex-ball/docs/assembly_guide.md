# Assembly guide

No tools are needed apart from your fingers. A 4 mm drill bit turned by hand
is handy for cleaning hinge holes, and a flat surface helps for pressing pins.
**Print and tune the calibration coupons first** (see `print_settings.md`).

Directions below use the toy's own frame in **ball mode**: *front* is +X
(where the face is), *left* is +Y, *up* is +Z. Every hinge axis runs
left-right.

All D-pins have a flat along one side. The flat must line up with the flat in
the press-fit (D-shaped) hole. The round, slightly larger hole in the moving
part is the one the pin turns in.

## 0. Clean up

1. Remove supports from the torso, thighs, both front panels and the rear
   shell.
2. Run the 4 mm bit through every hinge hole by hand (head, tail, knees,
   shoulders). Run the 8 mm axle holes in the thighs and panel ears through
   with the axle stub coupon.
3. Test-fit each pin. Running holes should turn freely; D-holes should need a
   firm push.

## 1. Head and jaw

1. Slide the jaw's centre tongue (the *ramus*) between the two cheeks at the
   back of the skull. The teeth interlock when it's closed.
2. Push the **D3 jaw pin** through cheek, jaw and cheek. In the ball-mode
   frame, its flat faces forward (+X).
3. Check that the jaw swings about 30° open and stops on the internal post,
   and closes with the teeth meshed.

## 2. Head to torso

1. The skull has a 5.6 mm tongue at its upper rear corner. Slide it into the
   fork at the top-front of the torso's dorsal plate.
2. Push in a **D4 knuckle pin**. Its flat faces the ball centre.
3. The head should swing 40° forward and stop when the V-notch faces close.

## 3. Tail

1. Join `tail3` into `tail2` (tongue into fork), then `tail2` into `tail1`,
   then `tail1` into the fork at the top-rear of the torso. Use one **D4
   knuckle pin** per joint, flat toward the ball centre.
2. Each joint should straighten by 20 to 30° and stop on its V-notch.

## 4. Arms

1. Hold an arm against the torso side so the torso's shoulder post sits in
   the gap of the arm's C-ring.
2. Push a **headed shoulder pin** through the arm into the blind D-hole in the
   torso (flat facing down). The head sits in the arm's counterbore.
3. Repeat on the other side. Each arm swings 75°.

## 5. Rear shell

1. Lower the rear shell over the back of the torso so its centre bridge drops
   into the slot in the dorsal plate.
2. Push the two **D3 bridge pins** radially through the holes in the dorsal
   skin, through the bridge, into the torso core. They finish flush with the
   surface.

## 6. Legs (each side)

1. Press the shin onto the thigh's knee boss. The shin's C-ring wraps the
   thigh bar.
2. Push a **headed knee pin** from the outside through the shin into the
   thigh's D-hole. The flat points along the thigh, toward the foot.
3. Slide the thigh hub against the torso hub. The torso's hip post must sit
   inside the gap of the thigh's C-ring.

## 7. Main axles (each side)

1. Insert an **axle** (D-flat facing down) through the thigh sleeve and press
   it into the torso's D-bore until its end stands about 3 mm beyond the
   sleeve.
2. The thigh must now swing about 54° and stop at both ends.

## 8. Latch sliders

1. With the toy in dinosaur mode (panels open), slide each **latch slider**
   into the T-slot channel on the belly from the side face. The flange goes
   under the lips, and the thumb head points outward.
2. Push until the peg clicks past the detent bump. The slider now moves
   3.6 mm between *unlocked* (inner) and *locked* (outer).

## 9. Front armour panels (each side)

1. Put the panel ear over the axle end (it passes through the clearance hole
   in the rear shell).
2. Press the **pole cap**'s D-peg into the axle end, with its stop lug inside
   the curved slot of the ear counterbore.
3. The panel should swing 150° between *closed* (ball) and *folded back*
   (dino), stopping at both ends.

## Transforming

**Ball to dinosaur**

1. Slide both latch sliders inward (unlock).
2. Swing both front panels up and back over the haunches until they stop
   (150°).
3. Fold the knees out to straight, swinging the thighs forward at the same
   time. Mid-way, the leg passes hip −54° / knee 64°. Finish with the thigh
   at about −26° to the body.
4. Swing the arms down (75°).
5. Uncurl the tail joint by joint until each V-notch closes.
6. Swing the head forward 40° until it stops. Open the jaw if you like.
7. Stand it on its feet and let the tail tip touch the table: tripod stance.

**Dinosaur to ball** is the exact reverse. If the foot catches on a panel,
swing the thighs further back *before* folding the knees. That's the path the
planner found (see `kinematics.md`). Finish by closing the panels and sliding
both latches outward until they lock flush in the panel notches.

## Troubleshooting

| symptom | fix |
|---|---|
| head or tail droops in dino mode | knuckle hole too loose: reprint that part with a smaller knuckle-hole clearance |
| a joint binds | clean the hole with the 4 mm bit; check that the pin's D-flat matches the press hole |
| panel won't close fully | the leg isn't fully folded (knee 184°, hip −54°); also check that the slider is unlocked |
| ball won't stay shut | slider not clicked past the detent into the notch; tune `SLIDE` |
| axle slides out | press fit too loose: reprint with the next tighter D-hole size from the gauge |
