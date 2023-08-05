""" 
    ##################################################################
    # FLOYD-WARSHALL SHORTEST PATH ALGORITHM IMPLEMENTATION [PYTHON] #
    ##################################################################
    NOTES 
        * main source: baeldung.com (modified implementation)
		* printable / narrow width 

        * source: https://stackoverflow.com/a/19814318
    API 
        * weight_fn(edge_data) 
        * init_matrix(m, n, d) 
        * floyd_warshall(graph) 
        * print_results(res) 
        * find_indexed_path(res, a, b) 
        * reverse_indices(VM) 
        * vertex_path(path, ri) 
        * find_path_by_index(res, i, j, path) 
        * find_path(res, a, b) 
        * get_all_paths(res)
 
""" 

INFINITY = float('INF')

class FloydWarshallPF: 
    def __init__(self, graph): 
        self.graph = graph

    def weight_fn(self, edge_data): 
        return edge_data

    def init_matrix(self, m, n, d): 
        M = [] 
        for i in range(m): 
            M.append([d] * n) 
        return M

    def run(self):
        graph = self.graph

        V = graph.n_vertices() 

        M = self.init_matrix(V, V, None)
        VM = {} 

        i = 0 
        for a in graph.vertices(): 
            VM[a] = i

            j = 0  
            for b in graph.vertices(): 
                if a in graph.graph and b in graph.graph[a]: 
                    # print(i, j, weight_fn(graph.graph[a][b]), "<-")
                    M[i][j] = self.weight_fn(graph.graph[a][b])
                else:
                    # print(i, j)
                    M[i][j] = INFINITY 
                j += 1         
            i += 1


        dist  = self.init_matrix(V, V, None)
        next_ = self.init_matrix(V, V, None)

        for v in range(V): 
            dist[v][v] = 0

        for u in range(V):
            for v in range(V): 
                dist[u][v] = self.weight_fn(M[u][v])
                if M[u][v] < INFINITY:
                    next_[u][v] = u  

        for k in range(V): 
            for i in range(V): 
                for j in range(V): 
                    if dist[i][k] + dist[k][j] < dist[i][j]: 
                        dist[i][j] = dist[i][k] + dist[k][j] 
                        next_[i][j] = next_[k][j]  

        return dist, next_, VM

    def print_results(self, res):
        dist, next_, VM = res 
        V = len(dist)
        for u in range(V): 
            print(dist[u])   
        print(next_)

    def find_indexed_path(self, res, a, b): 
        dist, next_, VM = res 

        path = self.find_path_by_index(res, VM[a], VM[b], [])
    
        if path is None: 
            return None

        return [VM[a]] + path  

    def reverse_indices(self, VM): 
        ri = {} 
        for vertex in VM: 
            ri[VM[vertex]] = vertex
        return ri

    def vertex_path(self, path, ri): 
        path_ = [] 
        for index in path:
            path_.append(ri[index]) 
        return path_

    def find_path_by_index(self, res, i, j, path = []): 
        dist, next_, VM = res 

        if i == j:
            return path[::-1]
        elif next_[i][j] is None: 
            return None 
        else: 
            path.append(j)
            return self.find_path_by_index(res, i, next_[i][j], path)

    def find_path(self, res, a, b): 
        path = self.find_indexed_path(res, a, b)

        if path is None: 
            return None

        ri = self.reverse_indices(res[2])
        vp = self.vertex_path(path, ri)      

        return vp

    def get_all_paths(self, res): 
        paths = {} 
        for a in res[2]: 
            paths[a] = {} 
            for b in res[2]: 
                paths[a][b] = self.find_path(res, a, b) 
        return paths

    def find_cost(self, res, src, dest): 
        return res[0][res[2]["A"]][res[2]["F"]]