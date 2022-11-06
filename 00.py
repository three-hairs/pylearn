import os
import math
#
#
# try:
#     os.remove(r'G:/Vampire-Survivors-v0.6.104_setup.exe')
# finally:
#     print('dddd')
#
#
for s in range(0, 7):
    for f in range(0, 60):
        for m in range(0, 60):
            d_m = m/60 * 360
            d_f = f/60 * 360 + m/60 * 6
            d_s = s/12 * 360 + f/60 * 30
            a = math.fabs(d_s - d_f)
            b = math.fabs(d_f - d_m)
            a = min(a, 360 - a)
            b = min(b, 360 - b)
            if a == 2 * b:
                print('shi:{:} fen:{:} miao {:} {:.2f} {:.2f}'.format(s, f, m, a, b))
