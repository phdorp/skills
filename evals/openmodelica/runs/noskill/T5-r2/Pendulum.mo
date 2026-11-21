model Pendulum "Point-mass pendulum on a massless rod, released from rest with the rod horizontal"
  import Modelica.Units.SI;
  parameter SI.Mass m = 1 "Point mass";
  parameter SI.Length L = 1 "Rod length";
  parameter SI.Acceleration g = 9.81 "Gravity";

  inner Modelica.Mechanics.MultiBody.World world(
    g = g,
    n = {0, -1, 0}) "Gravity acts along -y (down)";
  Modelica.Mechanics.MultiBody.Joints.Revolute hinge(
    n = {0, 0, 1},
    phi(fixed = true, start = Modelica.Constants.pi/2),
    w(fixed = true, start = 0)) "Pivot; rotation about z, motion in the x-y plane";
  Modelica.Mechanics.MultiBody.Parts.FixedTranslation rod(
    r = {0, -L, 0}) "Massless rod, hangs along -y when hinge.phi = 0";
  Modelica.Mechanics.MultiBody.Parts.PointMass mass(m = m) "Bob";

  SI.Angle phi "Angle between rod and downward vertical (0 = hanging down)";
equation
  connect(world.frame_b, hinge.frame_a);
  connect(hinge.frame_b, rod.frame_a);
  connect(rod.frame_b, mass.frame_a);
  phi = hinge.phi;
  annotation (experiment(StopTime = 3));
end Pendulum;
