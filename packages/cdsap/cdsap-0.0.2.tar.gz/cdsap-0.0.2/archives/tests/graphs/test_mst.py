import pytest 
from dsap.graphs.structs.graph import Graph
from dsap.graphs.mst.prim import PrimMST 
from dsap.graphs.mst.kruskal import KruskalMST 

def test_prim_mst():
    graph = Graph(False) 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_edge("A", "B", 11)
    graph.add_edge("A", "C", 61)
    graph.add_edge("B", "C", 40)
    graph.add_edge("B", "D", 23)
    graph.add_edge("B", "E", 18)
    graph.add_edge("C", "D", 29)
    graph.add_edge("C", "E", 20)
    graph.add_edge("E", "D", 20) 
    graph.add_edge("D", "F", 38)
    graph.add_edge("E", "F", 32)   

    prim_mst = PrimMST(graph)
    mst = prim_mst.run() 

    vertices = list(mst[0].vertices()) 

    assert("A" in vertices)
    assert("B" in vertices)
    assert("C" in vertices)
    assert("D" in vertices)
    assert("E" in vertices)
    assert("F" in vertices)

    assert(mst[1] == 101)


def test_kruskal_mst():
    graph = Graph(False) 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_edge("A", "B", 11)
    graph.add_edge("A", "C", 61)
    graph.add_edge("B", "C", 40)
    graph.add_edge("B", "D", 23)
    graph.add_edge("B", "E", 18)
    graph.add_edge("C", "D", 29)
    graph.add_edge("C", "E", 20)
    graph.add_edge("E", "D", 20) 
    graph.add_edge("D", "F", 38)
    graph.add_edge("E", "F", 32)   

    kruskal_mst = KruskalMST(graph)
    mst = kruskal_mst.run() 

    vertices = list(mst[0].vertices()) 

    assert("A" in vertices)
    assert("B" in vertices)
    assert("C" in vertices)
    assert("D" in vertices)
    assert("E" in vertices)
    assert("F" in vertices)

    assert(mst[1] == 101)
