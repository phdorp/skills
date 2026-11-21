within Fleet;
record Truck "Heavy truck, same fields as Params but declared on its own"
  parameter Real m(unit = "kg") = 12000 "Vehicle mass";
  parameter Real cdA(unit = "m2") = 6 "Drag area";
  parameter Real cr = 0.007 "Rolling resistance coefficient";
end Truck;
