model Pendulum "Point mass on a massless 1 m rod, hinged at a fixed pivot, released from horizontal"
  import Modelica.Units.SI;
  import Modelica.Constants.pi;
  inner Modelica.Mechanics.MultiBody.World world(
    gravityType = Modelica.Mechanics.MultiBody.Types.GravityTypes.UniformGravity,
    g = 9.81,
    n = {0, -1, 0}) "Gravity 9.81 m/s2 along -y (down); world.frame_b is the fixed pivot";
  Modelica.Mechanics.MultiBody.Joints.Revolute rev(
    n = {0, 0, 1},
    phi(start = pi/2, fixed = true),
    w(start = 0, fixed = true)) "Hinge about z: the pendulum swings in the x-y plane";
  Modelica.Mechanics.MultiBody.Parts.FixedTranslation rod(r = {0, -1, 0})
    "Massless rod of length 1 m, pointing down when rev.phi = 0";
  Modelica.Mechanics.MultiBody.Parts.PointMass mass(m = 1) "1 kg point mass";
  SI.Angle phi "Angle between rod and downward vertical (0 = hanging straight down)";
  SI.AngularVelocity w "Angular velocity der(phi)";
equation
  phi = rev.phi;
  w = rev.w;
  connect(world.frame_b, rev.frame_a);
  connect(rev.frame_b, rod.frame_a);
  connect(rod.frame_b, mass.frame_a);
  annotation(experiment(StopTime = 3));
end Pendulum;
