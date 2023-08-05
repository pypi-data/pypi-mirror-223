from dsap.graphs.structs.graph import Graph
from dsap.graphs.sorting.topological_sorting import topological_sort

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