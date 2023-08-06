
def make_tree(graph, root = 'auto'):    
    if root == 'auto': 
        for vertex in graph.all_vertices(): 
            root = vertex 
            break   
    
    tree = {}
    visited = {}

    visited[root] = True

    tree[root] = {
        "weight" : 0, 
        "children" : {}
    } 

    make_tree_on_node(graph, root, tree[root], visited) 

    print(tree)

def make_tree_on_node(graph, node, base, visited):  
    for u, v, edge_data in graph.vertex_edges(node): 
        
        if v in visited: 
            continue

        visited[v] = True
        base["children"][v] = { 
            "data" : edge_data, 
            "children" : {}  
        }
        make_tree_on_node(graph, v, base["children"][v], visited)
