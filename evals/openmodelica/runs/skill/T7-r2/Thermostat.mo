model Thermostat "Room heated by an on/off heater with a 19..21 degC hysteresis"
  import Modelica.Units.SI;
  parameter SI.HeatCapacity C = 2e5 "Heat capacity of the room";
  parameter SI.ThermalConductance G = 100 "Thermal conductance to ambient";
  parameter SI.HeatFlowRate P = 3000 "Heater power";
  parameter SI.Temperature Tamb = 273.15 "Ambient temperature (0 degC)";
  parameter SI.Temperature TOff = 294.15 "Heater switches off at 21 degC";
  parameter SI.Temperature TOn = 292.15 "Heater switches on at 19 degC";
  SI.Temperature T(start = 288.15, fixed = true) "Room temperature (starts at 15 degC)";
  Boolean heaterOn(start = true, fixed = true) "Heater state";
  Integer nOn(start = 0, fixed = true) "Number of off-to-on switches";
  discrete SI.Time tOff1(start = -1, fixed = true) "Time of the first switch-off (-1 until then)";
equation
  C*der(T) = (if heaterOn then P else 0) - G*(T - Tamb);
algorithm
  when T >= TOff then
    heaterOn := false;
    if pre(tOff1) < 0 then
      tOff1 := time;
    end if;
  end when;
  when T <= TOn then
    heaterOn := true;
    nOn := pre(nOn) + 1;
  end when;
  annotation(experiment(StopTime = 86400));
end Thermostat;
