"""
    ##############################################
    # DOUBLY LINKED-LIST IMPLEMENTATION [PYTHON] #
    ##############################################

    NOTES
		* does not require other files 
        * printable / narrow width

	API		
        DLL_Node 
            Properties
                - value 
                - prev 
                - next 

        DLL 
            Properties 
                - head 
                - tail 
                - count

            Location Operations
                - at(index) 
                - search(value) 
                - search_node(node) 
                - index(value)
                - node_index(node) 
            
            Insertion Operations
                - insert(pos, value) 
                - insert_node(pos, node) 
                - prepend(value) 
                - prepend_node(node) 
                - append(value) 
                - append_node(value) 
                - insert_after(node, value) 
                - insert_node_after(node, new_node) 
                - insert_before(node, value) 
                - insert_node_before(node, new_node) 
                    
            Deletion Operations 
                - delete(pos) 
                - delete_node(node)
                - delete_head() 
                - delete_tail() 
                - delete_after(node) 
                - delete_before(node)
                - remove(value) 

            Utility Functions 
                - predecessor(node) 
                - successor(node)
                - prepredecessor(node)
                - postsucessor(node)
                - size()
                - is_empty()
                - iterate()
"""

class DLL_Node: 
    def __init__(self, value): 
        self.value = value 
        self.prev  = None
        self.next  = None 
         
class DLL: 
    def __init__(self): 
        self.head = None 
        self.tail = None 
        self.count = 0 

    # --- LOCATION OPERATIONS --- #
    
    def at(self, index): 
        """ 
            Returns node at a given index. 
        """
        i = 0 
        index = index % self.count 
        current = self.head 
        while i < index: 
            current = current.next 
            i += 1   
        return current     
    
    def search(self, value): 
        """ 
            Searches for node with a given value. 
        """ 
        current = self.head 
        while current is not None: 
            if current.value == value: 
                return current
            current = current.next 
        return None 
    
    def search_node(self, node):
        """ 
            Explicitly searches for a node. 
        """ 
        current = self.head 
        while current is not None: 
            if current is node: 
                return current 
            current = current.next 
        return None 

    def index(self, value):
        i = 0 
        current = self.head 
        while current is not None: 
            if current.value == value: 
                return i 
            current = current.next 
            i += 1 
        return -1   
        
    def node_index(self, node):
        i = 0 
        current = self.head 
        while current is not None: 
            if current is node: 
                return i 
            current = current.next 
            i += 1 
        return -1 
 
    # --- INSERTION OPERATIONS --- # 

    def insert(self, pos, value): 
        node = DLL_Node(value) 
        self.insert_node(pos, node)

    def insert_node(self, pos, node): 
        # insert at beginning of list 
        if pos == 0: 
            self.prepend_node(node)
        # insert at end of the list 
        elif pos == self.count: 
            self.append_node(node)
        # insert at the middle of the list 
        elif pos > 0 and pos < self.count: 
            # find predecessor and successor
            predecessor = self.at(pos - 1) 
            successor = predecessor.next 
            
            # attach predecessor and successor to node 
            node.next = successor 
            node.prev = predecessor 
            
            # link node to predecessor and successor
            predecessor.next = node 
            successor.prev = node 

            # increase size of list 
            self.count += 1
        # out of bounds 
        else:
            error = f"Out of bounds ({pos})" + \
                    f"when inserting {node.value}"
            raise Exception(error)
        
    def prepend(self, value): 
        node = DLL_Node(value)
        self.prepend_node(node) 

    def prepend_node(self, node): 
        # if list is initially empty 
        if self.head == None: 
            self.head = node 
            self.tail = node 
        else: 
            node.next = self.head 
            self.head.prev = node 
            self.head = node               

        # increase size of list 
        self.count += 1 

    def append(self, value): 
        node = DLL_Node(value) 
        self.append_node(node)

    def append_node(self, node):
        # if list is initially empty 
        if self.head == None: 
            self.head = node 
            self.tail = node 
        else: 
            self.tail.next = node 
            node.prev = self.tail
            self.tail = node 

        # increase size of list 
        self.count += 1

    def insert_after(self, node, value):
        new_node = DLL_Node(value)
        self.insert_node_after(node, new_node)

    def insert_node_after(self, node, new_node): 
        # if node is tail, append 
        if node is self.tail: 
            self.append_node(new_node)
        else: 
            successor = self.successor(node) 

            new_node.prev = node 
            new_node.next = successor 

            node.next = new_node 
            successor.prev = new_node 
            
        # increase size of list 
        self.count += 1 
    
    def insert_before(self, node, value): 
        new_node = DLL_Node(value) 
        self.insert_node_before(node, new_node) 

    def insert_node_before(self, node, new_node):
        # if node is head, prepend 
        if node is self.head: 
            self.prepend_node(new_node)
        else: 
            predecessor = self.predecessor(node)         

            new_node.prev = predecessor 
            new_node.next = node 

            predecessor.next = new_node 
            node.prev = new_node 

        # increase size of list 
        self.count += 1

    # --- DELETION OPERATONS --- # 
    def delete(self, pos):
        # delete at beginning of list 
        if pos == 0: 
            self.delete_head()
        # delete at end of the list 
        elif pos == self.count: 
            self.delete_tail()
        # delete at the middle of the list 
        elif pos > 0 and pos < self.count: 
            self.delete_node(self.at(pos))
        else:
            error = f"Out of bounds ({index})" + \
                    f"when deleting index {node.value}"
            raise Exception(error)


    def delete_node(self, node, predecessor = None): 
        if node is self.head: 
            self.delete_head() 
        elif node is self.tail: 
            self.delete_tail() 
        else: 
            if predecessor is None:
                predecessor = self.predecessor(node) 
            node.next.prev = predecessor 
            predecessor.next = node.next 
            
            # decrease size of list
            self.count -= 1  

    def delete_head(self): 
        # move head pointer
        if self.tail == self.head: 
            self.head = None
            self.tail = None 
        else:
            self.head.next.prev = None
            self.head = self.head.next 

        # decrease size of list 
        self.count -= 1 

    def delete_tail(self): 
        # move tail pointer 
        if self.tail == self.head: 
            self.head = None 
            self.tail = None 
        else: 
            predecessor = self.predecessor(self.tail) 
            predecessor.next = None 
            self.tail = predecessor 

        # decrease size of list 
        self.count -= 1 

    def delete_after(self, node):
        if node is self.tail: 
            raise Exception("Out of bounds when deleting node.") 
        else: 
            node.next.next.prev = node 
            node.next = node.next.next   


    def delete_before(self, node): 
        if node is self.head:  
            raise Exception("Out of bounds when deleting node.") 
        else: 
            prepredecessor = self.prepredecessor(node) 
            prepredecessor.next = node   
            node.prev = prepredecessor

    def remove(self, value): 
        node = self.search(value)
        self.delete_node(node)

    # --- UTILITY FUNCTIONS --- # 
    def predecessor(self, node):
        return node.prev
    
    def successor(self, node): 
        return node.next  

    def prepredecessor(self, node): 
        return node.prev.prev 

    def postsucessor(self, node): 
        return node.next.next 

    def size(self): 
        return self.count

    def is_empty(self): 
        return self.size() == 0
         
    def iterate(self): 
        current = self.head 
        
        if current == None: 
            return

        while current is not None:
            yield current 
            current = current.next  

    def clear(self):
        self.head = None 
        self.tail = None 
        self.count = 0 