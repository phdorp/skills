within HeatingLib;
model System "A room heated by a thermostat-controlled heater"
  Room room;
  Thermostat thermostat(C = room.C);
equation
  connect(room.T, thermostat.T);
  connect(thermostat.Q, room.Q_heat);
  annotation(experiment(StopTime = 86400));
end System;
