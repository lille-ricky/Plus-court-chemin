# -*- coding: utf-8 -*-
"""

@author: enrik pashaj
"""

class FibonacciNode:
    def __init__(self, key, value):
        self.key = key       # Distance (pour la priorité)
        self.value = value   # Sommet du graphe
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.marked = False

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.node_count = 0
        self.nodes = {}  # Pour retrouver les nodes par valeur
    
    def insert(self, key, value):
        new_node = FibonacciNode(key, value)
        self.nodes[value] = new_node
        
        if self.min_node is None:
            self.min_node = new_node
        else:
            self._add_to_root_list(new_node)
            if key < self.min_node.key:
                self.min_node = new_node
        self.node_count += 1
        return new_node
    
    def extract_min(self):
        z = self.min_node
        if z is not None:
            # Ajouter les enfants à la racine
            if z.child is not None:
                children = self._remove_child_nodes(z)
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None
            
            self._remove_from_root_list(z)
            self.nodes.pop(z.value)
            
            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()
            
            self.node_count -= 1
        return (z.key, z.value) if z else (None, None)
    
    def decrease_key(self, value, new_key):
        node = self.nodes.get(value)
        if node is None or new_key > node.key:
            return False
        
        node.key = new_key
        parent = node.parent
        
        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        
        if node.key < self.min_node.key:
            self.min_node = node
        
        return True
    
    def _add_to_root_list(self, node):
        if self.min_node is None:
            return
        
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node
    
    def _remove_from_root_list(self, node):
        node.left.right = node.right
        node.right.left = node.left
    
    def _remove_child_nodes(self, node):
        children = []
        current = node.child
        if current is not None:
            while True:
                children.append(current)
                current = current.right
                if current == node.child:
                    break
        return children
    
    def _consolidate(self):
        degree_table = {}
        nodes = []
        current = self.min_node
        if current is not None:
            while True:
                nodes.append(current)
                current = current.right
                if current == self.min_node:
                    break
        
        for node in nodes:
            degree = node.degree
            while degree in degree_table:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                self._link(other, node)
                degree_table.pop(degree)
                degree += 1
            degree_table[degree] = node
        
        self.min_node = None
        for node in degree_table.values():
            if self.min_node is None:
                self.min_node = node
            else:
                if node.key < self.min_node.key:
                    self.min_node = node
    
    def _link(self, child, parent):
        self._remove_from_root_list(child)
        child.parent = parent
        child.marked = False
        
        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child
        
        parent.degree += 1
    
    def _cut(self, node, parent):
        if parent.child == node:
            if node.right == node:
                parent.child = None
            else:
                parent.child = node.right
        self._remove_from_root_list(node)
        parent.degree -= 1
        self._add_to_root_list(node)
        node.parent = None
        node.marked = False
    
    def _cascading_cut(self, node):
        parent = node.parent
        if parent is not None:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
    
    def is_empty(self):
        return self.min_node is None
    
    
    
def dijkstra_fibonacci(graph, start):
    # Initialisation
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    
    # File de priorité (notre tas de Fibonacci)
    heap = FibonacciHeap()
    heap.insert(0, start)
    
    # Pour garder une référence aux noeuds dans le tas
    in_heap = {start}
    
    while not heap.is_empty():
        current_dist, current_node = heap.extract_min()
        in_heap.remove(current_node)
        
        # Si on a déjà trouvé un meilleur chemin, on ignore
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            
            # Si on trouve un chemin plus court
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                
                if neighbor in in_heap:
                    heap.decrease_key(neighbor, distance)
                else:
                    heap.insert(distance, neighbor)
                    in_heap.add(neighbor)
    
    return distances, previous_nodes

