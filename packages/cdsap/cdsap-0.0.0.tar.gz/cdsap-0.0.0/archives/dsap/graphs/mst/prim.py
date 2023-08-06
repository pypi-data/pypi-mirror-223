""" 
    #####################################################
    # PRIM'S MIN. SPANNING TREE IMPLEMENTATION [PYTHON] #
    #####################################################

    NOTES 
        * main source: programiz.com (modified implementation)
        * does not require other files
		* printable / narrow width 

    API 
        * source: simplilearn.com (modified implementation)
        

""" 

from dsap.graphs.structs.graph import Graph
from dsap.heaps.structs.kbh import KBH 

INFINITY = float('inf')


class PrimMST: 
    def __init__(self, graph): 
        self.graph = graph

    def weight_fn(self, edge_data): 
        return edge_data 

    def run(self): 
        graph = self.graph 

        mst = Graph(graph.directed)

        # create container for cost 
        cost = 0  

        # create container for sorted edges 
        sorted_edges = KBH("min") 

        # pick starting vertex 
        start = None 
        for vertex in graph.vertices(): 
            start = vertex 
            break

        mst.add_vertex(start)

        # store edges of starting vertex to heap 
        i = 0
        for u, v, edge_data in graph.vertex_edges(start): 
            weight = self.weight_fn(edge_data)
            sorted_edges.insert(i, weight, (u, v, edge_data)) 
            i += 1 

        # build minimum spanning tree 
        while mst.n_vertices() != graph.n_vertices():  
            min_edge = None 
            new_vertex = None 

            # find the next edge to add to the mst 
            while not sorted_edges.is_empty(): 
                # get the edge with the min. cost 
                edge = sorted_edges.top() 
                sorted_edges.pop()

                u, v, edge_data = edge.data 
                weight = edge.value 
            
                # check if edge forms a cycle with the current mst 
                if mst.has_vertex(u) and mst.has_vertex(v): 
                    continue 
                else: 
                    if not mst.has_vertex(u): 
                        mst.add_vertex(u)
                        new_vertex = u 

                    if not mst.has_vertex(v): 
                        mst.add_vertex(v)
                        new_vertex = v  

                    mst.add_edge(u, v, edge_data)
                    
                    cost += weight 
                    break  
            
            # add edges of new vertex to the sorted_edges queue/heap 
            for u, v, edge_data in graph.vertex_edges(new_vertex): 
                weight = self.weight_fn(edge_data) 
                sorted_edges.insert(i, weight, (u, v, edge_data))
                i += 1 
        
        return mst, cost 

         





 



    
