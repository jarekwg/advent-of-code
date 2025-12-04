t=lambda b,n:(m:=max(b[:-n]))+t(b[-~b.index(m):],~-n)if ~-n else max(b)
print(sum(int(t(a,2))+1j*int(t(a,12))for a in open(0)))