import csv
import numpy as np
j = 0
pre = []
real = []
with open("E:/QQVipDownload/1.1.arff.csv", 'r', encoding='utf-8') as f:
    # writer=csv.writer(f)
    rows1 = csv.reader(f)
    header_row = next(rows1)
    for row in rows1:
        pre.append(float(row[0]))
        real.append(float(row[1]))

real1 = np.array(real)

arr_mean = np.mean(real1)
a = np.mean(real)

b = 0
c = 0
e = 0
for i in range(0, 9):
    b = real[i] - pre[i]
    d = real[i] - a
    c = b * b + c
    e = d * d + e
r2 = 1 - c / e
rmse = np.sqrt(c / 9)
rrmse = rmse / a

print(r2, rmse, rrmse)
    # with open("E:/8.csv", "w", encoding='UTF-8', newline='') as f2:
    #     writer = csv.writer(f2)
    #     for row1 in rows1:
    #         with open("E:/科居公企商.csv", 'r', encoding='UTF-8') as f1:
    #             rows2 = csv.reader(f1)
    #             for index, row2 in enumerate(rows2):
    #                 if row1[0] == row2[1]:
    #                     row1.append(row2[2])
    #                     row1.append(row2[3])
    #                     row1.append(row2[4])
    #                     row1.append(row2[5])
    #                     row1.append(row2[6])
    #                     # writer.writerow(row1)
    #                     break
    #             writer.writerow(row1)




