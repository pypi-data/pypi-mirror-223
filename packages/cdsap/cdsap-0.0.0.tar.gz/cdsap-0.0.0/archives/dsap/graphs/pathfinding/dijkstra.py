""" 
    #############################################################
    # DIJKSTA'S SHORTEST PATH ALGORITHM IMPLEMENTATION [PYTHON] #
    #############################################################

    NOTES 
        * main source: programiz.com (modified implementation)
        * requires keyed-binary heap implementation 
            - refer to related project file
		* printable / narrow width 

    API 
        * weight_fn(edge_data) 
        * dijkstra(graph, src, dest) 
        * find_path(previous, src, dest)

""" 
from dsap.heaps.structs.kbh import KBH 

INFINITY = float('inf')

class DijkstraPF: 
    def __init__(self, graph): 
        self.graph = graph 

    def weight_fn(self, edge_data): 
        return edge_data 

    def run(self, src, dest = None): 
        graph = self.graph

        # initialize queue an d previous, containers  
        queue = KBH("min") 
        previous = {} 
        costs = {}

        min_cost = INFINITY

        v = graph.vertices() 
        for vertex in v: 
            previous[vertex] = None 
            if src != vertex:
                costs[vertex] = INFINITY
                queue.insert(vertex, INFINITY) 

        # initialize source vertex
        queue.insert(src, 0)
        costs[src] = 0

        # find shortest path
        while not queue.is_empty(): 
            u = queue.top() 

            break_outer = False
            
            # for each unvisited neighbor v of u 
            ckey = u.key
            ve = graph.vertex_edges(ckey) 

            for current, neighbor, edge_data in ve: 
         
                neighbor_cost = costs[neighbor]
                weight = self.weight_fn(edge_data)
                new_cost = costs[ckey] + weight

                if new_cost < neighbor_cost: 
                    costs[neighbor] = new_cost
                    previous[neighbor] = u.key  
                    if queue.has_key(neighbor): 
                        queue.set_value(neighbor, new_cost)
                    else: 
                        queue.insert(neighbor, new_cost)

                if dest is not None: 
                    if neighbor == dest: 
                        return costs, previous

            queue.pop()

                    
            if break_outer: 
                break
        
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
