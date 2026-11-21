package ThermostatTests "Checks for Thermostat.mo against the analytic solution (tau = C/G = 2000 s)"
  model Analytic "tOff1 = tau ln(15/9) = 1021.651 s; period tau (ln(21/19) + ln(11/9)) = 601.508 s; 142 switch-ons in a day; heater on at 86400 s with T = 20.8373 degC"
    Thermostat th;
    Real TEndC "Room temperature at the end, degC";
  equation
    TEndC = th.T - 273.15;
    when terminal() then
      assert(abs(th.tOff1 - 1021.6512475) < 0.1, "tOff1 wrong: " + String(th.tOff1, significantDigits = 15));
      assert(th.nOn == 142, "nOn wrong: " + String(th.nOn));
      assert(th.heaterOn, "heater should be on at the end");
      assert(abs(TEndC - 20.8373075) < 0.01, "final T wrong: " + String(TEndC, significantDigits = 15));
    end when;
    assert(th.T > 288.15 - 1e-6 and th.T < 294.15 + 0.01, "T left the range 15..21 degC: " + String(th.T, significantDigits = 15));
    annotation(experiment(StopTime = 86400, Tolerance = 1e-8));
  end Analytic;
end ThermostatTests;
