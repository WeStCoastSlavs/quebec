
# coding: utf-8

# In[121]:

import pandas as pd
df2 = pd.read_csv('df2.csv', encoding='utf-8', index_col=0, header=0)


# In[122]:

df2.out_links = df2.out_links.apply(lambda x: x.replace('[', ''))
df2.out_links = df2.out_links.apply(lambda x: x.replace(']', ''))
df2.out_links = df2.out_links.apply(lambda x: x.split(', '))
df2['link_num'] = df2.out_links.apply(lambda x: len(x))
df2 = df2.sort_values(by="link_num", ascending=False)


# In[123]:

df2 = df2.drop_duplicates(subset = "name")


# In[124]:

df2 = df2.set_index('name')


# In[125]:

# df2 = df2.head(500)


# In[126]:

len(df2)


# In[127]:

diction = df2.to_dict()['out_links']


# In[128]:

from time import time
def floydwarshall(graph):
 
    # Initialize dist and pred:
    # copy graph into dist, but add infinite where there is
    # no edge, and 0 in the diagonal
    start = time()
    dist = {}
#     pred = {}
    for u in graph.keys():
        dist[u] = {}
#         pred[u] = {}
        for v in graph.keys():
            dist[u][v] = 1000
            pred[u][v] = -1
        dist[u][u] = 0
        for neighbor in graph[u]:
            dist[u][neighbor] = 1
#             pred[u][neighbor] = u
            
    print(time() - start)
    
    diameter = 0
 
    for t in graph.keys():
        # given dist u to v, check if path u - t - v is shorter
        for u in graph.keys():
            for v in graph.keys():
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
#                   pred[u][v] = pred[t][v] 
                    # route new path through t
    
    print(time() - start)
 
    return dist, pred


# In[129]:

# dist, pred = floydwarshall(diction)
# only_d = [l for key in dist.keys() for l in dist[key].values() if l < 1000]
# max(only_d)


# In[130]:

import networkx as nx
G=nx.DiGraph(diction)


# In[131]:

G.number_of_nodes()


# In[132]:

G.number_of_edges()


# In[133]:

G.edges()


# In[144]:

length = 0 
subg = None
for subgraph in nx.strongly_connected_components(G):
    if len(subgraph) > length:
        subg = subgraph
        length = len(subgraph)


# In[146]:

len(subg)


# In[156]:

df1 = df2.ix[list(subg)]['out_links']


# In[157]:

df1_dict = df1.to_dict()
G=nx.DiGraph(df1_dict)
# print(nx.diameter(G))


# In[158]:

G.number_of_nodes()


# In[159]:

len(df1)


# In[160]:

pG = G.subgraph(subg)


# In[162]:

print(nx.diameter(pG))


# In[ ]:



