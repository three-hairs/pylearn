import jieba
filename1='决策树.txt'
with open(filename1) as f3:
    reader = f3.read()
    reader = reader.encode('GBK')
    document_cut = jieba.cut(reader)
result = ' '.join(document_cut)
with open(filename1, 'w')as f4:
    f4.write(result)

res=[]
with open(filename1) as f3:
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
print(cntTf.toarray())
print(names)

from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components=1,max_iter=100)
docres = lda.fit_transform(cntTf)
print(docres)
print( '\n')
print(lda.components_)
for topic_idx, topic in enumerate(lda.components_):
    temp=0
    for i in range(len(names)-1):
        if topic[i] > temp:
            max=i
            temp=topic[i]
    print(names[max])