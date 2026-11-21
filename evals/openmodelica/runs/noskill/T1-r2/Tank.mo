model Tank "Cylindrical water tank draining through a bottom hole (Torricelli's law)"
  import Modelica.Units.SI;
  parameter SI.Area A = 2 "Tank cross-section area";
  parameter SI.Area a = 0.01 "Hole area";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";
  parameter SI.Height h0 = 4 "Initial water level";
  SI.Height h(start = h0, fixed = true) "Water level";
  SI.VolumeFlowRate q "Outflow through the hole";
  Boolean empty(start = false, fixed = true) "True once the tank has run empty";
  discrete SI.Time tEmpty(start = 0, fixed = true) "Time the tank ran empty (0 until then)";
equation
  q = if empty then 0 else a*sqrt(2*g*max(h, 0));
  A*der(h) = -q;
  when h <= 0 then
    empty = true;
    tEmpty = time;
    reinit(h, 0);
  end when;
  annotation(experiment(StartTime = 0, StopTime = 300, Tolerance = 1e-6, Interval = 0.1));
end Tank;
