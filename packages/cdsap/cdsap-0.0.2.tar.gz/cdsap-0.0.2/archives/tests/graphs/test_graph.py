import pytest
from dsap.graphs.structs.graph import Graph 
 

def test_add_vertex(): 
    graph = Graph() 

    assert(len(graph.graph) == 0)

    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E")
    graph.add_vertex("F")

    assert(len(graph.graph) == 6)


@pytest.mark.depends(on=["test_add_vertex"])
def test_n_vertices(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D") 
    graph.add_vertex("E")
    graph.add_vertex("F")

    assert(graph.n_vertices() == 6) 


@pytest.mark.depends(on=["test_add_vertex"])
def test_add_edge(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)  

    assert(graph._n_edges == 10)

    
@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_n_edges(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)  

    assert(graph.n_edges() == 10) 

@pytest.mark.depends(on=["test_add_vertex"]) 
def test_has_vertex(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    assert(graph.has_vertex("A"))
    assert(graph.has_vertex("B"))
    assert(graph.has_vertex("C"))
    assert(graph.has_vertex("D")) 
    assert(graph.has_vertex("E")) 
    assert(graph.has_vertex("F")) 

    assert(not graph.has_vertex("Z"))

    
@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_has_edge(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)  

    assert(graph.has_edge("A", "B"))
    assert(graph.has_edge("A", "C"))
    assert(graph.has_edge("B", "C"))
    assert(graph.has_edge("B", "D"))
    assert(graph.has_edge("B", "E"))
    assert(graph.has_edge("C", "D"))
    assert(graph.has_edge("C", "E"))
    assert(graph.has_edge("E", "D")) 
    assert(graph.has_edge("D", "F"))
    assert(graph.has_edge("E", "F"))  

    assert(not graph.has_edge("Y", "Z"))

 
@pytest.mark.depends(on=[
    "test_add_vertex", "test_add_edge", 
    "test_has_vertex", "test_has_edge"
]) 
def test_remove_vertex(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)  

    graph.remove_vertex("A")

    assert(not graph.has_vertex("A"))
    assert(not graph.has_edge("A", "B"))
    assert(not graph.has_edge("A", "C"))
    assert(not graph.has_edge("C", "A"))



 
@pytest.mark.depends(on=[
    "test_add_vertex", "test_add_edge", 
    "test_has_vertex", "test_has_edge"
]) 
def test_remove_edge(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)  

    assert(graph.has_edge("C", "E"))

    graph.remove_edge("C", "E")

    assert(not graph.has_edge("C", "E"))



@pytest.mark.depends(on=[
    "test_add_vertex", "test_add_edge", 
    "test_has_vertex", "test_has_edge"
]) 
def test_remove_edge(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)  

    keys = set(["A", "B", "C", "D", "E", "F"]) 

    for vertex in graph.vertices(): 
        assert(vertex in keys)



@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"])
def test_edges(): 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)      

    edges = set([
        ("A", "B"), 
        ("A", "C"), 
        ("C", "A"),
        ("B", "C"),
        ("B", "D"), 
        ("B", "E"), 
        ("C", "D"),
        ("C", "E"), 
        ("E", "D"), 
        ("D", "F"),
        ("E", "F")
    ])


    for src, dest, _ in graph.edges(): 
        assert((src, dest) in edges)


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_vertex_edges():
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    
    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)      

    edges = list(graph.vertex_edges("A"))

    assert(("A", "B", None) in edges)
    assert(("A", "C", None) in edges)

@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_has_edges():
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    graph.add_vertex("G")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)      

    assert(graph.has_edges("A")) 
    assert(not graph.has_edges("G"))


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_back_edges():
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)

    back_edges = graph.back_edges()

    assert(back_edges["B"]["A"]) 
    assert(back_edges["C"]["A"])


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_is_cyclic():
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    graph.add_vertex("G")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("C", "A", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)      

    graph.add_edge("D", "B", None)
    graph.add_edge("C", "E", None)

    assert(graph.is_cyclic())
    

@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_is_acyclic():
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 
    graph.add_vertex("G")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)      

    assert(graph.is_acyclic())
    

@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_is_connected(): 
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_vertex("G")
    graph.add_vertex("H")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)   

    graph.add_edge("G", "H", None)   

    graph.add_edge("F", "G", None)

    assert(graph.is_connected()) 


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_disconnected(): 
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_vertex("G")
    graph.add_vertex("H")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", None)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)   

    graph.add_edge("G", "H", None)   
    
    assert(graph.is_disconnected()) 


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_get_data(): 
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_vertex("G")
    graph.add_vertex("H")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", 3.5)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)   
    
    assert(graph.get_data("B", "D") == 3.5) 


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_get_data(): 
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_vertex("G")
    graph.add_vertex("H")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", 3.5)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)   
    
    assert(graph.get_data("B", "D") == 3.5)


@pytest.mark.depends(on=["test_add_vertex", "test_add_edge"]) 
def test_set_data(): 
    graph = Graph() 
    
    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C") 
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F") 

    graph.add_vertex("G")
    graph.add_vertex("H")

    graph.add_edge("A", "B", None)
    graph.add_edge("A", "C", None)
    graph.add_edge("B", "C", None)
    graph.add_edge("B", "D", 3.5)
    graph.add_edge("B", "E", None)
    graph.add_edge("C", "D", None)
    graph.add_edge("C", "E", None)
    graph.add_edge("E", "D", None) 
    graph.add_edge("D", "F", None)
    graph.add_edge("E", "F", None)   

    graph.set_data("B", "D", 4.5)
    
    assert(graph.get_data("B", "D") == 4.5)