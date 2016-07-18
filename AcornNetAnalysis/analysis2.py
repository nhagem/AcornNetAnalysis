import networkx as nx

G=nx.read_edgelist("../Data/Gbird_edgelist.gz")

# Replace this later with a read-in of the tag ID file for unique values
tags = 60

print(nx.degree_centrality(G))
print(list(nx.find_cliques(G)))

