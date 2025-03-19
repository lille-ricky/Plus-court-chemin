def bellman_ford(graph, source):
    """
    Bellman-Ford algorithm

    """
    
    dist = {}
    precedent = {}
    
    for v in graph :
        dist[v] = float('inf')
        precedent[v] = None 
        
    dist[source] = 0 
    
    for i in range(1, len(graph)):
        for u in graph:
            for v in graph[u]:
                poids = graph[u][v]
                if dist[u] + poids < dist[v] :
                    dist[v] = dist[u] + poids 
                    precedent[v] = u 
                    
    return precedent 
