within Fleet;
record Params "Vehicle parameter set"
  parameter Modelica.Units.SI.Mass m "Vehicle mass";
  parameter Modelica.Units.SI.Area cdA "Drag area (drag coefficient times frontal area)";
  parameter Real cr "Rolling resistance coefficient";
end Params;
