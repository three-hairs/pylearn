import math
import csv
import pandas as pd

# return sum([(x - y) ** 2 for x in records_real for y in records_predict]) / len(records_real)


def get_mse(records_real, records_predict):
    if len(records_real) == len(records_predict):
        return sum([(x-y)**2 for x, y in zip(records_real, records_predict)])/len(records_real)
    else:
        return None


def get_mse1(records_real):
    mse = sum([(x[0]-x[1])**2 for x in records_real])/len(records_real)
    return mse, math.sqrt(mse)


with open(r'C:\Users\Lenovo\Desktop\111.csv', 'r', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    records1 = [(float(row[1]), float(row[0])) for row in reader]
    # records2 = [float(a[0]) for a in records1]
    # records3 = [float(a[1]) for a in records1]
    # records1 = []
    # records2 = []
    # for row in reader:
    #     records1.append(row[1])
    #     records2.append(row[2])

rmse = get_mse1(records1)
print(rmse)
print(reader)
print(records1)
# print(records2)
# print(records3)
