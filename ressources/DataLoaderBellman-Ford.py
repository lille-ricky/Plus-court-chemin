import csv
import time
import matplotlib.pyplot as plt
import numpy as np
from dijkstra_minheap import dijkstra as dijkstra_minheap
from dijkstra_fibo import dijkstra_fibonacci

# Ajout de l'implémentation de Bellman-Ford
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

def load_stop_times(file_path):
    """
    Load stop times and create a graph representation
    """
    graph = {}
    trips = {}
    
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip_id = row['trip_id']
            stop_id = row['stop_id']
            arrival_time = row['arrival_time']
            
            # Group stops by trip
            if trip_id not in trips:
                trips[trip_id] = []
            trips[trip_id].append((stop_id, arrival_time))
    
    # Create graph from trips
    for trip_stops in trips.values():
        for i in range(len(trip_stops) - 1):
            current_stop, current_time = trip_stops[i]
            next_stop, next_time = trip_stops[i+1]
            
            # Calculate time difference as edge weight
            h1, m1, s1 = map(int, current_time.split(':'))
            h2, m2, s2 = map(int, next_time.split(':'))
            weight = (h2 * 3600 + m2 * 60 + s2) - (h1 * 3600 + m1 * 60 + s1)
            
            # Undirected graph
            if current_stop not in graph:
                graph[current_stop] = []
            if next_stop not in graph:
                graph[next_stop] = []
            
            graph[current_stop].append((next_stop, weight))
            graph[next_stop].append((current_stop, weight))
    
    return graph

def load_subgraphs(graph, sizes):
    """
    Create subgraphs of different sizes for benchmarking
    """
    subgraphs = {}
    all_vertices = list(graph.keys())
    
    for size in sizes:
        if size > len(all_vertices):
            size = len(all_vertices)
        
        vertices_subset = all_vertices[:size]
        subgraph = {v: [] for v in vertices_subset}
        
        # Include only edges between vertices in the subset
        for v in vertices_subset:
            for u, weight in graph[v]:
                if u in vertices_subset:
                    subgraph[v].append((u, weight))
        
        subgraphs[size] = subgraph
    
    return subgraphs

def benchmark_algorithms(subgraphs):
    """
    Benchmark all three algorithm implementations on different graph sizes
    """
    results = {
        'sizes': [],
        'vertices': [],
        'edges': [],
        'minheap_time': [],
        'fibonacci_time': [],
        'bellman_ford_time': []
    }
    
    for size, graph in subgraphs.items():
        # Count actual vertices and edges
        num_vertices = len(graph)
        num_edges = sum(len(edges) for edges in graph.values()) // 2  # Divide by 2 for undirected graph
        
        # Choose a start node
        start_node = list(graph.keys())[0]
        
        # Benchmark MinHeap Dijkstra
        start_time = time.time()
        distances_minheap, _ = dijkstra_minheap(graph, start_node)
        minheap_time = time.time() - start_time
        
        # Benchmark Fibonacci Heap Dijkstra
        start_time = time.time()
        distances_fibonacci, _ = dijkstra_fibonacci(graph, start_node)
        fibonacci_time = time.time() - start_time
        
        # Benchmark Bellman-Ford
        start_time = time.time()
        distances_bellman, _ = bellman_ford(graph, start_node)
        bellman_time = time.time() - start_time
        
        # Store results
        results['sizes'].append(size)
        results['vertices'].append(num_vertices)
        results['edges'].append(num_edges)
        results['minheap_time'].append(minheap_time)
        results['fibonacci_time'].append(fibonacci_time)
        results['bellman_ford_time'].append(bellman_time)
        
        print(f"Completed benchmark for graph size {size}: {num_vertices} vertices, {num_edges} edges")
    
    return results

