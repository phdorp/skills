"""Compare build/MSD_res.csv with the analytic damped oscillation. Run after sim.mos."""
import csv, math, sys
m, c, d, x0 = 1.0, 100.0, 2.0, 0.1
s = d / (2 * m); wd = math.sqrt(c / m - s * s)
xa = lambda t: x0 * math.exp(-s * t) * (math.cos(wd * t) + s / wd * math.sin(wd * t))
rows = list(csv.DictReader(open(sys.argv[1] if len(sys.argv) > 1 else "build/MSD_res.csv")))
t = [float(r["time"]) for r in rows]; x = [float(r["x"]) for r in rows]
v = [float(r["mass.v"]) for r in rows]
err = max(abs(xi - xa(ti)) for ti, xi in zip(t, x))
checks = {
    "R1 x(0)=0.1, v(0)=0": abs(x[0] - 0.1) < 1e-9 and abs(v[0]) < 1e-9,
    "R2 max|x - analytic| < 1e-4": err < 1e-4,
    "R3 |x(3)| <= 0.1*exp(-3)*1.01": abs(x[-1]) <= 0.1 * math.exp(-3) * 1.01,
    "stop time 3 s": abs(t[-1] - 3.0) < 1e-9,
}
print(f"x(0)={x[0]} v(0)={v[0]} x(3)={x[-1]:.6g} (analytic {xa(3):.6g}) min x={min(x):.6g} max err={err:.3g}")
for k, ok in checks.items(): print("PASS" if ok else "FAIL", k)
sys.exit(0 if all(checks.values()) else 1)
