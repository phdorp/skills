model Tank "Cylindrical water tank draining through a bottom hole (Torricelli's law)"
  import SI = Modelica.Units.SI;
  parameter SI.Area A = 2 "Tank cross-section area";
  parameter SI.Area a = 0.01 "Outlet hole area";
  parameter SI.Height h0 = 4 "Initial water level";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";

  SI.Height h(start = h0, fixed = true) "Water level";
  SI.VolumeFlowRate q "Outflow through the hole";
  discrete SI.Time tEmpty(start = 0, fixed = true) "Time the tank runs empty (0 until then)";
  Boolean empty(start = false, fixed = true) "True once the tank has run empty";
equation
  // Torricelli's law; noEvent/max guard sqrt against tiny negative solver overshoot
  q = if empty then 0 else a*noEvent(sqrt(2*g*max(h, 0)));
  A*der(h) = -q;

  when h <= 0 then
    empty = true;
    tEmpty = time;
    reinit(h, 0);
  end when;

  annotation(experiment(StartTime = 0, StopTime = 300, Tolerance = 1e-8, Interval = 0.1));
end Tank;
