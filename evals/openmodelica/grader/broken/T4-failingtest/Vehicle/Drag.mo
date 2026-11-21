within Vehicle;
partial model Drag "Drag force interface"
  input Real v(unit = "m/s") "Velocity";
  output Real F(unit = "N") "Drag force";
end Drag;
