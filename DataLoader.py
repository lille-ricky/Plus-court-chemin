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
        'Distances Tas Fibonacci': len(distances_fibonacci)
    }

def plot_performance(results):
    """
    Create comparative performance visualization
    """
    plt.figure(figsize=(10, 5))
    
    # Time comparison
    plt.subplot(1, 2, 1)
    plt.bar(['Tas binaire', 'Tas Fibonacci'], 
            [results['Temps Tas Binaire'], results['Temps Tas Fibonacci']])
    plt.title('Comparaison du temps d\'execution')
    plt.ylabel('Temps (secondes)')
    
    # Distances comparison
    plt.subplot(1, 2, 2)
    plt.bar(['Tas binaire', 'Tas Fibonacci'], 
            [results['Distances Tas Binaire'], results['Distances Tas Fibonacci']])
    plt.title('Distances Calculés')
    plt.ylabel('Nombre de Distances')
    
    plt.tight_layout()
    plt.savefig('dijkstra_performance.png')
    plt.close()

# Main execution
def main():
    file_path = 'gtfs/stop_times.txt'  # Replace with actual file path
    graph = load_stop_times(file_path)
    
    # Select a starting node (first node in the graph)
    start_node = list(graph.keys())[0]
    
    # Benchmark and plot results
    results = benchmark_dijkstra(graph, start_node)
    plot_performance(results)
    
    print("Resultats de performance:")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()