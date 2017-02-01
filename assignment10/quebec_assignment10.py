
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
from collections import Counter
import math
import matplotlib.pyplot as plt


# In[2]:

data = pd.read_table("onlyhash.data",names=["user","date","hashtag"])
data.head()


# In[3]:

data.shape


# In[4]:

data["hashtag_list"] = data.hashtag.apply(lambda x: x.split(" "))
# data = data.head(10)
data.head(5)


# In[5]:

x = data[data["date"] == '2009-10-12']
print(len(x))
print(len(x.user.unique()))


# In[6]:

data.hashtag_list.values


# In[7]:

data.shape


# In[8]:

data.user.value_counts().mean()


# In[9]:

users = data.user.unique()
#print(len(users))
index = [i for i in range(1, len(users)+1)]

dates = data.date.unique()
index2 = [i for i in range(1, len(dates)+1)]


# In[10]:

df = pd.DataFrame(users, index=index, columns=['user'])
df = df.head(1000)


# In[11]:

data1 = data[data["user"] == "GetFreelanceJob"]
vals = data1["hashtag_list"].values
list_has = [val for sublist in vals for val in sublist]
#list_has


# In[12]:

def get_hash(user_name, dataframe):
    dataframe = dataframe[dataframe["user"] == user_name]
    hashtag_list = dataframe["hashtag_list"].values
    list_hash = [val for sublist in hashtag_list for val in sublist]
    return list_hash


# In[13]:

df["hashtags"] = df.user.apply(lambda x: get_hash(x, data))


# In[14]:

df.head()


# In[15]:

# df.hashtags.values[0]


# In[16]:

def entropy(counter_list):
#     log2 = lambda x: math.log(x,2)
    c = Counter(counter_list)
    ent = 0.0
    for k,v in c.items():
        p = float(v)/len(counter_list)
        ent = ent - p*math.log2(p)
    return ent


# In[17]:

df["user_entropy"] = df.hashtags.apply(lambda x: entropy(x))


# In[18]:

df.head()


# In[19]:

df.user_entropy.mean()


# In[20]:

# for bri 
# calc_sys_for_one_date(date):
#    return sys ent
# put it in an array 


# In[21]:

data["entropy"] = data.hashtag_list.apply(lambda x: entropy(x))


# In[22]:

data.head()


# In[23]:

grp = data.groupby(["date"]).entropy.mean()
user_entropy_by_day = grp.to_frame()
user_entropy_by_day.describe()


# In[24]:

user_entropy_by_day.head()


# In[25]:

df.head()


# In[26]:

df2 = pd.DataFrame(dates, index=index2, columns=['date'])


# In[27]:

df2.head()


# In[28]:

def get_hash_date(date, dataframe):
    dataframe = dataframe[dataframe["date"] == date]
    hashtag_list = dataframe["hashtag_list"].values
    list_hash = [val for sublist in hashtag_list for val in sublist]
    return list_hash


# In[29]:

df2["hashtags"] = df2.date.apply(lambda x: get_hash_date(x, data))


# In[30]:

df2.head()


# In[31]:

df2["sys_entropy"] = df2.hashtags.apply(lambda x: entropy(x))


# In[32]:

df2.describe()


# In[33]:

user_entropy_by_day.head()


# In[34]:

df2.head()


# In[35]:

user_entropy_by_day['date'] = user_entropy_by_day.index


# In[36]:

print(len(user_entropy_by_day))
print(len(df2))


# In[37]:

entropy_df = pd.merge(df2, user_entropy_by_day, on='date', how='outer')
len(entropy_df)


# In[38]:

entropy_df.head()


# In[39]:

ranked = entropy_df.sort_values(by="sys_entropy")
ranked.head()


# In[40]:

import matplotlib.pyplot as plt
length=len(ranked)
x = [x for x in range(0,length)]
plt.title("Sorted System Entropy and user Entropy (Average) per day")
plt.xticks(np.arange(0,max(x),40))
plt.yticks(range(0,int(max(ranked.sys_entropy)+2)))
plt.xlabel("Days Rank (based on System Entropy)")
plt.ylabel("Entropy")
plt.plot(x,ranked.entropy.values,label='User Entropy',color="r")
plt.plot(x,ranked.sys_entropy.values,label='System Entropy',color="b")
# plt.legend(loc=2)
plt.show()


# ## 2. Measuring inequality

# In[41]:

from chinese_restaurant import generateChineseRestaurant as chineseRes

customers = 1000
for i in range(0,5):
    tables, ginis = chineseRes(customers)
    plt.plot(ginis)
plt.show()


# # 3. Herding

# # Part 1 - First estimations

# In[42]:

estimations = pd.DataFrame({
        "fortress":[90,250,375],
        "tower":[250,400,300]
    })


# In[43]:

print("mean: ",estimations.fortress.mean())
print("std: ",estimations.fortress.std())
print("var: ",estimations.fortress.std()**2)


# In[44]:

# print("mean: ",estimations.tower.mean())
# print("std: ",estimations.tower.std())
# print("var: ",estimations.tower.std()**2)


# # Part 2 - After discussion

# In[45]:

estimations = pd.DataFrame({
        "fortress":[45,75,350],
        "tower":[250,200,450],
    })


# In[46]:

# print("mean: ",estimations.fortress.mean())
# print("std: ",estimations.fortress.std())
# print("var: ",estimations.fortress.std()**2)


# In[47]:

print("mean: ",estimations.tower.mean())
print("std: ",estimations.tower.std())
print("var: ",estimations.tower.std()**2)


# In[ ]:



