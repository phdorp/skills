within Vehicle;
partial model Drag "Interface of a drag model: velocity in, drag force out"
  input Modelica.Units.SI.Velocity v "Vehicle velocity";
  output Modelica.Units.SI.Force F "Drag force, opposing positive velocity";
end Drag;
