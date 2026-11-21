within Fleet.Examples;
model CarCoast
  Coast coast(p = Car());
  annotation(experiment(StopTime = 300));
end CarCoast;
