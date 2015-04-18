import pandas as pd
import networkx as nx
from math import factorial


def three_motifs(bipartite):
    """ Compute three motifs
    
    Args:
        bipartite (pybip.Bipartite): bipartie object
    """
    #print(bipartite.nodes.shape)
    bipartite.nodes = bipartite.nodes.set_index("id")
    bipartite.nodes["degree"] = pd.Series(bipartite.graph.degree())
    #print(bipartite.nodes.shape)
    try:
        adj = nx.adjacency_matrix(bipartite.graph, nodelist=bipartite.nodes.index)
    except Exception:
        print("ADJ. ERROR")
        print(bipartite.nodes)
        print(bipartite.nodes.index)
    
    bipartite.nodes["2degree"] = bipartite.nodes.degree.values.dot(adj.toarray())
    ##  Pos1 : (from Deg choose 2)
    bipartite.nodes["pos_1"] = bipartite.nodes.degree.map(lambda x: factorial(x) // (2 * factorial(x-2)) if x>=2 else 0 )
    bipartite.nodes["pos_2"] = bipartite.nodes["2degree"] - bipartite.nodes["degree"] 
    bipartite.nodes.reset_index(inplace=True)
