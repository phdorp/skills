within Vehicle;
partial model Drag "Interface of a drag model: force from velocity"
  input Modelica.Units.SI.Velocity v "Vehicle velocity";
  output Modelica.Units.SI.Force F "Drag force, opposing positive velocity";
end Drag;
