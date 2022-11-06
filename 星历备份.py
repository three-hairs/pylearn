# -*- coding: UTF-8 -*-
import re
import math

file="C:/Users/Lenovo/Desktop/brdc0180.12n"
list1=[]
with open(file,'r') as f:
    data=f.read()
    data1=data.strip('\n').replace('-', ' -').replace('D+', 'e').replace('D -', 'e-').split()
    list1.append(data1)
list3=[str(i)+" " for list2 in list1 for i in list2]
index=''.join(list3)
t='6 12 1 18 14 0 0.0'
m=' [+-]*\d+\.?\d*[Ee]*[+-]*\d+'*31
index=re.findall(t+m,index)
data2=[]
d=index[0].replace(t,'').split()
print(index[0])
for f in d:
    data2.append(float(f))
print(data2)

m_s=data2[6]+(math.sqrt(3.986005e14/math.pow(data2[10],6))+data2[5])*1776
e_s=m_s
for i in range(1,100):
    e_s = m_s+data2[8] * math.sin(e_s)

f_s = math.atan2((math.sqrt(1-data2[8]*data2[8]) * math.sin(e_s)),(math.cos(e_s)-data2[8]))
u_0 = data2[17]+f_s

q_u = data2[7]*math.cos(2*u_0)+data2[9]*math.sin(2*u_0)
q_r = data2[16]*math.cos(2*u_0)+data2[4]*math.sin(2*u_0)
q_i = data2[12]*math.cos(2*u_0)+data2[14]*math.sin(2*u_0)

u = u_0+q_u
r = data2[10] * data2[10] * (1-data2[8] * math.cos(e_s))+q_r
i = data2[15] + q_i+data2[19] * 1776

l = data2[13]+data2[18]*1776 - (7.2921151467e-05 * 311376)

x = r * math.cos(u)
y = r * math.sin(u)

X = x * math.cos(l) - y * math.cos(i) * math.sin(l)
Y = x * math.cos(l) + y * math.cos(i) * math.sin(l)
Z = y * math.sin(i)
print(X,Y,Z)
print( x,y)






