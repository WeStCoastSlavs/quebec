
# coding: utf-8

# In[1]:

import pandas as pd
import re
from statistics import median, mean
from split_sentence import split_into_sentences
data = []
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line == "\n": continue
        data.append(line)
df = pd.DataFrame(data, columns=['article'])


# In[3]:

df['lenght_char'] = df['article'].apply(lambda x: len(x))
df['sentences'] = df['article'].apply(lambda x: len(split_into_sentences(x)))
df['words'] = df['article'].apply(lambda x: re.findall(r'\w+', x))
df['word_len'] = df['words'].apply(lambda x: [len(p) for p in x])
df['word_count'] = df['words'].apply(lambda x: len(x))


# In[4]:

df = df.drop(df[df.word_count == 0].index)


# In[5]:

df['word_avg_len'] = df['word_len'].apply(lambda x: mean(x))
df['word_med_len'] = df['word_len'].apply(lambda x: median(x))


# In[9]:

df.head()


# In[10]:

df.shape


# In[14]:

print("Third quartile: ", df.sentences.describe()["75%"])


# In[ ]:



