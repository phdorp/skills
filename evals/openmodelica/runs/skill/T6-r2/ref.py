# Reference: TR-BDF2 with fixed small steps and Newton, pure python
def f(y):
    y1,y2,y3=y
    return [-0.04*y1+1e4*y2*y3, 0.04*y1-1e4*y2*y3-3e7*y2*y2, 3e7*y2*y2]
def J(y):
    y1,y2,y3=y
    return [[-0.04,1e4*y3,1e4*y2],[0.04,-1e4*y3-6e7*y2,-1e4*y2],[0,6e7*y2,0]]
def solve3(A,b):
    import copy
    A=[r[:]+[b[i]] for i,r in enumerate(A)]
    for c in range(3):
        p=max(range(c,3),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]
        for r in range(3):
            if r!=c:
                m=A[r][c]/A[c][c]; A[r]=[a-m*q for a,q in zip(A[r],A[c])]
    return [A[i][3]/A[i][i] for i in range(3)]
def implicit(yprev_rhs, gam_h, y0):
    # solve y - gam_h f(y) = rhs
    y=y0[:]
    for _ in range(20):
        F=[y[i]-gam_h*f(y)[i]-yprev_rhs[i] for i in range(3)]
        Jm=J(y); A=[[(1 if i==j else 0)-gam_h*Jm[i][j] for j in range(3)] for i in range(3)]
        d=solve3(A,F); y=[y[i]-d[i] for i in range(3)]
        if max(abs(x) for x in d)<1e-15: break
    return y
g=2-2**0.5
def run(h,T=40.0):
    y=[1.0,0.0,0.0]; n=int(round(T/h))
    for _ in range(n):
        fy=f(y)
        rhs=[y[i]+g*h/2*fy[i] for i in range(3)]
        yg=implicit(rhs,g*h/2,y)
        rhs=[((1/(g*(2-g)))*yg[i]-((1-g)**2/(g*(2-g)))*y[i]) for i in range(3)]
        y=implicit(rhs,(1-g)/(2-g)*h,yg)
    return y
for h in (4e-3,2e-3,1e-3):
    y=run(h); print(h, ["%.10g"%v for v in y], sum(y))
