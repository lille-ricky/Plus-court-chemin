def bellman_ford(graph, source):
    """
    Implements the Bellman-Ford algorithm to find shortest paths from a source vertex.
    
    Args:
    graph (dict): A dictionary representing the graph where keys are vertices 
                  and values are lists of (destination, weight) tuples
    source (int/str): The source vertex from which to calculate shortest paths
    
    Returns:
    tuple: (distances, predecessors) 
           - distances: dictionary of shortest distances from source to each vertex
           - predecessors: dictionary of predecessor vertices in the shortest path
    """
    # Initialize distances and predecessors
    vertices = list(graph.keys())
    distances = {v: float('inf') for v in vertices}
    predecessors = {v: None for v in vertices}
    
    # Distance to source is 0
    distances[source] = 0
    
    # Relax edges |V| - 1 times
    for _ in range(len(vertices) - 1):
        for u in graph:
            for v, weight in graph[u]:
                # If we can improve the distance to v through u
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
    
    # Check for negative-weight cycles
    for u in graph:
        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                raise ValueError("Graph contains a negative-weight cycle")
    
    return distances, predecessors


