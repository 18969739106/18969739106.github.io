#!/usr/bin/env python
# coding: utf-8

# 
# 
# # 使用Pandas进行数据清洗
# 
# 
# 
# ![image.png](./images/author.png)
# 
# 

# ## 简介
# 
# 
# 
# Pandas 是 Python 中很流行的类库，使用它可以进行数据科学计算和数据分析。数据分析结果的好坏依赖于数据的好坏。
# - 存在数据缺失、数据格式不统一、数据错误的情况。
# - 不管是不完善的报表，还是技术处理数据的失当，都会不可避免的产生“脏”数据。
# 

# 首先要检查数据，明确数据分析目的。在此基础上：
# - 处理缺失数据
# - 添加默认值
# - 删除不完整的行
# - 删除不完整的列
# - 规范化数据类型
# - 必要的转换
# - 变量重命名
# - 保存结果
# 
# https://www.cnblogs.com/BoyceYang/p/8182053.html

# 
# 
# 
# 
# ![](./images/pandas.png)
# 

# ## 案例1： 电影数据清洗
# 
# Imdb5000数据包含了很多信息，例如演员、导演、预算、总收入，以及 IMDB 评分和上映时间。有一些列的值是缺失的，有些列的默认值是0，有的是 NaN（Not a Number）。下面我们通过使用 Pandas 提供的功能来清洗“脏”数据。数据来源:
# - https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset
# - https://raw.githubusercontent.com/sundeepblue/movie_rating_prediction/master/movie_metadata.csv

# In[60]:


import pandas as pd
data = pd.read_csv('../data/movie_metadata.csv')
data.columns


# ### 检查数据
# 
# Pandas 提供了`describe()`方法描述数据，还提供了 `head() 方法`，输出前几行数据，让我们对读入的数据有一个大致的了解。此外，Pandas 提供了一些数据切片的方法：
# - 查看一列的一些基本统计信息：`data['columnname'].describe()`
# - 选择一列：`data['columnname']`
# - 选择一列的前几行数据：`data['columnsname'][:n]`
# - 选择多列：`data[['column1','column2']]`
# - Where 条件过滤：`data[data['columnname'] > condition]`
# 

# In[63]:


data.head()


# In[64]:


from collections import Counter

freq = Counter(data['director_name'].tolist())
sorted(list(freq.items()), key=lambda x: x[1], reverse=True)[:10]


# ###    一、缺失数据
# 
# 为什么要考虑数值缺失的情况？
# 
# - 真实世界的数据很少是干净和一致的
# - 许多有趣的数据集都会丢失一些数据
# - 不同的数据源可能以不同的方式表示缺失的数据
# 
# 缺失数据是最常见的问题之一。产生这个问题可能的原因
# 
# ① 从来没有填正确过② 数据不可用③ 计算错误
# 
# 处理缺失数据的方法：
# 一、补充缺失值; 二、删除缺失值; 三、不处理

# #### 1. 使用默认值填补缺失

# In[62]:


data.isnull()[:5] # 通过这个函数查看是否有缺失值。True表示缺失，False表示没有缺失。


# ##### 👉使用空字符串填补

# In[24]:


data.director_name.fillna('')
# 此处用空字符串替代缺失值
# 该函数的使用方法：列表名称.列名.fillna('替代NA的字符')


# ##### 👉使用数值0进行填补

# In[65]:


data['duration'].fillna(0)


# #### 2.删除缺失数据
# ##### ①有缺失数据的情况就删除（一行任意出现一个缺失值我就删掉）

# In[26]:


data.dropna()[:3]
# 删除任何包含 NA 值的行：
# 可以看到原本有NA值得行全部被删除


# ##### ② 全部是缺失值才删除
# （一般情况下如果有部分缺失值是不影响整体行列的，如果有就删除会影响数据完整性）

# In[11]:


data.dropna(how='all')[:3]
# 删除任何包含 NA 值的行：
# 可以看到原本有NA值得行全部被删除


# →图示解读：我们可以发现，全部是缺失值才删除的方法很低效几乎没用
# 
# →原始数据是5043行，经过处理后仍然是5043行

# ##### ③ 至少有n个才删除
# （我们可以设定一个“门槛”，如果一行中有5个以上缺失值就删除，这样比起上面两个方法更加“中庸”）
# 
# →图示解读：但我们发现设定5个缺失值为门槛仍然不能处理，我们需要降低删除的门槛,，比如改到4个或3

# In[13]:


data.dropna(thresh=5)[:3]
# 在下面的例子中，行数据中至少要有 5 个缺失值才会删除


# ##### ④ 某个/几个列值缺失才删除
# （如果我们觉得某几个值是特别重要的、不可或缺的话，如果是缺失值该数据就没意义，就可以指定特定列）
# 
# （例如对于一个电影而言，电影名字或者导演通常是必须的要素）

# In[14]:


data.dropna(subset=['director_name','title_year'])[:3]
# 此处用subset方法删除了 'director_name','title_year'为缺失值的行


# ##### ⑤ 删除列
# （前面的操作是针对行）
# 
# （同样的方法也适用于于列，只需要补充axis=1的参数即可。默认值为axis=0 行  axis=1 列）

# In[16]:


# 删除一正列为 NA 的列：
data.dropna(axis=1, how='all')[:3] 


# In[17]:


# 删除任何包含空值的列：
data.dropna(axis=1, how='any')[:3]


# #### 3. 通过计算填充
# 使用数字类型的数据，比如，电影的时长，计算像电影平均时长可以帮我们甚至是数据集。这并不是最优解，但这个持续时间是根据其他数据估算出来的。这样的方式下，就不会因为像 0 或者 NaN这样的值在我们分析的时候而抛错。

# In[35]:


