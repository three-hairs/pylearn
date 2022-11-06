import os
import csv_utilities
import jieba
docList = os.listdir('E:\QQVipDownload\创训\poi分块\\result')
docList.sort()  # 显示当前文件夹下所有文件并进行排序
for i in docList:
    j = i.replace("csv", "txt")
    # print(j)
    filename = 'E:\QQVipDownload\创训\poi分块\\result\\' + i
    filename1 = 'E:\QQVipDownload\创训\poi分块\\text\\' + j
    with open(filename, encoding='UTF-8') as f1:
        reader = csv.reader(f1)
        header_row = next(reader)
        header_row = next(reader)
        highs = []
        for row in reader:
            highs.append(row[1])
    with open(filename1, "w") as f2:
        for contain in highs:
            f2.write(contain)
    with open(filename1) as f3:
        reader = f3.read()
        reader = reader.encode('GBK')
        document_cut = jieba.cut(reader)
    result = ' '.join(document_cut)
    with open(filename1, 'w')as f4:
        f4.write(result)