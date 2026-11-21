within Vehicle;
partial model Drag "Interface of a drag law: velocity in, drag force out"
  import Modelica.Units.SI;
  input SI.Velocity v "Velocity of the vehicle";
  output SI.Force F "Drag force, opposing positive velocity";
end Drag;
