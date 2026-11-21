within Vehicle;
partial model Drag "Interface of a drag model: velocity in, resisting force out"
  import Modelica.Units.SI;
  input SI.Velocity v "Vehicle velocity";
  output SI.Force F "Drag force, positive when it opposes forward motion";
end Drag;
