within Fleet;
record Params "Vehicle parameter set"
  import Modelica.Units.SI;
  parameter SI.Mass m = 1000 "Vehicle mass";
  parameter SI.Area cdA = 0.5 "Drag area (drag coefficient times frontal area)";
  parameter Real cr = 0.01 "Rolling resistance coefficient";
end Params;
