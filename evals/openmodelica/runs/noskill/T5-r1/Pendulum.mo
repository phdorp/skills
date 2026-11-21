model Pendulum
  "Point mass on a massless 1 m rod, hinged at a fixed pivot, released from rest with the rod horizontal"
  import Modelica.Units.SI;
  parameter SI.Mass m = 1 "Point mass";
  parameter SI.Length L = 1 "Rod length";
  parameter SI.Angle phi0 = Modelica.Constants.pi/2 "Initial angle from downward vertical (horizontal rod)";

  inner Modelica.Mechanics.MultiBody.World world(
    g = 9.81,
    n = {0, -1, 0}) "Gravity 9.81 m/s2 along -y (down)";
  Modelica.Mechanics.MultiBody.Joints.Revolute revolute(
    n = {0, 0, 1},
    stateSelect = StateSelect.always,
    phi(fixed = true, start = phi0),
    w(fixed = true, start = 0)) "Hinge about z: pendulum swings in the x-y plane";
  Modelica.Mechanics.MultiBody.Parts.FixedTranslation rod(
    r = {0, -L, 0}) "Massless rod, pointing down when revolute.phi = 0";
  Modelica.Mechanics.MultiBody.Parts.PointMass mass(m = m) "Point mass at rod end";

  SI.Angle phi = revolute.phi "Angle between rod and downward vertical (0 = hanging down)";
  SI.AngularVelocity w = revolute.w "Angular velocity der(phi)";
equation
  connect(world.frame_b, revolute.frame_a);
  connect(revolute.frame_b, rod.frame_a);
  connect(rod.frame_b, mass.frame_a);
  annotation(experiment(StartTime = 0, StopTime = 3, Interval = 0.001, Tolerance = 1e-8));
end Pendulum;
