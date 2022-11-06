import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('E:/9.csv', header=None, sep=',', error_bad_lines=False)  # filename\csv文件，hea
col = list(df.columns)
# der=None表示头部为空，sep=' '表示数据间分隔符
df[col] = df[col].apply(pd.to_numeric, errors='coerce').fillna(0.0)
print(df.head())
print(df.tail())
# 作为示例，输出CSV文件的前5行和最后5行，

train, test = df[df[14] > 0], df[df[14] == 0]
print(train)
print(test)
features = df.columns[1:14]

clf = RandomForestClassifier(n_jobs=2, n_estimators=600, max_features=13)
y, _ = pd.factorize(train[14])
x=[]
for i in train[14]:

    x.append(i)
print(x,y)

clf.fit(train[features], x)
print(clf.predict(test[features]))


with open("E:/result1.txt", "w", encoding="UTF-8") as f:
    for i in clf.predict(test[features]):
        f.write(str(i)+'\n')

# preds = clf.predict(test[features])
# pd.crosstab(train[15], preds, rownames=['actual'], colnames=['preds'])
# print(pd.crosstab(test[15], preds, rownames=['actual'], colnames=['preds']))

# tree_in_forest = clf.estimators_[0]
# dot_data = StringIO()
# tree.export_graphviz(tree_in_forest, out_file=dot_data)
# graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
# #graph.write_pdf("irisacc.pdf")

