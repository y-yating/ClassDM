import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as stats

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')


#读取csv文件，根据数据集文档进行属性赋值

# 定义数据特征
attribute=["surgery"," Age ","Hospital Number","rectal temperature","pulse ","respiratory rate "," temperature of extremities","peripheral pulse","mucous membranes","capillary refill time "," pain","peristalsis "," abdominal distension","nasogastric tube ","nasogastric reflux "," nasogastric reflux PH "," rectal examination"," abdomen "," packed cell volume "," total protein "," abdominocentesis appearance "," abdomcentesis total protein","outcome ","surgical lesion"," lesion 1"," lesion 2"," lesion 3","cp_data "]
# 数值特征
attribute_num = ["rectal temperature","pulse ","respiratory rate "," nasogastric reflux PH "," packed cell volume "," total protein "," abdomcentesis total protein"]


# 读取数据
data_origin = pd.read_csv("./horse-colic.csv",  names = attribute, na_values = "?")


# 给出每个可能属性的频数

# 使用value_counts函数统计每个标称属性的取值频数
for item in attribute:
    if item not in attribute_num:
        print(item, '的频数为：\n', pd.value_counts(data_origin[item].values), '\n')


# 对数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数。

# 最大值
data_abstract = pd.DataFrame(data = data_origin[attribute_num].max(), columns = ['max'])
# 最小值
data_abstract['min'] = data_origin[attribute_num].min()
# 均值
data_abstract['mean'] = data_origin[attribute_num].mean()
# 中位数
data_abstract['median'] = data_origin[attribute_num].median()
# 四分位数
data_abstract['quartile'] = data_origin[attribute_num].describe().loc['25%']
# 缺失值个数
data_abstract['missing'] = data_origin[attribute_num].describe().loc['count'].apply(lambda x : 200-x)
print (data_abstract)


# 直方图
fig = plt.figure(figsize = (15,20))
index = 1
for item in attribute_num:
    ax = fig.add_subplot(4,2,index)
    data_origin[item].plot(kind = 'hist', title = item, ax = ax)
    index += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('./image/hist.jpg')


# qq图
fig = plt.figure(figsize = (15,20))
index = 1
for item in attribute_num:
    ax = fig.add_subplot(4,2,index)
    sm.qqplot(data_origin[item], ax = ax)
    ax.set_title(item)
    index += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('./image/qq.jpg')

# 盒图
fig = plt.figure(figsize = (15,20))
index = 1
for item in attribute_num:
    ax = fig.add_subplot(4,2,index)
    data_origin[item].plot(kind = 'box')
    index += 1
fig.savefig('./image/box.jpg')
