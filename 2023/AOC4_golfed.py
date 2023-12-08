a=[1]*999;b=c=0
for l in open(b):
 for i in range(m:=38-len({*l.split()})):a[i-~c]+=a[c]
 b+=2**m//2;c+=1
print(b,sum(a[:c]))