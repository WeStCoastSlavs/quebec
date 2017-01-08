
# coding: utf-8

# In[1]:

import pandas as pd
df1 = pd.read_csv('df1.csv', encoding='utf-8', index_col=0, header=0)
df2 = pd.read_csv('df2.csv', encoding='utf-8', index_col=0, header=0)


# In[2]:

import numpy as np


# In[3]:

df1.head()


# In[4]:

df2.head()


# In[5]:

df1 = df1.drop_duplicates(subset=['name'])
df2 = df2.drop_duplicates(subset=['name'])


# In[6]:

df2.shape


# In[7]:

import re 
df1["words"] = df1.text.apply(lambda x: set(re.findall("\w+",str(x))))
df1["word_list"] = df1.text.apply(lambda x: re.findall("\w+",str(x)))


# In[8]:

df1.head()


# In[9]:

x = df1.head().words[0]


# In[10]:

print(len(x))
print(len(set(x)))


# In[11]:

#intersetion_cardinality = len(set.intersection(*[set(x), set(y)]))
def calc_jaccard_simmilarity(wordset1, wordset2):
    intersetion_cardinality = len(set.intersection(wordset1, wordset2))
    union_cardinality = len(set.union(wordset1, wordset2))
    return intersetion_cardinality/float(union_cardinality)


# In[12]:

calc_jaccard_simmilarity(set(["red", "blue", "yellow"]), set(["green", "red", "orange"]))


# In[13]:

dfe = df1[df1["name"] == "Europe"]
europe_words = dfe.words.values[0]
dfg = df1[df1["name"] == "Germany"]
germany_words = dfg.words.values[0]


# In[14]:

calc_jaccard_simmilarity(europe_words, germany_words)


# In[15]:

# dfg = df1[df1["name"] == "German"]
# german = dfg.words.values[0]


# In[16]:

# calc_jaccard_simmilarity(german, germany)


# In[17]:

from collections import Counter
df1['tf'] = df1.word_list.apply(lambda x: Counter(x))


# In[18]:

df1.head()


# In[19]:

words = df1.words.tolist()


# In[20]:

all_words = [word for sets in words for word in sets]


# In[21]:

doc_freq = Counter(all_words)


# In[22]:

def tf_dict_to_tfidf(tf_dic):
    new_dic = {}
    for k,v in tf_dic.items():
        new_dic[k] = v / float(doc_freq[k])
    return new_dic
df1['tf_idf'] = df1.tf.apply(tf_dict_to_tfidf)


# In[23]:

df1.head()


# In[24]:

from math import sqrt
def euclidian_len(d1):
    return sqrt(sum([v*v for k,v in d1.items()]))

def scalar(d1, d2):
    suma = 0
    for k,v in d1.items():
        try:
            suma += v * d2[k]
        except KeyError:
            pass
    return suma

def calc_cosine_similarity(d1,d2):
    return (scalar(d1,d2)/(euclidian_len(d1)*euclidian_len(d2)))


# In[25]:

dfe = df1[df1["name"] == "Europe"]
europe = dfe.words.values[0]
dfg = df1[df1["name"] == "Germany"]
germany = dfg.words.values[0]


# In[26]:

calc_cosine_similarity(dfg.tf_idf.values[0], dfe.tf_idf.values[0])


# In[27]:

dfe2 = df2[df2["name"] == "Europe"]
europe_links = dfe2.out_links.values[0]
dfg2 = df2[df2["name"] == "Germany"]
germany_links = dfg2.out_links.values[0]


# In[28]:

df2.head()


# In[29]:

calc_jaccard_simmilarity(set(europe_links), set(germany_links))


# In[30]:

df1.head()


# In[31]:

df1['cos_ger'] = df1.tf_idf.apply(lambda x: calc_cosine_similarity(x, dfg.tf_idf.values[0]))


# In[32]:

df1['jac_ger'] = df1.words.apply(lambda x: calc_jaccard_simmilarity(x, germany_words))


# In[33]:

df2['jac_ger_links'] = df2.out_links.apply(lambda x: calc_jaccard_simmilarity(set(x), set(germany_links)))


# In[34]:

df3 = pd.merge(df1[['name', 'cos_ger', 'jac_ger']], df2[['name', 'jac_ger_links']], on='name', how='left')


# In[35]:

cos_text = df3.sort_values('cos_ger', ascending=False).head(10)['name']
jac_text = df3.sort_values('jac_ger', ascending=False).head(10)['name']
jac_links = df3.sort_values('jac_ger_links', ascending=False).head(10)['name']


# In[36]:

df1.shape


# In[37]:

df3.head()


# In[38]:

df1 = df1.head(1000)
df_jac_text = pd.DataFrame(df1.name)
names = df1.name.values
for name in names:
    helper = df1[df1["name"] == name].words.values[0]
    df_jac_text[name] = df1.words.apply(lambda x: calc_jaccard_simmilarity(x, helper))


