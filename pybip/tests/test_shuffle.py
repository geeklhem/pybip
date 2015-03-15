from pybip import shuffle
import networkx as nx
import numpy as np
from nose.tools import eq_ as eq 
from numpy.testing import assert_approx_equal

F = {}
def setup():
    F["i"] = np.random.randint(5,10)
    F["j"] = np.random.randint(5,10)
    F["N"] = F["i"]+F["j"]
    
    F["G"] = nx.bipartite_random_graph(F["i"],F["j"],.6)
    F["M"] = nx.bipartite.biadjacency_matrix(F["G"],range(F["i"]))

def test_connectance():
    
    connect = F["M"].sum()/F["N"]**2
    print("Connectance: ", connect)
    connect = np.zeros(1000)
    for k in range(1000):
        L = shuffle.connectance_shuffling(F["M"])
        connect[k] = L.sum()/F["N"]**2
    print("Mean connectance of 1000 shuffling: ", connect.mean())
    assert_approx_equal(F["M"].sum()/F["N"]**2, connect.mean() ,2)

def test_degree():
    for _ in range(10):
        H = shuffle.mcmc_shuffling(F["G"],N=1000,inplace=False)
        eq(nx.degree(F["G"]),nx.degree(H))
