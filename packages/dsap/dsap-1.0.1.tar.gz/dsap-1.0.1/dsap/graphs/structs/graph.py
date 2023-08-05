""" 
    ####################################
    # GRAPH IMPLEMENTATION [PYTHON]    #
    ####################################

    NOTES 
        * does not require other files
		* printable / narrow width 

        * integrations 
            - cycle presence checking (source: baeldung.com)
            - connected / disconnected graph checking

    API
        Properties 
            * graph 
            * directed 
            
        Methods 
            * add_vertex(vertex) 
            * add_edge(src, dest, data) 
            * n_vertices() 
            * n_edges()
            * remove_vertex(vertex)
            * vertices() 
            * edges() 
            * vertex_edges(vertex)
            * has_edges(vertex)
            * is_cyclic_dfs(target, track, visited) 
            * is_cyclic() 
            * is_acyclic() 
            * is_connected_dfs(target, visited) 
            * is_disconnected()  
            * is_connected() 
            * set_data(src, dest, data)  
            * has_vertex(vertex)
            * has_edge(src, dest)

""" 

class Graph: 
    def __init__(self, directed = True): 
        self.graph = {} 
        self.directed = directed 
        self._n_edges = 0

    def n_vertices(self): 
        return len(self.graph)

    def n_edges(self):
        return self._n_edges

    def add_vertex(self, vertex): 
        self.graph[vertex] = {}

    def add_edge(self, src, dest, data):
        # connect source to destination 
        self.graph[src][dest] = data 
        
        # connect back destination to source if 
        # graph is an undirected graph
        if not self.directed: 
            self.graph[dest][src] = data

        self._n_edges += 1

    def remove_vertex(self, vertex): 
        edges = list(self.edges())
        for src, dest, _ in edges: 
            if dest == vertex: 
                del self.graph[src][dest] 
        del self.graph[vertex]

    def remove_edge(self, src, dest): 
        del self.graph[src][dest]

    def vertices(self): 
        vertices = self.graph.keys() 
        for vertex in vertices: 
            yield vertex

    def edges(self): 
        vertices = self.vertices() 
        for vertex in vertices: 
            edges = self.graph[vertex] 
            for edge in edges: 
                yield vertex, edge, edges[edge] 
    
    def vertex_edges(self, vertex): 
        for dest in self.graph[vertex]:
            yield vertex, dest, self.graph[vertex][dest] 

    def has_edges(self, vertex): 
        return len(self.graph[vertex].keys()) > 0
    
    def is_cyclic_dfs(self, target, track, visited): 
        track[target] = True

        neighbors = self.vertex_edges(target)

        for src, dest, _ in neighbors: 
            not_yet_visited = dest not in visited

            if dest in track: 
                return True 
            elif not_yet_visited:
                if self.is_cyclic_dfs(dest, track, visited): 
                    return True
            
        del track[target] 
        visited[target] = True

        return False

    def is_cyclic(self): 
        track = {}
        visited = {} 
        
        for vertex in self.vertices():
            not_yet_visited = vertex not in visited
            if not_yet_visited: 
                if self.is_cyclic_dfs(vertex, track, visited): 
                    return True

        return False

    def is_acyclic(self):
        return not self.is_cyclic() 

    def is_disconnected_dfs(self, target, visited):
        n_visited = 0
        visited[target] = True

        for src, dest, _ in self.vertex_edges(target):
            if dest in visited: 
                continue 
            else: 
                n_visited += self.is_disconnected_dfs(dest, visited)                
        
        return 1 + n_visited   

    def is_disconnected(self): 
        visited = {}
        start = None 

        for vertex in self.vertices(): 
            start = vertex 
            break  

        n_visited = self.is_disconnected_dfs(start, visited) 

        if n_visited != self.n_vertices(): 
            return True 
        else: 
            return False

    def is_connected(self): 
        return not self.is_disconnected() 

    def set_data(self, src, dest, data): 
        self.graph[src][dest] = data 
        if self.directed: 
            self.graph[dest][src] = data

    def get_data(self, src, dest): 
        return self.graph[src][dest]

    def has_vertex(self, vertex): 
        return vertex in self.graph

    def has_edge(self, src, dest): 
        return src in self.graph and dest in self.graph[src]

    def back_edges(self): 
        I = {}

        # find nodes S with no incoming edges 
        for edge in self.edges(): 
            src, dest, _ = edge 
            if dest not in I: 
                I[dest] = {}
            I[dest][src] = True 

        return I
