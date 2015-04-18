import os
import networkx as nx 
import numpy as np 
import subprocess
import pandas as pd
import io

def bipartite_modules(graph,inplace=False, **kargs):
    """
    Compute the bipartite modules from a graph using bipartmod_cl.

    The graph must have a bipartite node attribute giving which component 
    the node belongs to (True/False).

    Args:
        graph (networkx.Graph): a bipartite graph.
        inplace (bool): if false, the node attribute "module" will be 
            added to the graph.
    
    Additional keyword arguments are passed to biparmod_wrapper.

    Returns:
        (dict) node name, node module.
    """
    if not inplace:
        graph = graph.copy()

    # get the two components of the network
    part = nx.get_node_attributes(graph,"bipartite")
    if part == {}:
        raise ValueError(("The 'bipartite' node attribute giving which component"
                         "of the graph it belongs to is required."))
    
    # Write the network for bipartmod
    f = []
    # get the edges with the node from each part in the right order.
    E = [e if part[e[0]] else e[::-1] for e in graph.edges()]

    f = "\n".join(["{0[0]} {0[1]}".format(e) for e in E])
    
    # Execute bipartmod
    actors_mod = bipartmod_wrapper(f, **kargs)
    team_mod   = bipartmod_wrapper(f,inv=True,**kargs)

    modules = pd.concat((actors_mod,team_mod))
    
    if inplace:
        nx.set_node_attributes(graph,"module",modules)
    return modules



def bipartmod_wrapper(network, iteration_factor=1, cooling_factor=.950,
                      inv=False, weighted=False, seed=None,degree=False):
    """
    Run bipartmod command. 
    
    Args: 
        network (str): Network, a line by edge, nodes names separated by
            a whitespace. Edge weight can be precised in a third column.
        seed (int): Random number seed (POSITIVE Integer).
        iteraction_factor (float): Iteration factor (recommended 1.0).
        cooling_factor (float): Cooling factor (recommended 0.950-0.995).
        inv (bool): Find modules for the first column (0) or second columnd (1).
        weighted (bool): use the weighted formula of modularity.
        degree (bool): use degree based rather than strength based role metrics.

    Returns:
        (list of list): A list of the modules members. 
    """

    if seed is None:
        seed = np.random.randint(10000)

    try:
        p = subprocess.Popen(["bipartmod",
                              '-s', str(seed),
                              '-i', str(iteration_factor), 
                              '-c', str(cooling_factor),
                              '-w' if weighted else '',
                              '-p' if inv else ''
                              '-d' if degree else ''],
                             stdin  = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        p.stdin.write(network.encode())
        out = io.StringIO(p.communicate()[0].decode())

    except Exception as e:
        print(e)
        print(e.__dict__)
        raise

    modules = pd.read_csv(out, sep="\t", header=None)
    modules.columns = ["id","module","role","P","z"]
    
    modules["role"] = modules["role"].map(str.strip)
    modules["id"] = modules["id"].map(str.strip)
    
    return modules

