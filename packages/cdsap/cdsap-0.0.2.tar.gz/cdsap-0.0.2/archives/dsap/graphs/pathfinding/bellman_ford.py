""" 
    ################################################################
    # BELLMAN-FORD SHORTEST PATH ALGORITHM IMPLEMENTATION [PYTHON] #
    ################################################################

    NOTES 
        * main source: programiz.com (modified implementation)
        * does not require other files
		* printable / narrow width 

    API 
        * weight_fn(edge_data) 
        * bellman_ford(graph, src, dest) 
        * find_path(previous, src, dest)

""" 
from dsap.heaps.structs.kbh import KBH 

INFINITY = float('inf')

class BellmanFordPF: 
    def __init__(self, graph):
        self.graph = graph

    def weight_fn(self, edge_data): 
        return edge_data
 
    def run(self, src): 
        graph = self.graph

        # initialize queue an d previous, containers  
        previous = {} 
        costs = {}

        min_cost = INFINITY

        v = graph.vertices() 
        for vertex in v: 
            costs[vertex] = INFINITY
            previous[vertex] = None 

        # initialize source vertex
        costs[src] = 0

        # find shortest path 
        V = graph.n_vertices() 
        for i in range(V): 
            for u, v, edge_data in graph.edges(): 
                weight_v = self.weight_fn(edge_data)
                new_cost = costs[u] + weight_v
                if new_cost < costs[v]: 
                    costs[v] = new_cost 
                    previous[v] = u 
        
        # check if negative cycle exists 
        for u, v, edge_data in graph.edges(): 
            weight_v = self.weight_fn(edge_data)
            if costs[u] + weight_v < costs[v]: 
                raise Error("Negative Cycle Exists.")

        return costs, previous 

    def find_path(self, previous, src, dest):
        curr = previous[dest] 
        path = [dest]

        while True: 
            path.append(curr)

            if curr == src: 
                break 
        
            if curr == None: 
                return None 
        
            curr = previous[curr] 

        return path[::-1]
