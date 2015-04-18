import networkx as nx
import pandas as pd
from pybip.modularity import bipartite_modules
from pybip.motifs import three_motifs

def dataframe(graph):
    nodes = bipartite_modules(graph)
    nodes.id = nodes.id.map(str.strip)
    nodes.sort("id",inplace=True)
    nodes.reset_index(inplace=True,drop=True)
    nodes["pos"] = nodes.index
    return nodes

class Bipartite():
    def __init__(self,graph=None,file=None,edges=None):
        if graph and file:
            raise ValueError("You have to choose between file or graph!")
        if graph is not None:
            self.graph  = graph.copy()
            self.graph.remove_nodes_from(nx.isolates(self.graph)) 
        if file is not None:
            with open(file,"r") as f:
                edges = [x.strip().split(" ")[:2] for x in f]
        if edges is not None:
            bipart = {}
            for e in edges:
                bipart[e[0]] = 0
                bipart[e[1]] = 1
            self.graph = nx.from_edgelist(edges)
            nx.set_node_attributes(self.graph,"bipartite",bipart)
            
        self.nodes = dataframe(self.graph)
        self.nodes["bipartite"]= self.nodes.id.map(nx.get_node_attributes(self.graph, "bipartite"))
        three_motifs(self)
        
