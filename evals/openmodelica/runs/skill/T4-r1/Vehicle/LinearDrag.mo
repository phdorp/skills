within Vehicle;
model LinearDrag "Linear drag: F = k*v"
  import Modelica.Units.SI;
  extends Drag;
  parameter SI.TranslationalDampingConstant k = 10 "Damping constant, N.s/m";
equation
  F = k*v;
end LinearDrag;
