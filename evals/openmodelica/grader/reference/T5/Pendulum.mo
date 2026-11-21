model Pendulum "Point mass on a massless rod, released from horizontal"
  import Modelica.Mechanics.MultiBody;
  inner MultiBody.World world(g = 9.81, n = {0, -1, 0});
  MultiBody.Joints.Revolute revolute(n = {0, 0, 1}, useAxisFlange = false,
    phi(start = Modelica.Constants.pi/2, fixed = true), w(start = 0, fixed = true));
  MultiBody.Parts.FixedTranslation rod(r = {0, -1, 0});
  MultiBody.Parts.Body mass(m = 1, r_CM = {0, 0, 0}, I_11 = 0, I_22 = 0, I_33 = 0);
  Real phi(unit = "rad") = revolute.phi "Angle from the downward vertical";
equation
  connect(world.frame_b, revolute.frame_a);
  connect(revolute.frame_b, rod.frame_a);
  connect(rod.frame_b, mass.frame_a);
  annotation(experiment(StopTime = 3));
end Pendulum;
