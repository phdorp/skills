model Pendulum "Point mass on a massless 1 m rod, swinging about a fixed pivot under gravity"
  import Modelica.Units.SI;
  import Modelica.Mechanics.MultiBody;
  parameter SI.Mass m = 1 "Mass of the bob";
  parameter SI.Length L = 1 "Rod length";
  parameter SI.Acceleration g = 9.81 "Gravity acceleration";
  inner MultiBody.World world(
    gravityType = MultiBody.Types.GravityTypes.UniformGravity,
    g = g,
    n = {0, -1, 0}) "Gravity along -y (down)";
  MultiBody.Joints.Revolute hinge(
    n = {0, 0, 1},
    phi(start = Modelica.Constants.pi/2, fixed = true),
    w(start = 0, fixed = true)) "Pivot, rotation about z: swing in the x-y plane";
  MultiBody.Parts.FixedTranslation rod(r = {0, -L, 0}) "Massless rod, hanging down at hinge.phi = 0";
  MultiBody.Parts.PointMass bob(m = m) "Point mass at the rod end";
  SI.Angle phi = hinge.phi "Angle between rod and downward vertical (0 = hanging down)";
equation
  connect(world.frame_b, hinge.frame_a);
  connect(hinge.frame_b, rod.frame_a);
  connect(rod.frame_b, bob.frame_a);
  annotation(experiment(StopTime = 3));
end Pendulum;
