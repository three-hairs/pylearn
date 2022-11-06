import csv_utilities
i = -1
j = 0
with open("C:\\Users\\Lenovo\\Desktop\\1.csv") as f1:
    rows1 = csv.reader(f1)
    with open("E:/11.csv", "w", encoding="UTF-8", newline='') \
            as f2:
        writer = csv.writer(f2)
        for row1 in rows1:
            if row1[15] == '':
                i = i + 1
                with open("E:/result.csv") as f3:
                    rows2 = csv.reader(f3)
                    for index, row2 in enumerate(rows2):
                        if index == i:
                            row1[15] = row2[0]
            writer.writerow(row1)


