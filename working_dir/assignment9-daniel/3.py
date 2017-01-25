import networkx as nx
G=nx.DiGraph(diction)

# Remove all but the (largest) strongly connected component
length = 0 
subg = None
for subgraph in nx.strongly_connected_components(G):
    if len(subgraph) > length:
        subg = subgraph
        length = len(subgraph)

# New graph for the SCC
df1 = df2.ix[list(subg)]['out_links']
df1_dict = df1.to_dict()
G=nx.DiGraph(df1_dict)
G.number_of_nodes()
pG = G.subgraph(subg)
# Print new graph diameter
print(nx.diameter(pG))
