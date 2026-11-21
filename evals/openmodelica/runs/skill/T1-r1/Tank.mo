model Tank "Cylindrical water tank draining through a bottom hole (Torricelli's law)"
  import Modelica.Units.SI;
  parameter SI.Area A = 2 "Tank cross-section area";
  parameter SI.Area a = 0.01 "Hole area";
  parameter SI.Height h0 = 4 "Initial water level";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";
  SI.Length h(start = h0, fixed = true) "Water level, m";
  SI.VolumeFlowRate q "Outflow through the hole";
  discrete SI.Time tEmpty(start = 0, fixed = true) "Time the tank runs empty, s (0 until then)";
equation
  q = a*sqrt(2*g*max(h, 0));
  A*der(h) = -q;
  when h <= 0 then
    tEmpty = time;
  end when;
  annotation(experiment(StopTime = 300, Tolerance = 1e-8));
end Tank;
