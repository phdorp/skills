within ;
package SyntaxCard "Tested forms of common Modelica constructs: om-test SyntaxCard.mo passes"
  // Copy the form you need. Each class here loads, checks and simulates in OpenModelica 1.27.

  record Vehicle "A parameter set: a record, not a model"
    parameter Real mass = 1 "Mass, kg";
    parameter Real cg[3] = {0, 0, 0} "Centre of gravity, m";
  end Vehicle;

  record Variant "Extends a record and changes an inherited value in the extends clause"
    extends Vehicle(mass = 100);
    parameter Real canardArea = 0.5 "m2";
  end Variant;

  function polar "A function with two outputs; call it as (r, phi) = polar(x, y)"
    input Real x;
    input Real y;
    output Real r;
    output Real phi;
  algorithm
    r := sqrt(x^2 + y^2);
    phi := atan2(y, x);
  end polar;

  partial model Body "An interface: what every body has (partial: can't be simulated alone)"
    replaceable parameter Vehicle v "Its parameter set; replaceable, so a derived record can take its place";
    Real h(start = 10, fixed = true) "Height, m";
    Real vz(start = 0, fixed = true) "Vertical speed, m/s";
  equation
    der(h) = vz;
  end Body;

  model FallingBody "Extends the interface; swaps the parameter set for a derived record"
    extends Body(redeclare parameter Variant v);  // a Vehicle-typed v = Variant() is a type error
    parameter Real g = 9.81 "m/s2";
  equation
    der(vz) = -g;
  end FallingBody;

  model DraggedBody "Another body with the same interface"
    extends Body(v = Vehicle(mass = 2));
    parameter Real k = 0.1 "Drag coefficient, kg/m";
  equation
    v.mass * der(vz) = -v.mass * 9.81 - k * vz * abs(vz);
  end DraggedBody;

  model Exchangeable "A replaceable part; swap it with redeclare (see Tests.SwapBody)"
    replaceable model BodyModel = FallingBody constrainedby Body;
    BodyModel body;
  end Exchangeable;

  model Bounce "Events: when with reinit; pre() is the value just before the event"
    parameter Real e = 0.8 "Coefficient of restitution";
    Real h(start = 1, fixed = true);
    Real vz(start = 0, fixed = true);
    Integer bounces(start = 0, fixed = true);
  equation
    der(h) = vz;
    der(vz) = -9.81;
    when h <= 0 then
      reinit(vz, -e * pre(vz));
      bounces = pre(bounces) + 1;
    end when;
    annotation(experiment(StopTime = 1.5));
  end Bounce;

  model ImpactTimes "Values recorded at events: discrete variables, set only in a when, keep their value between events"
    Bounce b;
    discrete Real tFirst(start = -1, fixed = true) "Time of the first bounce, s (-1: none yet)";
    discrete Real tSecond(start = -1, fixed = true) "Time of the second bounce, s";
    discrete Real tLast(start = -1, fixed = true) "Time of the latest bounce, s";
  equation
    when change(b.bounces) then  // one equation per variable; an if-expression where it depends on the case
      tFirst = if pre(tFirst) < 0 then time else pre(tFirst);
      tSecond = if b.bounces == 2 then time else pre(tSecond);  // the n-th event: ask the counter, not the time
      tLast = time;
    end when;
    annotation(experiment(StopTime = 1.5));
  end ImpactTimes;

  model Hysteresis "A value switched by two events: when-statements in an algorithm section"
    parameter Real C = 1, h = 2, Q = 25, Tamb = 285;
    Real T(start = 300, fixed = true);
    Boolean heat(start = false, fixed = true);
  equation
    C*der(T) = (if heat then Q else 0) - h*(T - Tamb);
  algorithm  // two when-EQUATIONS for heat would be two equations: over-determined
    when T < 294 then
      heat := true;
    end when;
    when T > 296 then
      heat := false;
    end when;
    // the same as one when-equation in the equation section: when {T < 294, T > 296} then heat = T < 294; end when;
    annotation(experiment(StopTime = 2));
  end Hysteresis;

  model Sampled "Sampled data: sample() fires every Ts from t = 0; a discrete value is held between samples"
    parameter Real Ts = 0.1 "Sampling period, s";
    parameter Real K = 2 "Controller gain";
    Real x(start = 0, fixed = true) "Plant state";
    discrete Real u(start = 0, fixed = true) "Control signal, held between samples";
  equation
    der(x) = -x + u;
    when sample(0, Ts) then  // a time event every Ts; its condition must not use what the when sets
      u = K*(1 - x);  // x: its value at the sampling instant
    end when;
  end Sampled;

  model StickSlip "Modes switched by events: a block held by dry friction until the force breaks it free"
    parameter Real m = 1, Fs = 5 "Static friction, N", Fk = 4 "Sliding friction, N";
    Real x(start = 0, fixed = true), v(start = 0, fixed = true);
    Real F = 6*sin(time) "Pushing force, N";
    Boolean stuck(start = true, fixed = true);
  equation
    der(x) = v;
    m*der(v) = if stuck then 0 else F - Fk;  // stuck: static friction balances F; this example slides forward only
    when {pre(stuck) and F > Fs, not pre(stuck) and v < 0} then  // one when for every switch of the mode
      stuck = not pre(stuck);
    end when;
    when stuck then  // stuck again: a state jumps with reinit, it never gets an equation in a when
      reinit(v, 0);
    end when;
    annotation(experiment(StopTime = 5));
  end StickSlip;

  model Chain "Arrays and a for loop in equations; an initial equation instead of start values"
    parameter Integer n = 4;
    parameter Real tau[n] = {1, 2, 3, 4} "Time constants, s";
    Real x[n];
  initial equation
    x = zeros(n);
  equation
    der(x[1]) = (1 - x[1]) / tau[1];
    for i in 2:n loop
      der(x[i]) = (x[i - 1] - x[i]) / tau[i];
    end for;
  end Chain;

  model RCCircuit "Library components joined with connect; modifiers set their parameters"
    Modelica.Electrical.Analog.Sources.ConstantVoltage source(V = 10);
    Modelica.Electrical.Analog.Basic.Resistor resistor(R = 100);
    Modelica.Electrical.Analog.Basic.Capacitor capacitor(C = 1e-3, v(start = 0, fixed = true));
    Modelica.Electrical.Analog.Basic.Ground ground;
  equation
    connect(source.p, resistor.p);
    connect(resistor.n, capacitor.p);
    connect(capacitor.n, source.n);
    connect(source.n, ground.p);
    annotation(experiment(StopTime = 0.5));
  end RCCircuit;

  package Tests "Test models with asserts: om-test runs every model in a package named Tests"
    model PolarRoundTrip
      Real r, phi;
    equation
      (r, phi) = polar(3, 4);
      assert(abs(r - 5) < 1e-12, "polar: r should be 5, got " + String(r, significantDigits = 15));
    end PolarRoundTrip;

    model FallTime "Free fall from 10 m: h(t) = 10 - g t^2 / 2"
      FallingBody b;
    equation
      when terminal() then
        assert(abs(b.h - (10 - 9.81 / 2)) < 1e-3, "h(1) wrong: " + String(b.h, significantDigits = 15));
        assert(b.v.mass == 100, "the record binding should give mass 100");
      end when;
    end FallTime;

    model SwapBody "redeclare a replaceable part"
      Exchangeable ex(redeclare model BodyModel = DraggedBody);
    equation
      when terminal() then
        assert(ex.body.v.mass == 2 and ex.body.h > 10 - 9.81 / 2, "the dragged body should fall slower");
      end when;
    end SwapBody;

    model BounceCount
      Bounce b;
    equation
      when terminal() then
        assert(b.bounces >= 2, "expected at least 2 bounces, got " + String(b.bounces));
      end when;
      annotation(experiment(StopTime = 1.5));
    end BounceCount;

    model FirstImpact "Bounce from 1 m, e = 0.8: impacts at t1 = sqrt(2 h / g) = 0.4515 s and t1 (1 + 2 e) = 1.1740 s"
      ImpactTimes it;
    equation
      when terminal() then
        assert(abs(it.tFirst - sqrt(2 / 9.81)) < 1e-4, "first impact wrong: " + String(it.tFirst, significantDigits = 15));
        assert(abs(it.tSecond - (1 + 2 * 0.8) * sqrt(2 / 9.81)) < 1e-4, "second impact wrong: " + String(it.tSecond, significantDigits = 15));
        assert(it.tLast >= it.tSecond and it.tSecond > it.tFirst, "the bounces should come in order");
      end when;
      annotation(experiment(StopTime = 1.5));
    end FirstImpact;

    model HysteresisSwitches "Heater on at 0.5 ln(15/9) = 0.2554 s, off 0.5 ln(3.5/1.5) = 0.4236 s later"
      Hysteresis th;
      discrete Real tOn(start = -1, fixed = true), tOff(start = -1, fixed = true);
    equation
      when th.heat and pre(tOn) < 0 then
        tOn = time;
      end when;
      when not th.heat and pre(tOn) > 0 and pre(tOff) < 0 then
        tOff = time;
      end when;
      when terminal() then
        assert(abs(tOn - 0.5*log(15/9)) < 1e-4, "switch-on time wrong: " + String(tOn, significantDigits = 15));
        assert(abs(tOff - tOn - 0.5*log(3.5/1.5)) < 1e-4, "heating time wrong: " + String(tOff - tOn, significantDigits = 15));
      end when;
      annotation(experiment(StopTime = 2, Tolerance = 1e-8));  // event times are as exact as the tolerance
    end HysteresisSwitches;

    model SampledResponse "Zero-order hold: x(k+1) = e^-Ts x(k) + (1 - e^-Ts) u(k); x(1 s) = 0.643546"
      Sampled s;
      discrete Real x10(start = 0, fixed = true) "x at the 10th sample after t = 0, i.e. t = 1 s";
    equation
      when sample(0, s.Ts) then  // read values at the sampling instants, not at terminal() (it can come later)
        x10 = if time > 1 - s.Ts/2 and time < 1 + s.Ts/2 then s.x else pre(x10);
      end when;
      when terminal() then
        assert(abs(x10 - 0.643546) < 1e-5, "x(1) wrong: " + String(x10, significantDigits = 15));
      end when;
      annotation(experiment(StopTime = 1.5, Tolerance = 1e-8));
    end SampledResponse;

    model StickSlipModes "Breaks free at asin(5/6) = 0.98511 s, sticks again when v is back to 0 at 3.29634 s"
      StickSlip b;
      discrete Real tFree(start = -1, fixed = true), tStuck(start = -1, fixed = true);
    equation
      when not b.stuck then
        tFree = time;
      end when;
      when b.stuck then
        tStuck = time;
      end when;
      when terminal() then
        assert(abs(tFree - 0.985111) < 1e-4, "breakaway time wrong: " + String(tFree, significantDigits = 15));
        assert(abs(tStuck - 3.296342) < 1e-4, "re-stick time wrong: " + String(tStuck, significantDigits = 15));
        assert(abs(b.v) < 1e-9, "the block should be stuck again");
      end when;
      annotation(experiment(StopTime = 5, Tolerance = 1e-8));
    end StickSlipModes;

    model ChainSettles
      Chain c;
    equation
      when terminal() then
        assert(c.x[1] > c.x[2] and c.x[2] > c.x[3], "the chain should lag stage by stage");
      end when;
      annotation(experiment(StopTime = 5));
    end ChainSettles;

    model RCCharge "Capacitor voltage after one time constant RC = 0.1 s: 10 (1 - e^-1)"
      RCCircuit rc;
    equation
      when time >= 0.1 then
        assert(abs(rc.capacitor.v - 10 * (1 - exp(-1))) < 0.01, "v(RC) wrong: " + String(rc.capacitor.v, significantDigits = 15));
      end when;
      annotation(experiment(StopTime = 0.2));
    end RCCharge;

    model StiffRadau "Choosing the solver: Radau IIA, order 7; x(t) = 1 - exp(-1000 t)"
      Real x(start = 0, fixed = true);
    equation
      der(x) = -1000 * (x - 1);
      when time >= 0.002 then
        assert(abs(x - (1 - exp(-2))) < 1e-6, "x(0.002) wrong: " + String(x, significantDigits = 15));
      end when;
      annotation(experiment(StopTime = 0.01, Tolerance = 1e-8),
        __OpenModelica_simulationFlags(s = "gbode", gbm = "radauIIA4"));
    end StiffRadau;
  end Tests;
end SyntaxCard;