# hist
# import matplotlib.pyplot as plt
# plt.hist(data['duration']);
data['duration'] = data['duration'].fillna(data['duration'].mean())
data['duration'][:5]
# 此外还可以使用最大值 最小值 等方式填补


# ###    二、对数值类型进行规范(转换类型）
# 
# 有的时候，尤其当我们读取 csv 中一串数字的时候，有的时候数值类型的数字被读成字符串的数字，或将字符串的数字读成数据值类型的数字。

# In[21]:


data.columns


# In[36]:


data['duration'] = data['duration'].astype('int')
data['duration']
# 这就是告诉 Pandas ‘duration’列的类型是数值类型。
# 同样的，如果想把上映年读成字符串而不是数值类型，我们使用和上面类似的方法：


# In[43]:


# import numpy as np
# data['title_year']=data['title_year'].fillna(np.nan)
data['title_year'].astype(str)[:3]


# ### 三、不识别数据
# 
# 有时候我们不想看到某列或者某行的空值，但却该列缺失不是关键量不需要删除
# 可以选择忽略/不识别该数据的方法

# In[51]:


data['director_name'] = data['director_name'].replace({'NaN',''})
data['director_name'].fillna('')


# 同样的， 对于爬虫文本中可能会出现换错行的情况
# 
# 例如 原文本为112233
# 
# 因为错换行情况变成11
# 
#                 22
#             
#                 33
#                 
# 因此，用这个方法可以可以替换文本中存在的\n（还可用来其他转移转义字符 \n\t\r

# ### 四、重复数据
# 
# 有的时候数据集中会有一些重复的数据。在我们的数据集中也添加了重复的数据。

# In[52]:


# 首先我们校验一下是否存在重复记录。
# 如果存在重复记录，就使用 Pandas 提供的 drop_duplicates() 来删除重复数据。

data.drop_duplicates(['director_name','duration'],inplace=True)


# ## 案例2：病人心脏病数据
# 
# https://www.cnblogs.com/BoyceYang/p/8186033.html
# 

# In[53]:


import pandas as pd
df = pd.read_csv('../data/patient_heart_rate.csv')
df.head() 


# - 没有列头
# - 一个列有多个参数
# - 列数据的单位不统一
# - 缺失值
# - 空行
# - 重复数据
# - 非 ASCII 字符
# - 有些列头应该是数据，而不应该是列名参数

# ### 五、增加列头

# In[54]:


import pandas as pd
column_names= ['id', 'name', 'age', 'weight','m0006','m0612','m1218','f0006','f0612','f1218']
df = pd.read_csv('../data/patient_heart_rate.csv', names = column_names)
df.head(15)


# ### 六、单位列数据的单位不统一
# 
# 如果仔细观察数据集可以发现 Weight 列的单位不统一。有的单位是 kgs，有的单位是 lbs (磅）

# In[55]:


# 获取 weight 数据列中单位为 lbs 的数据
rows_with_lbs = df['weight'].str.contains('lbs').fillna(False)
df[rows_with_lbs]


# 为了解决这个问题，将单位统一，我们将单位是 lbs(磅) 的数据转换成 kgs(千克）。 `1Kg=2.20462LBS`

# In[56]:


for i,lbs_row in df[rows_with_lbs].iterrows():
    weight = int(float(lbs_row['weight'][:-3])/2.2)
    df.at[i,'weight'] = '{}kgs'.format(weight) 


# In[57]:


df.head(12)


# ### 七、空行 
# 
# 仔细对比会发现我们的数据中一行空行，除了 index 之外，全部的值都是 NaN。
# 
# Pandas 的 read_csv() 并没有可选参数来忽略空行，这样，我们就需要在数据被读入之后再使用 dropna() 进行处理，删除空行.

# In[58]:


# 删除全空的行
df.dropna(how='all',inplace=True)
df.head(12)


# In[59]:


import pandas as pd
# 增加列头
column_names= ['id', 'name', 'age', 'weight','m0006','m0612','m1218','f0006','f0612','f1218']
df = pd.read_csv('../data/patient_heart_rate.csv', names = column_names)
# 切分名字，删除源数据列
df[['first_name','last_name']] = df['name'].str.split(expand=True)
df.drop('name', axis=1, inplace=True)
# 获取 weight 数据列中单位为 lbs 的数据
rows_with_lbs = df['weight'].str.contains('lbs').fillna(False)
df[rows_with_lbs]
# 将 lbs 的数据转换为 kgs 数据
for i,lbs_row in df[rows_with_lbs].iterrows():
    weight = int(float(lbs_row['weight'][:-3])/2.2)
df.at[i,'weight'] = '{}kgs'.format(weight)
# 删除全空的行
df.dropna(how='all',inplace=True)
# 删除重复数据行
df.drop_duplicates(['first_name','last_name'],inplace=True)
# 删除非 ASCII 字符
df['first_name'].replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
df['last_name'].replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
# 切分 sex_hour 列为 sex 列和 hour 列
sorted_columns = ['id','age','weight','first_name','last_name']
df = pd.melt(df,
id_vars=sorted_columns,var_name='sex_hour',value_name='puls_rate').sort_values(sorted_columns)
df[['sex','hour']] = df['sex_hour'].apply(lambda x:pd.Series(([x[:1],'{}-{}'.format(x[1:3],x[3:])])))[[0,1]]
df.dr op('sex_hour', axis=1, inplace=True)
# 删除没有心率的数据
row_with_dashes = df['puls_rate'].str.contains('-').fillna(False)
df.drop(df[row_with_dashes].index,
inplace=True)
# 重置索引，不做也没关系，主要是为了看着美观一点
df = df.reset_index(drop=True)
print(df)


# 更多练习： https://github.com/computational-class/data_cleaning  
# 
# ![image.png](./images/end.png)
