import csv_utilities
with open("C:\\Users\\Lenovo\\Desktop\\数据1.11.csv") as f:
    rows = csv.reader(f)
    with open("C:\\Users\\Lenovo\\Desktop\\train.csv", "w", encoding='UTF-8', newline='') as f2:
        writer = csv.writer(f2)
        for row in rows:
            if row[16] != '':
                writer.writerow(row)