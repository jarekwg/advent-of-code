# #205
# import re
# with open("2")as f:l=f.readlines()
# c=re.findall("..","AXBYCZAYBZCXAZBXCY")
# s=['456897312','357492816']
# def v(p):return lambda r:int(s[p][c.index(r[::2])])
# print(sum(map(v(0),l)),sum(map(v(1),l)))

# # 207
# import re
# with open("2")as f:l=f.readlines()
# c=re.findall("..","AXBYCZAYBZCXAZBXCY")
# s=re.findall("..","435567849972381126")
# def v(r):return map(int,s[c.index(r[::2])])
# print(list(map(sum,(zip(*map(v,l))))))

# # 187
# import re
# with open("2")as f:l=f.readlines()
# c=re.findall("..","AXBYCZAYBZCXAZBXCY435567849972381126")
# def v(r):return map(int,c[c.index(r[::2])+9])
# print(list(map(sum,(zip(*map(v,l))))))

# # 193
# import textwrap
# with open("2")as f:l=f.readlines()
# c=textwrap.wrap("AXBYCZAYBZCXAZBXCY435567849972381126",2)
# def v(r):return map(int,c[c.index(r[::2])+9])
# print(list(map(sum,(zip(*map(v,l))))))

# # 190
# with open("2")as f:l=f.readlines()
# c=[*map(''.join,zip(*[iter('AXBYCZAYBZCXAZBXCY435567849972381126')]*2))]
# def v(r):return map(int,c[c.index(r[::2])+9])
# print([*map(sum,(zip(*map(v,l))))])

# # 184
# import re
# with open("2")as f:l=f.readlines()
# c=re.findall("..","AXBYCZAYBZCXAZBXCY435567849972381126")
# def v(r):return map(int,c[c.index(r[::2])+9])
# print([*map(sum,(zip(*map(v,l))))])

# # 181
# with open("2")as f:l=f.readlines()
# c=[*zip(*[iter('AXBYCZAYBZCXAZBXCY435567849972381126')]*2)]
# def v(r):return map(int,c[c.index((r[0],r[2]))+9])
# print([*map(sum,(zip(*map(v,l))))])

# # 186
# with open("2")as f:l=f.readlines()
# c='ABCABCABC456897312XYZYZXZXY357492816'
# c=[*zip(c[:18],c[18:])]
# def v(r):return map(int,c[c.index((r[0],r[2]))+9])
# print([*map(sum,(zip(*map(v,l))))])

# # 163
# c='ABCABCABC456897312XYZYZXZXY357492816'
# c=[*zip(c[:18],c[18:])]
# print([*map(sum,(zip(*map(lambda r: map(int,c[c.index((r[0],r[2]))+9]),open("2").readlines()))))])

# # 157
# c=[*zip(*[iter('AXBYCZAYBZCXAZBXCY435567849972381126')]*2)]
# print([*map(sum,(zip(*map(lambda r:map(int,c[c.index((r[0],r[2]))+9]),open("2").readlines()))))])

# # 164
# c=['AXBYCZAYBZCXAZBXCY435567849972381126'[i:i+2]for i in range(0,36,2)]
# print([*map(sum,(zip(*map(lambda r:map(int,c[c.index(r[::2])+9]),open("2").readlines()))))])

# # 164
# c=['AXBYCZAYBZCXAZBXCY435567849972381126'[i*2:i*2+2]for i in range(18)]
# print([*map(sum,(zip(*map(lambda r:map(int,c[c.index(r[::2])+9]),open("2").readlines()))))])

# # 149
# c=[*zip('ABCABCABC456897312','XYZYZXZXY357492816')]
# print([*map(sum,(zip(*map(lambda r:map(int,c[c.index((r[0],r[2]))+9]),open("2").readlines()))))])

# # 148
# c=[*zip('ABC'*3+'456897312','XYZYZXZXY357492816')]
# print([*map(sum,(zip(*map(lambda r:map(int,c[c.index((r[0],r[2]))+9]),open("2").readlines()))))])

# # 145
# v=lambda r:(int('456897312'[i:="AXBYCZAYBZCXAZBXCY".index(r[::2])//2]),int('357492816'[i]))
# print([*map(sum,zip(*map(v,open("2").readlines())))])

# # 141
# print([*map(sum,zip(*map(lambda r:(int('456897312'[i:="AXBYCZAYBZCXAZBXCY".index(r[::2])//2]),int('357492816'[i])),open("2").readlines())))])

# # 134
# print([*map(sum,(zip(*map(lambda r:map(int,'456897312357492816'['AXBYCZAYBZCXAZBXCY'.index(r[::2])//2::9]),open("2").readlines()))))])

# # 132
# print(*map(sum,(zip(*map(lambda r:map(int,'456897312357492816'['AXBYCZAYBZCXAZBXCY'.index(r[::2])//2::9]),open("2").readlines())))))

# # 145
# d=open('2').read()
# print(*map(sum,zip(*[map(int,'456897312357492816'['AXBYCZAYBZCXAZBXCY'.index(d[i:i+4:2])//2::9])for i in range(0,len(d),4)])))

# # 126
# print(*map(sum,zip(*[map(int,'456897312357492816'['AXBYCZAYBZCXAZBXCY'.index(r[::2])//2::9])for r in open('2').readlines()])))

# 114
print(*map(sum,zip(*[map(int,'456897312357492816'['AXBYCZAYBZCXAZBXCY'.index(r[::2])//2::9])for r in open('2')])))
