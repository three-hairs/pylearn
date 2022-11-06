import numpy as np
import pandas as pd
file = "1.py"
point = [110, 110]
df = pd.read_csv(file, header=None, sep=' ', error_bad_lines=False)
b = np.mat(df)
length = len(df)
M = []
Z = []
P = np.zeros((length, length))
for i in range(length):
    Z.append(b[i, 2])
    P[i][i] = 1/((point[0]-b[i, 0]) * (point[0]-b[i, 0]) + (point[1]-b[i, 1]) * (point[1]-b[i, 1]))
    row = [0, 0, 0, 0, 0, 0]
    row[0], row[1], row[2], row[3], row[4], row[5] = b[i, 0] * b[i, 0], b[i, 0] * b[i, 1], b[i, 1] * b[i, 1], b[i, 0], \
                                                     b[i, 1], 1
    M.append(row)
M = np.mat(M)
Z = np.mat(Z)
x = (M.T * P.T * M).I * M.T * P.T * Z.T
row = [0, 0, 0, 0, 0, 0]
row[0], row[1], row[2], row[3], row[4], row[5] = point[0] * point[0], point[0] * point[1], \
                                            point[1] * point[1], point[0], point[1], 1
row = np.mat(row)
print(x)
print(x.T * row.T)
