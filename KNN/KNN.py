import csv
import random

#读取
with open('Prostate_Cancer.csv','r') as file:
    reader = csv.DictReader(file)
    datas=[row for row in reader]

# 分组
random.shuffle(datas)
n=len(datas)//3

text_set=datas[0:n]
train_set=datas[n:]

# print(text_set)

# KNN
# 距离
def distance(d1,d2):
    res=0

    for key in ("radius","texture","perimeter","area","smoothness","compactness","symmetry","fractal_dimension"):
        res+=(float(d1[key])-float(d2[key]))**2

    return res**0.5

K = 10
# 四种方法固定不变
def knn(data):
    # 1距离
    res = [

        {"结果":train["diagnosis_result"],"距离":distance(data,train)}
        for train in train_set
    ]

    # print(res)

    # 2排序-升序
    res = sorted(res,key=lambda item:item['距离'])

    # 3取前K个
    res2 = res[0:K]

    # 4加权平均
    result={'B':0,'M':0}

    # 总距离
    sum=0
    for r in res2:
        sum+=r['距离']

    for r in res2:
        result[r['结果']]+=1-r['距离']/sum

    print(result)
    print(data['diagnosis_result'])

    if result['B']>result['M']:
        return 'B'
    else:
        return 'M'


knn(text_set[0])

# 测试阶段
correct = 0
for text in text_set:
    result = text['diagnosis_result']
    result2 = knn(text)

    if result == result2:
        correct+=1

print(correct)
print(len(text_set))

print("准确率：{:.2f}%".format(100*correct/len(text_set)))