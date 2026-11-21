model Thermostat "Room heated by an on/off heater with hysteresis thermostat"
  import Modelica.Units.SI;
  parameter SI.HeatCapacity C = 2e5 "Heat capacity of the room";
  parameter SI.ThermalConductance G = 100 "Thermal conductance to ambient";
  parameter SI.Power P = 3000 "Heater power";
  parameter SI.Temperature Tamb = 273.15 "Ambient temperature (0 degC)";
  parameter SI.Temperature TOff = 273.15 + 21 "Heater switches off at this temperature";
  parameter SI.Temperature TOn = 273.15 + 19 "Heater switches on at this temperature";
  parameter SI.Temperature T0 = 273.15 + 15 "Initial room temperature";

  SI.Temperature T(start = T0, fixed = true) "Room temperature";
  Boolean heaterOn(start = true, fixed = true) "Heater state";
  Integer nOn(start = 0, fixed = true) "Number of off-to-on switches";
  discrete SI.Time tOff1(start = -1, fixed = true) "Time of first switch-off (-1 until it happens)";
equation
  C*der(T) = (if heaterOn then P else 0) - G*(T - Tamb);

  when T >= TOff then
    heaterOn = false;
  elsewhen T <= TOn then
    heaterOn = true;
  end when;

  when heaterOn then
    nOn = pre(nOn) + 1;
  end when;

  when not heaterOn then
    tOff1 = if pre(tOff1) < 0 then time else pre(tOff1);
  end when;
  annotation(experiment(StartTime = 0, StopTime = 86400, Tolerance = 1e-8, Interval = 10));
end Thermostat;
