model BallTest "Checks Ball against the analytic solution: impacts at t1 = sqrt(2 h0 / g) = 1.42784 s and t1 (1 + 2 e) = 3.71239 s"
  Ball b;
  discrete Real hMin(start = 10, fixed = true) "Lowest height at an impact";
  discrete Real tSecond(start = -1, fixed = true) "Time of the second impact";
equation
  when change(b.n) then
    hMin = min(pre(hMin), b.h);
  end when;
  when b.n == 2 then
    tSecond = time;
  end when;
  when terminal() then
    assert(abs(b.tFirst - 1.4278431229270645) < 1e-4, "first impact wrong: " + String(b.tFirst, significantDigits = 15));
    assert(abs(tSecond - 3.712392119610368) < 1e-4, "second impact wrong: " + String(tSecond, significantDigits = 15));
    assert(b.n == 2, "expected 2 bounces by t = 5, got " + String(b.n));
    assert(hMin > -1e-6, "ball went below the floor: " + String(hMin, significantDigits = 15));
    assert(abs(b.h - 3.410684781814945) < 1e-3, "h(5) wrong: " + String(b.h, significantDigits = 15));
  end when;
  annotation(experiment(StopTime = 5));
end BallTest;
