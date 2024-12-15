D,f=[-1j,1,1j,-1],[*open(0)]
X,Y,d=len(f[0])-1,len(f),range
z=lambda t:{x+y*1j for y in d(Y)for x in d(X)if f[y][x]in t}
b,o,r=z("#"),z("^").pop(),{}
def f(s,p):
 q,e=o,0
 while X>q.real>=0<=q.imag<Y:
  while{(u:=q+D[e])}<s:e=-~e%4
  if e in(a:=p.get(q,{})):return 1
  p[q],q={e:1}|a,u
f(b,r)
print(len(r),sum((g!=o)==f(b|{g},{})for g in r))