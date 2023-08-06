import pytest 

from dsap.graphs.structs.graph import Graph

from dsap.graphs.pathfinding.dijkstra import DijkstraPF
from dsap.graphs.pathfinding.astar import AStarPF 
from dsap.graphs.pathfinding.bellman_ford import BellmanFordPF
from dsap.graphs.pathfinding.floyd_warshall import FloydWarshallPF

def test_dijkstra(): 
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

    d_pf  = DijkstraPF(graph)
    d_pf_run = d_pf.run("A")
    d_pf_p = d_pf.find_path(d_pf_run[1], "A", "F")
    
    assert(d_pf_run[0]["F"] == 61) 
    assert(d_pf_p == ["A", "B", "E", "F"])


def test_astar(): 
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

    point_map = {
        "A" : (10, 10), 
        "B" : (12, 38), 
        "C" : (38, 23), 
        "D" : (45, 12), 
        "E" : (11, 27), 
        "F" : (14, 59)
    }
        
    as_pf = AStarPF(graph, point_map) 
    as_pf_run = as_pf.run("A", "F")
    as_pf_p = as_pf.find_path(as_pf_run[1], "A", "F") 

    assert(as_pf_run[0][1]["F"] == 61) 
    assert(as_pf_p == ["A", "B", "E", "F"])


def test_bellman_ford(): 
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
        
    bf_pf = BellmanFordPF(graph) 
    bf_pf_run = bf_pf.run("A")
    bf_pf_p = bf_pf.find_path(bf_pf_run[1], "A", "F")

    assert(bf_pf_run[0]["F"] == 61) 
    assert(bf_pf_p == ["A", "B", "E", "F"])

def test_floyd_warshall(): 
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

    fw_pf = FloydWarshallPF(graph) 
    fw_pf_run = fw_pf.run()
    fw_pf_p = fw_pf.find_path(fw_pf_run, "A", "F")

    cost = fw_pf.find_cost(fw_pf_run, "A", "F")
    assert(cost == 61)
    assert(fw_pf_p == ["A", "B", "E", "F"])
