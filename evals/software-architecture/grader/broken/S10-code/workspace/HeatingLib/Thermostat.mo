within HeatingLib;
block Thermostat "Proportional heating controller with a set point"
  parameter Interfaces.Temperature T_set = 293.15 "Set point";
  parameter Real tau(unit = "s") = 1800 "Time to close the gap to the set point";
  parameter Interfaces.HeatFlowRate Q_max = 3000 "Heater power limit";
  Interfaces.TemperatureInput T "Measured room temperature";
  Interfaces.HeatFlowOutput Q "Heating power demand";
protected
  // The gain needs the room's heat capacity, so it is read from the package constant
  // the room model uses as well.
  parameter Real k(unit = "W/K") = HeatingLib.roomHeatCapacity / tau "Controller gain";
equation
  Q = min(Q_max, max(0, k * (T_set - T)));
end Thermostat;

// k moved to a parameter
