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

class AStarPF: 
    def __init__(self, graph, point_map = {}): 
        self.graph = graph 
        self.point_map = point_map

    def point_fn(self, x):
        return self.point_map[x]

    def weight_fn(self, edge_data): 
        return edge_data 

    def dist(self, a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1/2)

    def heuristic(self, a, b):
        a = self.point_fn(a) 
        b = self.point_fn(b) 
        return self.dist(a, b)

    def run(self, src, dest): 
        graph = self.graph

        # initialize queue an d previous, containers  
        queue = KBH("min") 
        previous = {} 
        costs = {}
        actual_costs = {} 

        min_cost = INFINITY

        v = graph.vertices() 
        for vertex in v: 
            previous[vertex] = None 
            if src != vertex:
                costs[vertex] = INFINITY
                actual_costs[vertex] = INFINITY
                queue.insert(vertex, INFINITY) 


        # initialize source vertex
        queue.insert(src, 0)
        costs[src] = 0
        actual_costs[src] = 0

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
                heuristic = self.heuristic(neighbor, dest)
                base_cost = costs[ckey] + weight
                actual_cost = actual_costs[ckey] + weight
                new_cost = base_cost + heuristic

                if new_cost < neighbor_cost: 
                    actual_costs[neighbor] = actual_cost
                    costs[neighbor] = new_cost
                    previous[neighbor] = u.key  
                    if queue.has_key(neighbor): 
                        queue.set_value(neighbor, new_cost)
                    else: 
                        queue.insert(neighbor, new_cost)

                if neighbor == dest: 
                    return (costs, actual_costs), previous

            queue.pop()
                    
            if break_outer: 
                break
        
        return (costs, actual_costs), previous 

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
