""" 
    #####################################
    # DOUBLE-ENDED QUEUE IMPLEMENTATION #
    ##################################### 

    NOTES 
		* doubly linked-list based 
		* does not require other files
		* printable / narrow width

	API 
		Dequeue 
			- front()
			- back() 
			- enqueue_front(item) 
			- enqueue_back(item)
            - dequeue_front() 
            - dequeue_back() 
            - size() 
            - is_empty()

""" 
from dsap.linked_lists.structs.dll import DLL

class Deque: 
    def __init__(self): 
        self.items = DLL()  

    def front(self): 
        return self.items.head 

    def back(self): 
        return self.items.tail

    def enqueue_front(self, item): 
        self.items.prepend(item) 

    def enqueue_back(self, item): 
        self.items.append(item) 

    def dequeue_front(self): 
        front = self.front() 
        self.items.delete_head() 
        return front 

    def dequeue_back(self): 
        back = self.back() 
        self.items.delete_tail() 
        return back     

    def size(self): 
        return self.items.size()

    def is_empty(self): 
        return self.size() == 0

    def clear(self): 
        self.items = DLL()