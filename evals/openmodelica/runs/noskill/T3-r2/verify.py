import csv, math
rows = list(csv.DictReader(open("MSD_res.csv")))
m, c, d, x0 = 1.0, 100.0, 2.0, 0.1
wn = math.sqrt(c/m); z = d/(2*math.sqrt(c*m)); wd = wn*math.sqrt(1-z**2)
xa = lambda t: x0*math.exp(-z*wn*t)*(math.cos(wd*t) + z*wn/wd*math.sin(wd*t))
err = max(abs(float(r["x"]) - xa(float(r["time"]))) for r in rows)
f, l = rows[0], rows[-1]
print("n=%d t_end=%s x(0)=%s v(0)=%s x(3)=%s analytic x(3)=%.6f" % (len(rows), l["time"], f["x"], f["mass.v"], l["x"], xa(3)))
print("max |x - analytic| = %.3e" % err)
print("max |x - mass.s| = %.3e" % max(abs(float(r["x"]) - float(r["mass.s"])) for r in rows))
