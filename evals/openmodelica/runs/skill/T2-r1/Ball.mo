model Ball "Ball dropped from 10 m, bouncing on the floor at h = 0"
  import Modelica.Units.SI;
  parameter SI.Height h0 = 10 "Initial height";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";
  parameter Real e = 0.8 "Coefficient of restitution";
  parameter SI.Velocity vMin = 1e-3 "Rebound speed below which the ball comes to rest";
  SI.Height h(start = h0, fixed = true) "Height above the floor";
  SI.Velocity v(start = 0, fixed = true) "Vertical velocity, upwards positive";
  Boolean resting(start = false, fixed = true) "Ball lies on the floor";
  Integer n(start = 0, fixed = true) "Number of bounces (floor impacts)";
  discrete SI.Time tFirst(start = -1, fixed = true) "Time of the first impact (-1: none yet)";
equation
  der(h) = v;
  der(v) = if resting then 0 else -g;
  when h <= 0 and v < 0 then
    resting = -e*pre(v) < vMin;
    reinit(v, if resting then 0 else -e*pre(v));
    reinit(h, 0);
    n = pre(n) + 1;
    tFirst = if pre(n) == 0 then time else pre(tFirst);
  end when;
  assert(h > -1e-4, "Ball below the floor: h = " + String(h, significantDigits = 15));
  annotation(experiment(StopTime = 5));
end Ball;
