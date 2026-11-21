model Tank "Cylindrical water tank draining through a bottom hole (Torricelli)"
  import Modelica.Units.SI;
  parameter SI.Area A = 2 "Tank cross-section";
  parameter SI.Area a = 0.01 "Hole area";
  parameter SI.Height h0 = 4 "Initial level";
  parameter SI.Acceleration g = 9.81 "Gravity";
  SI.Length h(start = h0, fixed = true) "Water level, m";
  SI.VolumeFlowRate q "Outflow";
  Boolean empty(start = false, fixed = true) "True once the tank has run empty";
  discrete SI.Time tEmpty(start = 0, fixed = true) "Time the tank runs empty (0 until then)";
equation
  q = if empty then 0 else a*sqrt(2*g*max(h, 0));
  A*der(h) = -q;
  when h <= 0 then
    empty = true;
    tEmpty = time;
    reinit(h, 0);
  end when;
  annotation(experiment(StopTime = 300));
end Tank;
