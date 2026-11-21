within Fleet;
record Params "Vehicle parameter set"
  extends Modelica.Icons.Record;
  parameter Modelica.Units.SI.Mass m "Vehicle mass";
  parameter Modelica.Units.SI.Area cdA "Drag area (drag coefficient times frontal area)";
  parameter Real cr(unit = "1") "Rolling resistance coefficient";
end Params;
