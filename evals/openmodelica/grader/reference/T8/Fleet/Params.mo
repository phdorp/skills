within Fleet;
record Params "Vehicle parameters"
  parameter Real m(unit = "kg") "Vehicle mass";
  parameter Real cdA(unit = "m2") "Drag area";
  parameter Real cr "Rolling resistance coefficient";
end Params;
