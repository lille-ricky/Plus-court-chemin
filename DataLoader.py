import csv
import time
import matplotlib.pyplot as plt
from dijkstra_minheap import dijkstra as dijkstra_minheap
from dijkstra_fibo import dijkstra_fibonacci

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
    
    # Sort stops by arrival time within each trip
    for trip_id in trips:
        trips[trip_id].sort(key=lambda x: x[1])
    
    # Create graph from trips
    for trip_stops in trips.values():
        for i in range(len(trip_stops) - 1):
            current_stop, current_time = trip_stops[i]
            next_stop, next_time = trip_stops[i+1]
            
            # Calculate time difference as edge weight (in minutes for simplicity)
            h1, m1, s1 = map(int, current_time.split(':'))
            h2, m2, s2 = map(int, next_time.split(':'))
            weight_seconds = (h2 * 3600 + m2 * 60 + s2) - (h1 * 3600 + m1 * 60 + s1)
            weight_minutes = weight_seconds / 60  # Convert to minutes for more readable values
            
            # Add to graph (undirected)
            if current_stop not in graph:
                graph[current_stop] = {}
            if next_stop not in graph:
                graph[next_stop] = {}
            
            # Use dictionary to avoid duplicate edges (keep minimum weight)
            if next_stop not in graph[current_stop] or weight_minutes < graph[current_stop][next_stop]:
                graph[current_stop][next_stop] = weight_minutes
            if current_stop not in graph[next_stop] or weight_minutes < graph[next_stop][current_stop]:
                graph[next_stop][current_stop] = weight_minutes
    
    # Convert dictionary format to list format for compatibility with Dijkstra
    for node in graph:
        graph[node] = [(neighbor, weight) for neighbor, weight in graph[node].items()]
    
    return graph

def benchmark_dijkstra(graph, start_node):
    """
    Benchmark Dijkstra's algorithm implementations
    """
    # MinHeap implementation
    start_time = time.time()
    distances_minheap, _ = dijkstra_minheap(graph, start_node)
    minheap_time = time.time() - start_time
    
    # Fibonacci Heap implementation
    start_time = time.time()
    distances_fibonacci, _ = dijkstra_fibonacci(graph, start_node)
    fibonacci_time = time.time() - start_time
    
    return {
        'Temps Tas Binaire': minheap_time,
        'Temps Tas Fibonacci': fibonacci_time,
        'Distances Tas Binaire': len(distances_minheap),
        'Distances Tas Fibonacci': len(distances_fibonacci),
        'Speedup': minheap_time / fibonacci_time if fibonacci_time > 0 else 0
    }

def plot_performance(results):
    """
    Alternative version showing both metrics with better spacing
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Time comparison
    implementations = ['Binary Heap', 'Fibonacci Heap']
    times = [results['Temps Tas Binaire'], results['Temps Tas Fibonacci']]
    ax1.bar(implementations, times, color=['#3498db', '#e74c3c'])
    ax1.set_ylabel('Execution Time (seconds)')
    for i, v in enumerate(times):
        ax1.text(i, v * 1.05, f"{v:.4f}s", ha='center')
    
    # Nodes comparison
    nodes = [results['Distances Tas Binaire'], results['Distances Tas Fibonacci']]
    ax2.bar(implementations, nodes, color=['#3498db', '#e74c3c'])
    ax2.set_ylabel('Nodes Reached')
    for i, v in enumerate(nodes):
        ax2.text(i, v * 1.02, str(v), ha='center')
    
    fig.suptitle('Dijkstra Algorithm Performance Comparison')
    plt.tight_layout()
    plt.savefig('dijkstra_performance_side.png', dpi=300)
    plt.close()

# Main execution
def main():
    file_path = 'gtfs/stop_times.txt'  
    graph = load_stop_times(file_path)
    
    print(f"Graph loaded: {len(graph)} nodes and {sum(len(edges) for edges in graph.values())} edges")
    
    # Select a starting node (first node in the graph)
    start_node = list(graph.keys())[0]
    
    # Benchmark and plot results
    results = benchmark_dijkstra(graph, start_node)
    plot_performance(results)
    
    print("\nRésultats de performance:")
    print(f"Temps d'exécution - Tas Binaire: {results['Temps Tas Binaire']:.6f} secondes")
    print(f"Temps d'exécution - Tas Fibonacci: {results['Temps Tas Fibonacci']:.6f} secondes")
    print(f"Facteur d'accélération: {results['Speedup']:.2f}x")
    print(f"Nombre de nœuds atteints - Tas Binaire: {results['Distances Tas Binaire']}")
    print(f"Nombre de nœuds atteints - Tas Fibonacci: {results['Distances Tas Fibonacci']}")

if __name__ == '__main__':
    main()