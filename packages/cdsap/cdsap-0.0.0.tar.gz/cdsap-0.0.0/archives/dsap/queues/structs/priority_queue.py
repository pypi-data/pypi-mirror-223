""" 
    ##############################################
    # DOUBLE-ENDED PRIORITY QUEUE IMPLEMENTATION #
    ##############################################

    NOTES 
		* min-max heap based 
		* requires min-max heap (same project)
		* printable / narrow width

	API 
		PriorityQueue 
			- comparator() 
            - min() 
            - max() 
            - front() 
            - back() 
            - enqueue(self, key, priority, data = None) 
            - dequeue_front(self) 
            - dequeue_back(self)
            - size() 
            - is_empty()
            - display() 

""" 
from dsap.heaps.structs.kmmh import KMMH

class PriorityQueue: 
    def __init__(self, type_ = "min"): 
        self.items = KMMH()  
        self.type = type_

        def comparator(a, b):                 
            if self.type == "min":
                return self.comparator(a, b)
            else: 
                return not self.comparator(a, b)

        self.items.comparator = comparator

    def comparator(self, a, b): 
        if a.value == b.value: 
            return a.key < b.key 
        else: 
            return a.value < b.value

    def min(self):
        return self.items.min()
    
    def max(self):
        return self.items.max() 

    def front(self): 
        if self.type == "min": 
            return self.min()
        elif self.type == "max": 
            return self.max()

    def back(self): 
        if self.type == "min": 
            return self.max()
        elif self.type == "max": 
            return self.min()

    def enqueue(self, key, priority, data = None): 
        return self.items.insert(key, priority, data)

    def dequeue_front(self):
        return self.items.pop_min()

    def dequeue_back(self): 
        return self.items.pop_max()

    def size(self): 
        return self.items.size()

    def is_empty(self): 
        return self.size() == 0

    def display(self): 
        return self.items.display()

    def clear(self): 
        self.items = KMMH() 