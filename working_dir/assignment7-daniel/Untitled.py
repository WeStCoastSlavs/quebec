
# coding: utf-8

# In[1]:

d1 = "this is a text about web science".split(" ")
d2 = "web science is covering the analysis of text corpora".split(" ")
d3 = "scientific methods are used to analyze webpages".split(" ")


# In[2]:

sve = d1.copy()
sve.extend(d2)
sve.extend(d3)
sve = set(sve)


# In[3]:

len(sve)


# In[4]:

def brojac(d1):
    d1_dic = {}
    for elem in sve:
        if elem in d1:
            d1_dic[elem] = 1
        else:
            d1_dic[elem] = 0
    return d1_dic
d1_dict = brojac(d1)
d2_dict = brojac(d2)
d3_dict = brojac(d3)


# In[5]:

print(d1_dict)
print(d2_dict)


# In[6]:

def scalar(d1, d2):
    suma = 0
    for k,v in d1.items():
        suma += v * d2[k]
    return suma


# In[7]:

from math import sqrt
def euclidian_len(d1):
    return sqrt(sum([v*v for k,v in d1.items()]))
def cosine(d1, d2):
    return (scalar(d1,d2)/(euclidian_len(d1)*euclidian_len(d2)))


# In[8]:

print(cosine(d1_dict, d2_dict))
print(cosine(d1_dict, d3_dict))
print(cosine(d3_dict, d2_dict))


# # Nova stvar

# In[9]:

import pandas as pd
import re
from collections import Counter
from statistics import median, mean
data = []
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line == "\n": continue
        data.append(line)
df = pd.DataFrame(data, columns=['article'])
# df['words'] = df['article'].apply(lambda x: re.findall(r'\w+', x))
# df['word_count'] = df['words'].apply(lambda x: len(x))
# df = df.drop(df[df.word_count == 0].index)


# In[10]:

df['article'] = df['article'].apply(lambda x: x.lower())
df['article'] = df['article'].apply(lambda x: "".join([p for p in x if p.isalpha() or p==" "]))
df["counts"] = df['article'].apply(lambda x: Counter(x))
df['char_count'] = df['counts'].apply(lambda x: sum([v for k,v in x.items()]))
# df['char_count'] = df['counts'].apply(lambda x: sum([v for k,v in x.items() if k.isalpha() or k==" "]))


# In[11]:

df.head()


# In[12]:

real_data = " ".join(df["article"].values)


# In[13]:

num_chars = sum(df['char_count'])


# In[ ]:

with open("probabilities.py.txt") as prob:
    dump = []
    for line in prob:
        if line != "\n":
            dump.append(line[:-1])


# In[ ]:

exec(dump[0])
exec(dump[1])
# zipf_probabilities, uniform_probabilities


# In[ ]:

kumul_zipf = {}
suma = 0
for k,v in zipf_probabilities.items():
    suma+= v
    kumul_zipf[suma] = k
kumul_unif = {}
suma = 0
for k,v in uniform_probabilities.items():
    suma+= v
    kumul_unif[suma] = k


# In[ ]:

def find_next(num, lista):
    for elem in lista:
        if elem >= num:
            return elem


# In[ ]:

import random

def generate_chars1(number, CDF_dict):
    articles = ""
    CDF = sorted(CDF_dict)
    for i in range(0,number):
        num = random.random()
        elem = find_next(num, CDF)
        letter = CDF_dict[elem]
        articles += letter
    return articles

def generate_chars(number, CDF_dict):
    CDF = sorted(CDF_dict)
    return "".join(CDF_dict[find_next(random.random(), CDF)] for i in range(0,number))


# In[ ]:

import time
f = open('unif_data.txt', 'w')
start = time.time()
unif_data = generate_chars(num_chars, kumul_unif)
end = time.time()
print("Time taken : {}".format(end - start))
f.write(unif_data)
f.close()
f = open('zipf_data.txt', 'w')
start = time.time()
zipf_data = generate_chars(num_chars, kumul_zipf)
end = time.time()
print("Time taken : {}".format(end - start))
f.write(unif_data)
f.close()


# In[ ]:

unif_words = re.findall(r'\w+', unif_data)
zipf_words = re.findall(r'\w+', zipf_data)


# In[ ]:

unif_c = Counter(unif_words)
zipf_c = Counter(zipf_words)


# In[ ]:

words, frequencies_u = zip(*unif_c.most_common()) 


# In[ ]:

words, frequencies_z = zip(*zipf_c.most_common())    


# In[ ]:

real_words = re.findall(r'\w+', real_data)
real_c = Counter(real_words)


# In[ ]:

words, frequencies_r = zip(*real_c.most_common())   


# In[ ]:

with open("generated.txt", 'w') as g:
    g.write("{}".format(frequencies_u))
    g.write('\n')
    g.write("{}".format(frequencies_z))
    g.write('\n')
    g.write("{}".format(frequencies_r))
    g.write('\n')


# In[ ]:

# freqencies = list(map(lambda x: x**np.e, list(frequencies)))
import matplotlib.pyplot as plt
# plt.axis([0, 10**6], [0, 10**7])
plt.loglog([i for i in range(0,len(frequencies_z))], frequencies_z, label='Zipf')
plt.loglog([i for i in range(0,len(frequencies_r))], frequencies_r, color='red', label="Real")
plt.loglog([i for i in range(0,len(frequencies_u))], frequencies_u, color='green', label="Uniform")
plt.xlabel('Word rank')
plt.ylabel('Word frequency')
plt.legend(loc='upper right')
plt.show()


# In[ ]:

import numpy as np
freq_r_sum = sum(frequencies_r)
frequencies_cum_r = list(map(lambda x: x/freq_r_sum, frequencies_r))
frequencies_cum_r = np.cumsum(frequencies_cum_r)


# In[ ]:

freq_z_sum = sum(frequencies_z)
frequencies_cum_z = list(map(lambda x: x/freq_z_sum, frequencies_z))
frequencies_cum_z = np.cumsum(frequencies_cum_z)
freq_u_sum = sum(frequencies_u)
frequencies_cum_u = list(map(lambda x: x/freq_u_sum, frequencies_u))
frequencies_cum_u = np.cumsum(frequencies_cum_u)


# In[ ]:

dist_r_z = np.absolute(np.subtract(frequencies_cum_r, frequencies_cum_z[:len(frequencies_cum_r)]))
max_dist_r_z = max(dist_r_z)
max_index_r_z = np.where(dist_r_z == max_dist_r_z)
max_index_r_z = max_index_r_z[0][0]


# In[ ]:

dist_r_u = np.absolute(np.subtract(frequencies_cum_r, frequencies_cum_u[:len(frequencies_cum_r)]))
max_dist_r_u = max(dist_r_u)
max_index_r_u = np.where(dist_r_u == max_dist_r_u)
max_index_r_u = max_index_r_u[0][0]


# In[ ]:

plt.semilogx([i for i in range(0,len(frequencies_cum_r))], frequencies_cum_r, 'r')
plt.semilogx([i for i in range(0,len(frequencies_cum_u))], frequencies_cum_u, 'g')
plt.semilogx([i for i in range(0,len(frequencies_cum_z))], frequencies_cum_z, 'b')
# plt.plot([max_index_r_z,max_index_r_z], [0,1], 'b-')
axes = plt.gca()
# axes.set_xlim([xmin,xmax])
axes.set_ylim([0,1])
plt.show()


# In[ ]:



# In[ ]:



