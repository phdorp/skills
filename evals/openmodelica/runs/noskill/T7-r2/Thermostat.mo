model Thermostat "Room heated by an on/off heater with hysteresis"
  import Modelica.Units.SI;
  parameter SI.HeatCapacity C = 2e5 "Heat capacity of the room";
  parameter SI.ThermalConductance G = 100 "Thermal conductance to ambient";
  parameter SI.Power P = 3000 "Heater power";
  parameter SI.Temperature Tamb = 273.15 "Ambient temperature (0 degC)";
  parameter SI.Temperature T0 = 288.15 "Initial room temperature (15 degC)";
  parameter SI.Temperature Thigh = 294.15 "Switch-off temperature (21 degC)";
  parameter SI.Temperature Tlow = 292.15 "Switch-on temperature (19 degC)";
  SI.Temperature T(start = T0, fixed = true) "Room temperature";
  Boolean heaterOn(start = true, fixed = true) "Heater state";
  Integer nOn(start = 0, fixed = true) "Number of off-to-on switches";
  discrete SI.Time tOff1(start = -1, fixed = true) "Time of first switch-off (-1 until it happens)";
equation
  C*der(T) = (if heaterOn then P else 0) - G*(T - Tamb);
  when T >= Thigh then
    heaterOn = false;
  elsewhen T <= Tlow then
    heaterOn = true;
  end when;
  when T <= Tlow then
    nOn = pre(nOn) + 1;
  end when;
  when T >= Thigh and pre(tOff1) < 0 then
    tOff1 = time;
  end when;
  annotation(experiment(StopTime = 86400, Interval = 10, Tolerance = 1e-8));
end Thermostat;
