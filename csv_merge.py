import os
import csv
import datetime
import csv_utilities
docList = os.listdir('E:\QQVipDownload\CSV版本')  # 特定目录下的文件存入列表
docList.sort()  # 显示当前文件夹下所有文件并进行排序
for i in docList:
    print(i)  # 输出文件名
str_time = datetime.datetime.now().strftime('%Y-%m-%d')
fname = open('E:\QQVipDownload\{0}.csv'.format(str_time), "w")  # 创建一个以当前时间命名的log文件

for i in docList:
    name='E:\QQVipDownload\CSV版本\\'+i
    x = open(name,  "r")  # 打开列表中的文件,读取文件内容
    reader = csv.reader(x)
    header_row = next(reader)
    for row in reader:
        if row[5] == "江苏省":
            for a in row:
                fname.write(a+',')
            fname.write('\n')

    x.close()  # 关闭列表文件

fname.close()



