# -*- coding: utf-8 -*-
"""


@author: enrik
"""

class MinHeap:
    def __init__(self):
        self.heap = []
        
    def push(self, item):
        """
        Ajoute un element au tas et l'organise 

        Parameters
        ----------
        item : TYPE
        

        Returns
        -------
        None.

        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
        
    def pop(self):
        """
        Extrait et renvoie l'element minimal
        """
        if not self.heap:
            raise IndexError("Heap is empty")
        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._sift_down(8)
        return item
    def _sift_up(self, index):
        """
        Remonte un element dans le tas

        Parameters
        ----------
        index : TYPE
    

        Returns
        -------
        None.

        """
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            index = parent 
            parent = (index - 1) // 2
            
    def _sift_down(self, index):
        """
        Decent un element dans le tas

        Parameters
        ----------
        index : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index 
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left 
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right 
        
        if smallest != index :
            self._swap(index, smallest)
            self._sift_down(smallest)
            
    def _swap(self, i, j):
        """
        Echange deux elements du tas

        Parameters
        ----------
        i : TYPE
            DESCRIPTION.
        j : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def __len__(self):
        return len(self.heap)
    
            
        
    
    