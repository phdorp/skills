import csv, sys
rows = list(csv.DictReader(open(sys.argv[1])))
col = lambda k: [float(r[k]) for r in rows]
t, h, v, n, tf = col('time'), col('h'), col('v'), col('n'), col('tFirst')
print('min h', min(h), 'max h', max(h))
print('final t', t[-1], 'h', h[-1], 'v', v[-1], 'n', n[-1], 'tFirst', tf[-1])
apex = max(x for s, x in zip(t, h) if 1.5 < s < 3.7)
print('apex after 1st bounce', apex)
print('n changes at', [t[i] for i in range(1, len(t)) if n[i] != n[i-1]])
