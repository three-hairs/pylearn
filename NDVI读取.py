# -*- coding: UTF-8 -*-
import re
import xlwt

workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet('My Worksheet')
style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = 'Times New Roman'
font.bold = False  # 黑体
font.underline = False  # 下划线
font.italic = False  # 斜体字
style.font = font  # 设定样式
worksheet.write(0, 0, 'OBJECTID')  # 不带样式的写入
worksheet.write(0, 1, 'NDVI_Mean')  # 不带样式的写入
a=1
m='number='
b='E:/QQVipDownload/创训/道路NDVI.txt'
with open(b, "r") as f1:
    data1=f1.readlines()
    for indx, i in enumerate(data1):
        if m in i:
            index = re.findall(r"number=\d+", i)[0].replace(m, '')

            ls = data1[indx+2].strip('\n').replace(' ', '').replace('、', '/').replace('?', '').split()
            print(ls[3])
            worksheet.write(a, 0, index.replace(m,''))  # 不带样式的写入
            worksheet.write(a, 1, ls[3])
            a = a+1
workbook.save('formattng.xls')  # 保存文件
print(a)




    # ls = data1[3].strip('\n').replace(' ', '').replace('、', '/').replace('?', '').split()
    # print(ls)
    # for index,i in enumerate(ls):
    #     if (index == 3):
    #         print(i)


# for line in data1:
#     data2 = line.encode("GBK")
#     print (data2[0])
#     m = re.findall(r"[0-9]:", data2[0])
#     if m:
#         results.append(line)
# #
#     # for i in data2[0]:
#     # data3=i.split(":")
#     # print data3
#     # if data3>=0 and data3<=50000:
#     #  results.append(line)
#
#     # if i=='1':
#     #  results.append(line)
#
# f2 = open('deal.txt', 'w')
# f2.writelines(results)
# f2.close()
