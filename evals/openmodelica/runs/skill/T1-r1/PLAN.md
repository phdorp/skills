# Tank: plan

Requirements and checks (expected values computed with python3):
- h starts at 4 m, decreases monotonically, never below 0 -> CSV: h[0]=4, min(h)>=0.
- Torricelli: A*der(h) = -a*sqrt(2*g*h). Analytic: sqrt(h) = sqrt(h0) - a/(2A)*sqrt(2g)*t
  -> h(50)=2.0918, h(100)=0.7968, h(150)=0.1149 m.
- Empty at tEmpty = (2A/a)*sqrt(h0/(2g)) = 180.609 s -> tEmpty in CSV ~180.61, 0 before it.
- Simulates 300 s without errors/warnings (checkModel + simulate).

Steps:
1. Tank.mo: state h, outflow q guarded sqrt(max(h,0)), when h <= 0 records tEmpty.
2. sim.mos: load, checkModel, simulate csv; run from build/.
3. python csv check against the numbers above.
