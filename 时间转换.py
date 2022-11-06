from datetime import datetime

day1='2012-02-24 11:25:30'
date1,time1=day1.split()
n,y,r = date1.split('-')
n,y,r=int(n),int(y),int(r)
next_day = datetime(n,y,r)
cur_day = datetime(2000,1,1)

h, m, s = time1.strip().split(':')
num=(float(h)*3600+float(m) * 60+ float(s)) / (24 * 3600)
jd=(next_day - cur_day).days+2451544.5+num
print("JD =",jd)
if (n%4 == 0):
    li=[31,29,31,30,31,30,31,31,30,31,30,31]
    days=0
    for i in range(0,y-1):
        days=days+li[i]
    days=days+r
else:
    li = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days = 0
    for i in range(0, y - 1):
        days = days + li[i]
    days = days + r

print(n,"+",days)

day2='2010-11-27 23:59:59.999999999'
date2,time2=day2.split()
n,y,r = date2.split('-')
n,y,r=int(n),int(y),int(r)
cur_day2 = datetime(1980,1,6)
next_day2 = datetime(n,y,r)
h, m, s = time2.strip().split(':')
h, m, s = float(h), float(m), float(s)

week=int((next_day2 - cur_day2).days/7)
tow=(next_day2 - cur_day2).days % 7 * 3600 * 24 + h * 3600 + m * 60 + s
print(week,"+",tow)