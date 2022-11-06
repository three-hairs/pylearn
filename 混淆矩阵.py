from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

import pandas
import os
from dbfread import DBF

rootdir = "E:\\GIS2017\\紫金山\\conf"
list = os.listdir(rootdir)
colnames = ['ID', 'RASTERVALU', 'true']
true = []
result = []
for i in range(0, len(list)):
    if not list[i].endswith(".dbf"):
        continue
    folder = os.path.join(rootdir, list[i])
    print(folder)
    table = DBF(folder, encoding='GBK')
    df = pandas.DataFrame(iter(table))
    result_temp = df['RASTERVALU'].tolist()
    true_temp = df['true'].tolist()
    score = accuracy_score(true_temp, result_temp)
    print('score=', score)
    kappa = cohen_kappa_score(true_temp, result_temp)
    print('kappa=', kappa)
    report = classification_report(true_temp, result_temp, digits=4)
    print('report=', report)
    true.extend(true_temp)
    result.extend(result_temp)