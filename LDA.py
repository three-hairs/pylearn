import os
import csv_utilities
res = []
docList = os.listdir('E:\QQVipDownload\创训\poi分块\\text\\')
docList.sort()  # 文件排序
for dex, list1 in enumerate(docList):
    filename = 'E:\QQVipDownload\创训\poi分块\\text\\'+list1
    with open(filename) as f3:
        res.append(str(f3.read()))

from sklearn.feature_extraction.text import CountVectorizer
stpwrdpath = "stop_words.txt"
with open(stpwrdpath) as f:
    stpwrd_dic= f.read()
    stpwrdlst = stpwrd_dic.splitlines()
cntVector = CountVectorizer(stop_words=stpwrdlst)
cntTf = cntVector.fit_transform(res)
names=cntVector.get_feature_names()
print(cntTf)
print(names)

from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components=7,max_iter=1000)
docres = lda.fit_transform(cntTf)
print(docres)
print(lda.components_)

with open("E:/lda.csv", "w", encoding="UTF-8") as f:
    writer=csv.writer(f)
    for index, i in enumerate(docres):
        list2=[]
        list2.append(docList[index])
        i = i.tolist()
        list2.append(str(i.index(max(i))))
        writer.writerow(list2)

# for topic_idx, topic in enumerate(lda.components_):
#     temp=0
#     for i in range(len(names)-1):
#         if topic[i] > temp:
#             m=i
#             temp=topic[i]
#     print(names[m])

for topic_idx, topic in enumerate(lda.components_):
        print ("Topic #%d:" % topic_idx)
        print( " ".join([names[i]
                        for i in topic.argsort()[:-10 - 1:-1]]))
