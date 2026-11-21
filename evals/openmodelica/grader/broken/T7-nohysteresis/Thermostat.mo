model Thermostat "Room heated by an on/off heater with hysteresis"
  parameter Real C(unit = "J/K") = 2e5 "Heat capacity";
  parameter Real G(unit = "W/K") = 100 "Thermal conductance to ambient";
  parameter Real P(unit = "W") = 3000 "Heater power";
  parameter Real Tamb(unit = "K") = 273.15 "Ambient temperature (0 degC)";
  parameter Real Ton(unit = "K") = 273.15 + 19 "Switch on at or below";
  parameter Real Toff(unit = "K") = 273.15 + 21 "Switch off at or above";
  Real T(unit = "K", start = 273.15 + 15, fixed = true) "Room temperature";
  Boolean heaterOn;
  Integer nOn(start = 0, fixed = true) "Off-to-on switches";
  discrete Real tOff1(unit = "s", start = 0, fixed = true) "Time of the first switch-off";
equation
  C*der(T) = (if heaterOn then P else 0) - G*(T - Tamb);
  heaterOn = T < 273.15 + 20;
  when pre(heaterOn) and not heaterOn and pre(nOn) == 0 then
    tOff1 = time;
  end when;
  when heaterOn and not pre(heaterOn) then
    nOn = pre(nOn) + 1;
  end when;
  annotation(experiment(StopTime = 86400));
end Thermostat;
