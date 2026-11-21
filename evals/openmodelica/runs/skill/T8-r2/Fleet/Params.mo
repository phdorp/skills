within Fleet;
record Params "Vehicle parameter set"
  import Modelica.Units.SI;
  parameter SI.Mass m "Vehicle mass";
  parameter SI.Area cdA "Drag area (drag coefficient times frontal area)";
  parameter Real cr "Rolling resistance coefficient";
end Params;
