within ;
model SteadyStateTest "Test wrapper: the shipped System simulated for 24 h, read by tests/check.mos"
  HeatingLib.System system;
  annotation(experiment(StopTime = 86400));
end SteadyStateTest;
