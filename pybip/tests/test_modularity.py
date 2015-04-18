from pybip import modularity
import numpy.testing as nt

F = {}
F["women"] = "Eleanor_Nye E5\nEleanor_Nye E8\nEleanor_Nye E6\nEleanor_Nye E7\nFlora_Price E9\nFlora_Price E11\nOlivia_Carleton E9\nOlivia_Carleton E11\nBrenda_Rogers E5\nBrenda_Rogers E6\nBrenda_Rogers E4\nBrenda_Rogers E8\nBrenda_Rogers E3\nBrenda_Rogers E1\nBrenda_Rogers E7\nRuth_DeSand E5\nRuth_DeSand E8\nRuth_DeSand E7\nRuth_DeSand E9\nHelen_Lloyd E8\nFrances_Anderson E8\nDorothy_Murchison E8\nSylvia_Avondale E8\nKatherina_Rogers E8\nVerne_Sanderson E8\nLaura_Mandeville E8\nPearl_Oglethorpe E8\nMyra_Liddel E8\nTheresa_Anderson E8\nEvelyn_Jefferson E8\nHelen_Lloyd E11\nNora_Fayette E11\nSylvia_Avondale E12\nSylvia_Avondale E10\nSylvia_Avondale E9\nSylvia_Avondale E7\nSylvia_Avondale E13\nSylvia_Avondale E14\nKatherina_Rogers E12\nKatherina_Rogers E10\nKatherina_Rogers E9\nKatherina_Rogers E13\nKatherina_Rogers E14\nPearl_Oglethorpe E6\nNora_Fayette E6\nLaura_Mandeville E6\nFrances_Anderson E6\nTheresa_Anderson E6\nEvelyn_Jefferson E6\nHelen_Lloyd E7\nNora_Fayette E7\nVerne_Sanderson E7\nLaura_Mandeville E7\nCharlotte_McDowd E7\nTheresa_Anderson E7\nCharlotte_McDowd E4\nCharlotte_McDowd E5\nCharlotte_McDowd E3\nHelen_Lloyd E10\nHelen_Lloyd E12\nTheresa_Anderson E4\nEvelyn_Jefferson E4\nNora_Fayette E14\nTheresa_Anderson E2\nEvelyn_Jefferson E2\nLaura_Mandeville E2\nTheresa_Anderson E5\nTheresa_Anderson E9\nTheresa_Anderson E3\nFrances_Anderson E5\nFrances_Anderson E3\nDorothy_Murchison E9\nLaura_Mandeville E3\nEvelyn_Jefferson E3\nMyra_Liddel E12\nNora_Fayette E12\nVerne_Sanderson E12\nMyra_Liddel E9\nMyra_Liddel E10\nNora_Fayette E10\nNora_Fayette E9\nNora_Fayette E13\nVerne_Sanderson E9\nLaura_Mandeville E5\nLaura_Mandeville E1\nPearl_Oglethorpe E9\nEvelyn_Jefferson E5\nEvelyn_Jefferson E9\nEvelyn_Jefferson E1"
F["women_modules"] = frozenset( (frozenset(("Olivia_Carleton", "Helen_Lloyd",
                                            "Katherina_Rogers", "Myra_Liddel",
                                            "Sylvia_Avondale", "Verne_Sanderson",
                                            "Nora_Fayette", "Dorothy_Murchison",
                                            "Flora_Price", "Pearl_Oglethorpe")),
                                 frozenset(("Brenda_Rogers", "Eleanor_Nye",
                                            "Frances_Anderson", "Laura_Mandeville",
                                            "Theresa_Anderson", "Charlotte_McDowd",
                                            "Evelyn_Jefferson", "Ruth_DeSand")
)))
F["women_modules_inv"] = frozenset((frozenset(("E3","E6", "E1", "E5", "E4", "E7", "E2", "E8")),
                                    frozenset(("E12", "E14", "E13", "E9", "E10", "E11"))))

