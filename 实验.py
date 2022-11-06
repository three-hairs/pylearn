import  numpy as np
from numpy import *
import glob

prem = 0
preh=0
pref = 0
#hitrate=0
issrate=0
#falserate=0
mask = array([arange(1,4),arange(4,7),arange(7,10),arange(10,13),arange(13,16),arange(16,19)])
for count in range(0,168):
    grd = array([arange(1,4),arange(4,7),arange(7,10),arange(10,13),arange(13,16),arange(16,19)])
    pre =array([arange(1,4),arange(4,7),arange(7,10),arange(10,13),arange(13,16),arange(16,19)])
    data_sf = array([arange(1,4),arange(4,7),arange(7,10),arange(10,13),arange(13,16),arange(16,19)])
    [rows, cols] = grd.shape
    for i in range(rows):
          for j in range(cols):
            if mask[i, j] != 0 and (data_sf[i, j] == 2 or data_sf[i,j] == 3) and grd[i,j] >= 0.1 and pre[i,j] >= 0.1:
                preh += 1
            if mask[i, j] != 0 and (data_sf[i, j] == 2. or data_sf[i,j]==3) and grd[i, j] >= 0.1 and pre[i,j] < 0.1 and pre[i,j] != 9999:
                prem += 1
            if mask[i,j] != 0 and (data_sf[i,j]==2. or data_sf[i,j]==3) and grd[i, j]< 0.1 and pre[i, j] >= 0.1:
                pref += 1
print(preh)
print(prem)
print(pref)
print(mask)