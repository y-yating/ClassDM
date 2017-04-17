import operator
import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as stats

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')


attribute=["surgery"," Age ","Hospital Number","rectal temperature","pulse ","respiratory rate "," temperature of extremities","peripheral pulse","mucous membranes","capillary refill time "," pain","peristalsis "," abdominal distension","nasogastric tube ","nasogastric reflux "," nasogastric reflux PH "," rectal examination"," abdomen "," packed cell volume "," total protein "," abdominocentesis appearance "," abdomcentesis total protein","outcome ","surgical lesion"," lesion 1"," lesion 2"," lesion 3","cp_data "]
attribute_num = ["rectal temperature","pulse ","respiratory rate "," nasogastric reflux PH "," packed cell volume "," total protein "," abdomcentesis total protein"]


# 读取数据
data_horse = pd.read_csv("./horse-colic.csv",  names = attribute, na_values = "?")


# 找出含有缺失值的数据条目索引值
nan_list = pd.isnull(data_horse).any(1).nonzero()[0]

# 使用dropna()函数操作删除缺失值
# 将缺失值对应的数据整条剔除，生成新数据集
data_filtrated = data_horse.dropna()

# 绘制可视化图
fig = plt.figure(figsize = (30,20))
i = 1
for item in attribute:
    ax = fig.add_subplot(4,7,i)
    ax.set_title(item)
    data_horse[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', legend = True)
    ax.axvline(data_horse[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'g')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('./image/missing_1.jpg')
data_filtrated.to_csv('./output/missing_1.csv', mode = 'w', encoding='utf-8', index = False,header = False)

# 用最高频率值来填补缺失值
data_filtrated = data_horse.copy()
for item in attribute:
    # 计算最高频率的值
    most_frequent_value = data_filtrated[item].value_counts().idxmax()
    # 替换缺失值
    data_filtrated[item].fillna(value = most_frequent_value, inplace = True)

# 绘制可视化图
fig = plt.figure(figsize = (30,20))
i = 1
for item in attribute:
    ax = fig.add_subplot(4,7,i)
    ax.set_title(item)
    data_horse[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(data_horse[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'g')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('./image/missing_2.jpg')
data_filtrated.to_csv('./output/missing_2.csv', mode = 'w', encoding='utf-8', index = False,header = False)


# 通过属性的相关关系来填补缺失值
# 使用pandas中Series的***interpolate()***函数，对数值属性进行插值计算，并替换缺失值。
# 建立原始数据的拷贝
data_filtrated = data_horse.copy()
for item in attribute:
    data_filtrated[item].interpolate(inplace = True)

# 绘制可视化图
fig = plt.figure(figsize = (30,20))
i = 1
for item in attribute:
    ax = fig.add_subplot(4,7,i)
    ax.set_title(item)
    data_horse[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(data_horse[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'g')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

# 保存图像和处理后数据
fig.savefig('./image/missing_3.jpg')
data_filtrated.to_csv('./output/missing_3.csv', mode = 'w', encoding='utf-8', index = False,header = False)


# 通过数据对象之间的相似性来填补缺失值 
data_norm = data_horse.copy()
# 将数值属性的缺失值替换为0
data_norm[attribute] = data_norm[attribute].fillna(0)
# 对数据进行正则化
data_norm[attribute] = data_norm[attribute].apply(lambda x : (x - np.mean(x)) / (np.max(x) - np.min(x)))
# 构造分数表
score = {}
range_length = len(data_horse)
for i in range(0, range_length):
    score[i] = {}
    for j in range(0, range_length):
        score[i][j] = 0    

# 在处理后的数据中，对每两条数据条目计算差异性得分，分值越高差异性越大
for i in range(0, range_length):
    for j in range(i, range_length):
        for item in attribute:
            temp = abs(data_norm.iloc[i][item] - data_norm.iloc[j][item])
            score[i][j] += temp
        score[j][i] = score[i][j]
data_filtrated = data_horse.copy()

# 对有缺失值的条目，用和它相似度最高（得分最低）的数据条目中对应属性的值替换
for index in nan_list:
    best_friend = sorted(score[index].items(), key=operator.itemgetter(1), reverse = False)[1][0]
    for item in attribute:
        if pd.isnull(data_filtrated.iloc[index][item]):
            if pd.isnull(data_horse.iloc[best_friend][item]):
                data_filtrated.ix[index, item] = data_horse[item].value_counts().idxmax()
            else:
                data_filtrated.ix[index, item] = data_horse.iloc[best_friend][item]

# 绘制可视化图
fig = plt.figure(figsize = (30,20))
i = 1
for item in attribute:
    ax = fig.add_subplot(4,7,i)
    ax.set_title(item)
    data_horse[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', legend = True)
    data_filtrated[item].plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'droped', legend = True)
    ax.axvline(data_horse[item].mean(), color = 'r')
    ax.axvline(data_filtrated[item].mean(), color = 'g')
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('./image/missing_4.jpg')
data_filtrated.to_csv('./output/missing_4.csv', mode = 'w', encoding='utf-8', index = False,header = False)