# In[39]:

df_jac_text


# In[40]:

df_cos_text = pd.DataFrame(df1.name)
names = df1.name.values
for name in names:
    helper = df1[df1["name"] == name].tf_idf.values[0]
    df_cos_text[name] = df1.tf_idf.apply(lambda x: calc_cosine_similarity(x, helper))


# In[41]:

df_cos_text.set_index('name', inplace=True)
df_cos_text = df_cos_text.rename_axis(None)


# In[42]:

df_cos_text = df_cos_text.where(np.triu(np.ones(df_cos_text.shape)).astype(np.bool))


# In[43]:

df_cos_text = df_cos_text.stack()


# In[44]:

df_cos_text = df_cos_text.reset_index()


# In[45]:

df_cos_text.columns= ['Article1', 'Article2', 'CosineText']


# In[46]:

df_cos_text = df_cos_text.sort_values(by='CosineText', ascending=False)
# df_cos_text.drop_duplicates(subset=['Article1', 'Article2'], inplace=True, keep=False)
df_cos_text = df_cos_text[df_cos_text.Article1 != df_cos_text.Article2]
ranks = pd.Series([i for i in range(1, df_cos_text.shape[0]+1)])
df_cos_text['cos_rank'] = ranks.values


# In[47]:

df_cos_text.head()


# In[48]:

df_jac_text = pd.DataFrame(df1.name)
names = df1.name.values
for name in names:
    helper = df1[df1["name"] == name].words.values[0]
    df_jac_text[name] = df1.words.apply(lambda x: calc_jaccard_simmilarity(x, helper))
df_jac_text.set_index('name', inplace=True)
df_jac_text = df_jac_text.rename_axis(None)
df_jac_text = df_jac_text.where(np.triu(np.ones(df_jac_text.shape)).astype(np.bool))

df_jac_text = df_jac_text.stack()
df_jac_text = df_jac_text.reset_index()
df_jac_text.columns= ['Article1', 'Article2', 'JaccardText']
df_jac_text = df_jac_text.sort_values(by='JaccardText', ascending=False)
df_jac_text = df_jac_text[df_jac_text.Article1 != df_jac_text.Article2]
ranks = pd.Series([i for i in range(1, df_jac_text.shape[0]+1)])
df_jac_text['jac_rank'] = ranks.values


# In[49]:

df_jac_text.head()


# In[50]:

df2 = df2.head(1000)


# In[51]:

df_jac_links = pd.DataFrame(df2.name)
names = df2.name.values
for name in names:
    helper = df2[df2["name"] == name].out_links.values[0]
    df_jac_links[name] = df2.out_links.apply(lambda x: calc_jaccard_simmilarity(set(x), set(helper)))
df_jac_links.set_index('name', inplace=True)
df_jac_links = df_jac_links.rename_axis(None)
df_jac_links = df_jac_links.where(np.triu(np.ones(df_jac_links.shape)).astype(np.bool))

df_jac_links = df_jac_links.stack()
df_jac_links = df_jac_links.reset_index()
df_jac_links.columns= ['Article1', 'Article2', 'JaccardLinks']
df_jac_links = df_jac_links.sort_values(by='JaccardLinks', ascending=False)
df_jac_links = df_jac_links[df_jac_links.Article1 != df_jac_links.Article2]
ranks = pd.Series([i for i in range(1, df_jac_links.shape[0]+1)])
df_jac_links['jac_rank_l'] = ranks.values


# In[52]:

df_jac_links.head()


# In[53]:

df_sim = pd.merge(df_cos_text, df_jac_text, on=['Article1', 'Article2'])
df_sim = pd.merge(df_sim, df_jac_links, on=['Article1', 'Article2'])


# In[54]:

df_sim.sort_values(by="CosineText", ascending=False).head(15)


# In[55]:

df_sim['diff'] = np.square(df_sim['cos_rank'] - df_sim['jac_rank'])
df_sim['diff1'] = np.square(df_sim['cos_rank'] - df_sim['jac_rank_l'])
df_sim['diff2'] = np.square(df_sim['jac_rank'] - df_sim['jac_rank_l'])


# In[56]:

df_sim.head()


# In[57]:

sum(df_sim['diff'])


# In[58]:

sum(df_sim['diff1'])


# In[59]:

sum(df_sim['diff2'])


# In[60]:

def rho(diff_column, n): 
    return 1 - (6*sum(diff_column))/(n*(n**2 -1))


# In[61]:

# cos and jaccard
rho(df_sim['diff'], df_sim.shape[0]) 


# In[62]:

# cos and jaccard_links
rho(df_sim['diff1'], df_sim.shape[0])


# In[63]:

# jaccard and jaccard_links
rho(df_sim['diff2'], df_sim.shape[0])


# In[65]:

np.square(27500)


# In[ ]:



