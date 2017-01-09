
# coding: utf-8

# In[26]:

import random
import matplotlib.pyplot as plt
def roll_die():
    return random.randint(1,6)


# In[27]:

def roll_2_dies(n_times):
    arr = []
    for i in range(0,n_times):
        x = roll_die()
        y = roll_die()
        arr.append(x+y)
    return arr


# In[28]:

# times_to_run = 100
times_to_run = 1000
arr = roll_2_dies(times_to_run)
arr2 = roll_2_dies(times_to_run)


# In[29]:

n, bins, patches = plt.hist(arr, bins=11, normed=0, facecolor='blue', alpha=0.75)
plt.xlabel('Sum of dice roll')
plt.ylabel('Frequency of sum x')
plt.title('Simultanious dice roll')
plt.xticks([i for i in range(2,13)])
plt.axis([1, 13, 0, 250])
plt.grid(True)

plt.show()


# In[30]:

from collections import Counter
counter = Counter(arr)
counter2 = Counter(arr2)
print(counter)
print(counter2)


# In[31]:

for k,v in counter.items():
    counter[k] = v/times_to_run
for k,v in counter2.items():
    counter2[k] = v/times_to_run


# In[32]:

suma = 0
for k,v in counter.items():
    suma+= v
    counter[k] = suma
suma = 0
for k,v in counter2.items():
    suma+= v
    counter2[k] = suma


# In[33]:

x_tics = []
y_tics = []
for k,v in counter.items():
    x_tics.append(k)
    y_tics.append(v)


# In[34]:

y_tics


# In[35]:

from statistics import median
med = median(arr)
bar = plt.plot(x_tics, y_tics)
plt.xlabel('Sum of dice roll')
plt.ylabel('Cumulative frequency')
plt.title('Simultanious dice roll')
plt.xticks(x_tics)
plt.yticks([0.1*i for i in range(1,11)])
plt.axis([1.5, 13, 0, 1.0])
plt.grid(True)


plt.plot([0, 13], [0.5, 0.5], 'r-', linewidth=1.5)
plt.plot([med, med], [0, 0.5], 'r-', linewidth=1.5, label="median")
plt.plot([0, 9], [y_tics[7], y_tics[7]], 'g-', linewidth=1.5, label="probability f(x)<=9")
plt.legend(loc="lower right")

plt.show()
print("Probability of f(x)<=9 is {}".format(y_tics[7]))


# In[36]:

print(med)


# In[37]:

def perform_KS(dict1, dict2):
    maximum = 0
    for k,v in dict1.items(): 
        maximum = abs(v - dict2[k]) if abs(v - dict2[k]) > maximum else maximum
    return maximum


# In[38]:

print(perform_KS(counter, counter2))


# In[ ]:




# In[ ]:



