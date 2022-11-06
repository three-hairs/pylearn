import csv_utilities
import jieba
lists1 = ['风景名胜','公共厕所','公交设施服务','公司企业','购物','金融保险服务','科技文化服务','商务住宅','生活服务',
        '体育休闲服务','医疗保健服务','政府机构及社会团体','住宿服务']
for list1 in lists1:
    filename = 'E:\QQVipDownload\CSV版本\\'+list1+'.csv'
    filename1 = 'E:\QQVipDownload\CSV版本\\'+list1+'.txt'
    with open(filename) as f1:
        reader = csv.reader(f1)
        header_row = next(reader)
        highs = []
        for row in reader:
            if row[5]=="江苏省":
                highs.append(row[3])
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
