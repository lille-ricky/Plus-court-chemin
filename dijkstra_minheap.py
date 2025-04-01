class MinHeap:
    def __init__(self):
        self.heap = []
        
    def push(self, item):
        """
        Adds an element to the heap and organizes it 
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
        
    def pop(self):
        """
        Extracts and returns the minimal element
        """
        if not self.heap:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._sift_down(0) 
        return item
    
    def _sift_up(self, index):
        """
        Moves an element up in the heap
        """
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            index = parent 
            parent = (index - 1) // 2
            
    def _sift_down(self, index):
        """
        Moves an element down in the heap
        """
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index 
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left 
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right 
        
        if smallest != index:
            self._swap(index, smallest)
            self._sift_down(smallest)
            
    def _swap(self, i, j):
        """
        Swaps two elements in the heap
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def __len__(self):
        return len(self.heap)

def dijkstra(graph, start):
    # Initialization
    distances = {node: float('inf') for node in graph}
    distances[start] = 0 
    previous_nodes = {node: None for node in graph}
    
    # Priority queue using MinHeap
    heap = MinHeap()
    heap.push((0, start)) 
    
    # To solve the problem of duplicates in the heap
    in_heap = {start}
    
    while len(heap) > 0:
        curr_dist, curr_node = heap.pop()
        in_heap.remove(curr_node)
        
        # If a better path is found, continue
        if curr_dist > distances[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight 
            
            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance 
                previous_nodes[neighbor] = curr_node 
                
                # Add only if not already in the heap
                if neighbor not in in_heap:
                    heap.push((distance, neighbor))
                    in_heap.add(neighbor)
    
    return distances, previous_nodes