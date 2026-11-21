model Ball "Ball dropped from 10 m that bounces on the floor at h = 0"
  import Modelica.Units.SI;
  parameter SI.Height h0 = 10 "Initial height";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";
  parameter Real e = 0.8 "Coefficient of restitution";
  Real h(start = h0, fixed = true, unit = "m") "Height above the floor";
  SI.Velocity v(start = 0, fixed = true) "Vertical velocity, positive upwards";
  Integer n(start = 0, fixed = true) "Number of bounces";
  discrete SI.Time tFirst(start = -1, fixed = true) "Time of the first impact (-1: none yet)";
equation
  der(h) = v;
  der(v) = -g;
  when h <= 0 then
    reinit(v, -e * pre(v));
    n = pre(n) + 1;
    tFirst = if pre(tFirst) < 0 then time else pre(tFirst);
  end when;
  annotation(experiment(StopTime = 5));
end Ball;
