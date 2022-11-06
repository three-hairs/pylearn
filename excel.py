# coding=utf-8
import os
import numpy as np

path="C:\\Users\\Lenovo\\Desktop\\2.第二次测量分好类遥感数据\\1.石楠3"
files=os.listdir(path)
xls=[]
xls1=[]
x=[]
for file in files:
    pos=path+'\\'+file
    with open(pos,'r') as f:
        datas=f.readlines()
        for index,row in enumerate(datas):
            if index>=23:
                x=row.strip().split()
                if float(x[0])>797.0:
                    xls.append(float(x[-1]))
                else:
                    continue
            else:
                continue
        if len(xls)>0:
             xls.append(xls[-1])
             xls.append(xls[-1])
        i = 0
        for a in xls[2:-2]:
            xls1.append(np.mean(xls[i:i + 5]))
            i = i + 1
        xls.clear()
        pos2=path+'\\mean'+file
        with open(pos2,'w') as f2:
            m=0
            for index,row in enumerate(datas):
                if index >= 23:
                    if float(x[0]) < 800.0:
                        f2.write(x[0]+' ')
                        f2.write(x[-1]+'\n')
                    else:
                        f2.write(x[0]+ ' ')
                        f2.write(str(xls1[m])+'\n')
                        m=m+1
                m=0
                else:
                    continue
            xls1.clear()




