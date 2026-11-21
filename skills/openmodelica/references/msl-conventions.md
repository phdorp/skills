# Modelica Standard Library conventions

The library's conventions may differ from the project's (its conventions ADR). Where a ticket
uses a library class, convert at its connectors and test the conversion:

- Quaternions (`Modelica.Mechanics.MultiBody.Frames.Quaternions`): **scalar last**,
  `Q = {n*sin(phi/2), cos(phi/2)}`, so `Q[4]` is the scalar part.
- Orientations are **passive**: `Frames.Orientation` R holds `T`, the transformation matrix from
  frame 1 (usually world) to frame 2 (local); `resolve2(R, v1)` gives the same vector's
  coordinates in frame 2, `resolve1(R, v2)` back. Nothing is rotated.
- `World`: uniform gravity `g = g_n` along `n = {0, -1, 0}`, i.e. **minus y is down**; point
  gravity with `gravityType = PointGravity` and `mu`. Set both explicitly.
- `Parts.Body`: quaternion states by default (`useQuaternions = true`); Euler angle states use
  `sequence_angleStates = {1, 2, 3}`. A Body without `r_CM` warns "Parameter body.r_CM has no
  value": it uses {0, 0, 0}; give `r_CM` to silence it.
- Angles in radians (`Modelica.Units.Conversions.from_deg`), all units SI.
- `Translational.Components.Mass` (and the other sliding masses) has a length `L` (start 0, no
  default value): its flanges sit at `s - L/2` and `s + L/2`, and `s` is its centre.
  With a `Fixed` at s0 = 0 and a spring with `s_rel0 = 0`, set `L = 0`; then `mass.s` is the
  displacement from the spring's rest position (seen: L = 0.2 left the spring unstretched).

Check any other convention in the source: `instantiateModel(CLASS)` shows every parameter with
its default and every equation, inherited ones included.
