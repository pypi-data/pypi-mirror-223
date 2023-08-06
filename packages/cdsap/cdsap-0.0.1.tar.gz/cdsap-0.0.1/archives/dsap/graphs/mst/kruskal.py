""" 
    ########################################################
    # KRUSKAL'S MIN. SPANNING TREE IMPLEMENTATION [PYTHON] #
    ########################################################

    NOTES 
        * main source: programiz.com (modified implementation)
        * does not require other files
		* printable / narrow width 

    API 
        

""" 
from dsap.graphs.structs.graph import Graph 

class KruskalMST: 
    def __init__(self, graph): 
        self.graph = graph

    def weight_fn(self, edge_data): 
        return edge_data 

    def parent(self, Va, x): 
        if type(Va[x]) is int and Va[x] < 0: 
            return x 
        else: 
            p = Va[x]
            while type(Va[p]) is type(x):  
                if type(Va[p]) is int and Va[p] < 0: 
                    break 
                p = Va[p]
            return p 

    def union(self, Va, x, y): 
        m_x = -Va[x]
        m_y = -Va[y] 
        n = m_x + m_y
        m = None 

        if m_x >= m_y: 
            Va[y] = x 
            Va[x] = -n 
        else: 
            Va[x] = y 
            Va[y] = -n


    def run(self):
        graph = self.graph 

        # create for the vertices 
        # (for union-find data structure) 
        Va  = {}
        for vertex in graph.vertices(): 
            Va[vertex] = -1  

        # create heap for sorted edges 
        sorted_edges = []
        for u, v, edge_data in graph.edges():
            weight = self.weight_fn(edge_data) 
            sorted_edges.append((u, v, weight))
        sorted_edges = sorted(sorted_edges, key=lambda x: x[2]) 

        # create mst graph and cost counter
        mst = Graph(False)
        cost = 0

        # loop through edge and check if there is a cycle 
        for edge in sorted_edges: 
            u, v, weight = edge 
            
            p_u = self.parent(Va, u)
            p_v = self.parent(Va, v)
            
            if p_u != p_v: 
                self.union(Va, p_u, p_v)

                if not mst.has_vertex(u):
                    mst.add_vertex(u)
                if not mst.has_vertex(v): 
                    mst.add_vertex(v)

                mst.add_edge(u, v, weight)
                                
                cost += weight 

            else: 
                continue 
            

        return mst, cost