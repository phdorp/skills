package Tests "Checks for Tank against the analytic Torricelli solution"
  model TankEmpties
    extends Tank;
    Real k = a/A*sqrt(2*g) "Analytic rate constant";
    Real tEmptyExact = 2*sqrt(h0)/k "Analytic emptying time, s";
    Real hExact = (max(sqrt(h0) - k*time/2, 0))^2 "Analytic level, m";
  equation
    assert(abs(h - hExact) < 1e-3, "h deviates from analytic: h=" + String(h, significantDigits = 15) + " exact=" + String(hExact, significantDigits = 15));
    assert(h >= -1e-9, "h negative: " + String(h, significantDigits = 15));
    when time >= 299 then
      assert(abs(tEmpty - tEmptyExact) < 0.5, "tEmpty wrong: " + String(tEmpty, significantDigits = 15) + " exact=" + String(tEmptyExact, significantDigits = 15));
    end when;
    when time >= 170 then
      assert(tEmpty <= 0, "tEmpty set too early: " + String(tEmpty, significantDigits = 15));
    end when;
    annotation(experiment(StopTime = 300));
  end TankEmpties;
end Tests;
