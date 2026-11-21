model ThermostatCheck "Analytic: tau = C/G = 2000 s; tOff1 = tau ln(15/9); 142 switch-ons in one day"
  Thermostat th;
equation
  when terminal() then
    assert(abs(th.tOff1 - 2000*log(15/9)) < 0.1, "tOff1 wrong: " + String(th.tOff1, significantDigits = 15));
    assert(th.nOn == 142, "nOn wrong: " + String(th.nOn));
    assert(th.heaterOn, "heater should be on at the end of the day");
  end when;
  annotation(experiment(StopTime = 86400, Tolerance = 1e-8));
end ThermostatCheck;
