F = {}
F["simple_1"] = (("A","a"),("B","b"),("C","c"),("D","d"),("A","b"),("B","a"),("B","c"),("C","d"),("D","c"))
F["simple_2"] = (("A","a"),("A","b"),("B","a"),("C","a"),("C","b"),("D","a"),("D","b"),("D","c"),("E","c"),("F","c"),("G","c"))

F["simple_1_idx"] = [x for x in "ABCDabcd"]
F["simple_1_pos_1"] = [1,3,1,1,1,1,3,1]
F["simple_1_pos_2"] = [2,4,3,3,3,3,4,2]

F["simple_2_idx"] = [x for x in "ABCDEFGabc"]
F["simple_2_pos_1"] = [1,0,1,3,0,0,0,6,3,6]
F["simple_2_pos_2"] = [5,3,5,8,3,3,3,4,4,2]

import pybip.bipartite

def test_3motifs():
    bip = pybip.Bipartite(edges=F["simple_1"]).nodes.set_index("id")
    
    assert (F["simple_1_pos_1"] == bip.loc[F["simple_1_idx"],"pos_1"].values).all
    assert (F["simple_1_pos_2"] == bip.loc[F["simple_1_idx"],"pos_2"].values).all
    
    bip = pybip.Bipartite(edges=F["simple_2"]).nodes.set_index("id")
    
    assert (F["simple_2_pos_1"] == bip.loc[F["simple_2_idx"],"pos_1"].values).all
    assert (F["simple_2_pos_2"] == bip.loc[F["simple_2_idx"],"pos_2"].values).all
