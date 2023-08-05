
""" 
    ################################################################
    # KAHN'S TOPOLOGICAL SORTING ALGORITHM IMPLEMENTATION [PYTHON] #
    ################################################################

    NOTES 
        * main source: wikipedia.com (modified implementation)
        * does not require other files
		* printable / narrow width 

    API 
        * topological_sort(graph)

""" 
from dsap.graphs.structs.graph import Graph

def topological_sort(graph, copy = True): 

    
    # copy graph to avoid modifying the original
    if copy:
        graph_ = Graph(True)
        graph_.graph = graph.graph.copy()
        graph = graph_

    L = [] 
    V = set(list(graph.vertices()))
    H = set()
    I = {}

    # find nodes S with no incoming edges 
    for edge in graph.edges(): 
        src, dest, _ = edge 
        if dest not in H: 
            H.add(dest) 
        if dest not in I: 
            I[dest] = {}
        I[dest][src] = True

    S = list(V - H) 

    # find sorting 
    while len(S) > 0: 
        # remove a node n from S
        n = S[-1]  
        S.pop()

        # add n to L 
        L.append(n)

        # for each node m with an edge e from n to m 
        vertex_edges = list(graph.vertex_edges(n)) 

        for e in vertex_edges:
            n, m, _ = e 
            # remove edge e from the graph
            del graph.graph[n][m] 
            graph._n_edges -= 1
            del I[m][n]
            # if m has no other incoming edges 
            if len(I[m]) == 0: 
                S.append(m)
    
    return L



if __name__ == "__main__": 
    graph = Graph() 

    graph.add_vertex("A")
    graph.add_vertex("B") 
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E") 
    graph.add_vertex("F")
    graph.add_vertex("G")

    graph.add_edge("B", "A", 1) 
    graph.add_edge("C", "A", 1) 
    graph.add_edge("D", "B", 1) 
    graph.add_edge("E", "B", 1)
    graph.add_edge("E", "C", 1)
    graph.add_edge("F", "D", 1) 
    graph.add_edge("F", "E", 1)
    graph.add_edge("G", "E", 1) 

    print(topological_sort(graph))