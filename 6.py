import csv_utilities
j = 0
with open("E:/8.csv", 'r', encoding='utf-8') as f:
    # writer=csv.writer(f)
    rows1 = csv.reader(f)
    with open("E:/9.csv", "w", encoding='UTF-8', newline='') as f2:
        writer = csv.writer(f2)
        for row1 in rows1:
            with open("E:/科居公企商111.csv", 'r', encoding='UTF-8') as f1:
                rows2 = csv.reader(f1)
                for index, row2 in enumerate(rows2):
                    if row1[0] == row2[1]:
                        row1[9] = row2[2]
                        row1[10] = row2[3]
                        row1[11] = row2[4]
                        row1[12] = row2[5]
                        row1[13] = row2[6]
                        # row1.append(row2[2])
                        # row1.append(row2[3])
                        # row1.append(row2[4])
                        # row1.append(row2[5])
                        # row1.append(row2[6])
                        # writer.writerow(row1)
                        break
                writer.writerow(row1)

