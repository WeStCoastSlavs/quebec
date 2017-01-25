import pandas as pd
df2 = pd.read_csv('df2.csv', encoding='utf-8', index_col=0, header=0)
# CSV parsing
df2.out_links = df2.out_links.apply(lambda x: x.replace('[', ''))
df2.out_links = df2.out_links.apply(lambda x: x.replace(']', ''))
df2.out_links = df2.out_links.apply(lambda x: x.split(', '))

df2['link_num'] = df2.out_links.apply(lambda x: len(x))
df2 = df2.sort_values(by="link_num", ascending=False)
df2 = df2.drop_duplicates(subset = "name")
df2 = df2.set_index('name')
# df2 = df2.head(500)

diction = df2.to_dict()['out_links']


from time import time
def floydwarshall(graph):
    start = time()
    dist = {}
    pred = {}
    for u in graph.keys():
        dist[u] = {}
        pred[u] = {}
        for v in graph.keys():
            dist[u][v] = 1000
            pred[u][v] = -1
        dist[u][u] = 0
        for neighbor in graph[u]:
            dist[u][neighbor] = 1
            pred[u][neighbor] = u
            
    print(time() - start)
    
    diameter = 0
 
    for t in graph.keys():
        # given dist u to v, check if path u - t - v is shorter
        for u in graph.keys():
            for v in graph.keys():
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
                  # pred[u][v] = pred[t][v] 
                    # route new path through t
    
    print(time() - start)
 
    return dist, pred


dist, pred = floydwarshall(diction)
# Ignore nodes that are not connected
only_d = [l for key in dist.keys() for l in dist[key].values() if l < 1000]
print(max(only_d))

