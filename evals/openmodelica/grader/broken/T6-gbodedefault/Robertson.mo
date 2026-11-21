model Robertson "Robertson's stiff chemical kinetics"
  Real y1(start = 1, fixed = true);
  Real y2(start = 0, fixed = true);
  Real y3(start = 0, fixed = true);
equation
  der(y1) = -0.04*y1 + 1e4*y2*y3;
  der(y2) = 0.04*y1 - 1e4*y2*y3 - 3e7*y2^2;
  der(y3) = 3e7*y2^2;
  annotation(experiment(StopTime = 40, Tolerance = 1e-8),
    __OpenModelica_simulationFlags(s = "gbode"),
    __OpenModelica_commandLineOptions = "--generateDynamicJacobian=symbolic");
end Robertson;