F["simple_1"] = "A a\nB b\nC c\nD d\nA b\nB a\nB c\nC d\nD c"
F["simple_1_modules"] = frozenset((frozenset("AB"),frozenset("CD")))

F["simple_2"] = "A a\nA b\nB a\nC a\nC b\nD a\nD b\nD c\nE c\nF c\nG c\n"
F["simple_2_modules"] = frozenset((frozenset("ABCD"),frozenset("EFG")))
F["simple_2_modules_inv"] = frozenset((frozenset("ab"),frozenset("c")))

def test_modules():
    out = modularity.bipartmod_wrapper(F["women"],seed=1)
    out = frozenset([frozenset(x.id.values) for m,x in out.groupby("module")])
    assert out == F["women_modules"]

    out = modularity.bipartmod_wrapper(F["simple_1"],seed=1)
    out = frozenset([frozenset(x.id.values) for m,x in out.groupby("module")])
    assert out == F["simple_1_modules"]

    out = modularity.bipartmod_wrapper(F["simple_2"],seed=1)
    out = frozenset([frozenset(x.id.values) for m,x in out.groupby("module")])
    assert out == F["simple_2_modules"]


def test_modules_inverted():
    out = modularity.bipartmod_wrapper(F["women"],seed=1,inv=True)
    out = frozenset([frozenset(x.id.values) for m,x in out.groupby("module")])
    assert out == F["women_modules_inv"]

    out = modularity.bipartmod_wrapper(F["simple_2"],seed=1,inv=True)
    out = frozenset([frozenset(x.id.values) for m,x in out.groupby("module")])
    assert out == F["simple_2_modules_inv"]


def test_degree_participation():
    out = modularity.bipartmod_wrapper(F["simple_1"],seed=1,degree=1).set_index("id")
    idx = ["A","B","C","D"]
    nt.assert_almost_equal(out.loc[idx,"P"].values, (0,0.4444,.5,.5),3,)
    
    out = modularity.bipartmod_wrapper(F["simple_2"],seed=1,degree=1).set_index("id")
    idx = ["A","B","C","D","E","F","G"]
    nt.assert_almost_equal(out.loc[idx,"P"].values,  [0,0,0,.5,.4444,.4444,.4444],3)



def test_degree_zscore():
    out = modularity.bipartmod_wrapper(F["simple_1"],seed=1,degree=1).set_index("id")
    idx = ["A","B","C","D"]
    nt.assert_almost_equal(out.loc[idx,"z"].values, [0]*4,)

    out = modularity.bipartmod_wrapper(F["simple_2"],seed=1,degree=1).set_index("id")
    idx = ["A","B","C","D","E","F","G"]
    nt.assert_almost_equal(out.loc[idx,"z"].values, [0]*7)



def test_strength_participation():
    out = modularity.bipartmod_wrapper(F["simple_1"],seed=1).set_index("id")
    idx = ["A","B","C","D"]
    nt.assert_almost_equal(out.loc[idx,"P"].values, (0,0.5,.444,.444),3)

    out = modularity.bipartmod_wrapper(F["simple_2"],seed=1).set_index("id")
    idx = ["A","B","C","D","E","F","G"]
    nt.assert_almost_equal(out.loc[idx,"P"].values,  [0,0,0,.46875,0.4444,0.4444,0.4444],4)


def test_strength_zscore():
    out = modularity.bipartmod_wrapper(F["simple_1"],seed=1).set_index("id")
    idx = ["A","B","C","D"]
    nt.assert_almost_equal(out.loc[idx,"z"].values, [0]*4)

    out = modularity.bipartmod_wrapper(F["simple_2"],seed=1).set_index("id")
    idx = ["A","B","C","D","E","F","G"]
    nt.assert_almost_equal(out.loc[idx,"z"].values, [0.57735027, -1.73205081,  0.57735027,  0.57735027,0,0,0],4)




