r=range
def c(n,b):
 a=[*r(n)]
 for i in r(~-len(b)):
  for j in r(min(n,-~i)):
   if b[i]>b[a[j]]and~-len(b)-n+j>=i>a[j]:a[j:]=r(i,i+n-j)
 return"".join(b[i]for i in a)
print(*(sum(int(c(n,b))for b in[*open("3")])for n in(2,12)))