def plot_theoretical_vs_empirical(results):
    """
    Plot theoretical complexity bounds versus empirical results
    """
    plt.figure(figsize=(18, 12))
    
    # Get data
    vertices = np.array(results['vertices'])
    edges = np.array(results['edges'])
    
    # Plot 1: Dijkstra MinHeap
    plt.subplot(2, 2, 1)
    theoretical_minheap = edges * np.log(vertices)  # O(E log V)
    # Normalize for comparison
    theoretical_minheap = theoretical_minheap * (max(results['minheap_time']) / max(theoretical_minheap))
    
    plt.plot(results['sizes'], results['minheap_time'], 'b-', marker='o', label='Empirique')
    plt.plot(results['sizes'], theoretical_minheap, 'b--', label='Théorique O(E log V)')
    plt.title('Dijkstra avec Tas Binaire')
    plt.xlabel('Taille du graphe')
    plt.ylabel('Temps (secondes)')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Dijkstra Fibonacci Heap
    plt.subplot(2, 2, 2)
    theoretical_fibonacci = edges + vertices * np.log(vertices)  # O(E + V log V)
    # Normalize for comparison
    theoretical_fibonacci = theoretical_fibonacci * (max(results['fibonacci_time']) / max(theoretical_fibonacci))
    
    plt.plot(results['sizes'], results['fibonacci_time'], 'g-', marker='o', label='Empirique')
    plt.plot(results['sizes'], theoretical_fibonacci, 'g--', label='Théorique O(E + V log V)')
    plt.title('Dijkstra avec Tas de Fibonacci')
    plt.xlabel('Taille du graphe')
    plt.ylabel('Temps (secondes)')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: Bellman-Ford
    plt.subplot(2, 2, 3)
    theoretical_bellman = vertices * edges  # O(V * E)
    # Normalize for comparison
    theoretical_bellman = theoretical_bellman * (max(results['bellman_ford_time']) / max(theoretical_bellman))
    
    plt.plot(results['sizes'], results['bellman_ford_time'], 'r-', marker='o', label='Empirique')
    plt.plot(results['sizes'], theoretical_bellman, 'r--', label='Théorique O(V * E)')
    plt.title('Bellman-Ford')
    plt.xlabel('Taille du graphe')
    plt.ylabel('Temps (secondes)')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: Comparison of all algorithms
    plt.subplot(2, 2, 4)
    plt.plot(results['sizes'], results['minheap_time'], 'b-', marker='o', label='Dijkstra Tas Binaire')
    plt.plot(results['sizes'], results['fibonacci_time'], 'g-', marker='o', label='Dijkstra Tas Fibonacci')
    plt.plot(results['sizes'], results['bellman_ford_time'], 'r-', marker='o', label='Bellman-Ford')
    plt.title('Comparaison des Algorithmes')
    plt.xlabel('Taille du graphe')
    plt.ylabel('Temps (secondes)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('algorithmes_performance_comparaison.png', dpi=300)
    plt.close()

def create_performance_table(results):
    """
    Create a comprehensive comparison table for LaTeX
    """
    latex_table = """
\\begin{table}[htbp]
\\centering
\\caption{Comparaison des performances des algorithmes de plus court chemin}
\\begin{tabular}{|c|c|c|c|c|c|c|}
\\hline
\\textbf{Taille} & \\textbf{Sommets} & \\textbf{Arêtes} & \\textbf{Dijkstra} & \\textbf{Dijkstra} & \\textbf{Bellman-} & \\textbf{Ratio} \\\\
\\textbf{Graphe} & \\textbf{(|V|)} & \\textbf{(|E|)} & \\textbf{Binaire (s)} & \\textbf{Fibonacci (s)} & \\textbf{Ford (s)} & \\textbf{B-F/Fibo} \\\\
\\hline
"""
    
    for i in range(len(results['sizes'])):
        size = results['sizes'][i]
        vertices = results['vertices'][i]
        edges = results['edges'][i]
        minheap = results['minheap_time'][i]
        fibonacci = results['fibonacci_time'][i]
        bellman = results['bellman_ford_time'][i]
        ratio = bellman / fibonacci if fibonacci > 0 else "N/A"
        
        if isinstance(ratio, float):
            ratio_str = f"{ratio:.2f}"
        else:
            ratio_str = ratio
            
        row = f"{size} & {vertices} & {edges} & {minheap:.6f} & {fibonacci:.6f} & {bellman:.6f} & {ratio_str} \\\\\n\\hline\n"
        latex_table += row
    
    latex_table += """\\end{tabular}
\\label{tab:performance_comparison}
\\end{table}
"""
    
    with open('performance_table.tex', 'w') as f:
        f.write(latex_table)
    
    return latex_table

def main():
    # Load data
    file_path = 'gtfs/stop_times.txt'  
    try:
        full_graph = load_stop_times(file_path)
        print(f"Loaded graph with {len(full_graph)} vertices")
        
        # Create subgraphs of increasing sizes for benchmarking
        sizes = [50, 100, 200, 300, 400, 500]
        subgraphs = load_subgraphs(full_graph, sizes)
        
        # Run benchmarks
        results = benchmark_algorithms(subgraphs)
        
        # Generate visualizations
        plot_theoretical_vs_empirical(results)
        
        # Create performance table
        latex_table = create_performance_table(results)
        print("Performance table saved to performance_table.tex")
        
        print("Analyse complète. Résultats sauvegardés dans algorithmes_performance_comparaison.png")
        
    except FileNotFoundError:
        print(f"Erreur: Fichier {file_path} non trouvé. Veuillez vérifier le chemin.")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == '__main__':
    main()