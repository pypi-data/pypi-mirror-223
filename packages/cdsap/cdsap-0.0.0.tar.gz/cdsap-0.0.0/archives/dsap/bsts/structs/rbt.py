""" 
    ##########################################
    # RED-BLACK TREE IMPLEMENTATION [PYTHON] #
    ##########################################

    NOTES 
        * main source: programiz.com (modified implementation)
        * does not require other files
		* printable / narrow width 

        * integrations 
            - order statistics (for log(n) indexing) 
            - threaded nodes (for range queries)
            - range queries (index, key, interval)

    API 
        RBT_Node 
            Properties 
                - key 
                - value 
                - parent 
                - left 
                - right 
                - color 
        
        RBT 
            Properties 
                - TNULL 
                - root 
                - count 
            
            Utility Methods 
                - at(index)
                - index(key)

                - size() 
                - is_empty()s
                
                - find(key, root)
                - find_min(root)  
                - find_max(root) 
                
                - get_n_desc(root)
                - update_n_desc(root)

                - transplant(u, v)
                - rebalance_insert(k)
                - rebalance_delete(k)

                - display() 
                - display_node(root, indent, orient) 
                
                - prev(root)
                - next(root)

                - iterate()
                - keys()
                - values()
                
                - key_prev(key)
                - prev(node)
                - key_next(next)
                - next(node) 

                - update_n_desc()
                
            Rotation Methods
                - left_rotate(x) 
                - right_rotate(x)
                - left_right_rotate(A) 
                - right_left_rotate(A) 
            
            Threaded Binary Tree Methods 
                - set_prev(node, prev)
                - set_next(node, next)
            
            Main Operations 
                - insert(key, value) 
                - insert_node(root, node, parent) 
                - delete(key) 
                - delete_node(root, key)
                - clear()
                - update(key, value)
                
""" 


class RBT_Node():
    def __init__(self, key, value):
        self.key = key 
        self.value = value

        self.n_desc = 1

        self.parent = None

        self.left = None
        self.right = None
        
        self.color = 1

        self.prev = None
        self.next = None
    
class RBT():
    def __init__(self):
        self.TNULL = RBT_Node(None, None)
        self.TNULL.color = 0
        self.TNULL.left = self.TNULL
        self.TNULL.right = self.TNULL
        self.TNULL.n_desc = 0
        self.root = self.TNULL
        self.count = 0

    #
    # UTILITY METHODS
    #

    def comparator(self, a, b): 
        return a.key < b.key 

    def equals(self, a, b): 
        return a.key == b.key

    def at(self, index): 
        current = self.root 
        lo = 0
        hi = self.size() - 1

        while current.n_desc > 1: 
            if current.left: 
                mid = lo + current.left.n_desc
            elif current.right: 
                mid = lo
            
            left = (lo, mid)
            right = (mid + 1, hi) 


            if index == mid: 
                return current 

            elif index >= left[0] and index <= left[1]: 
                hi = mid - 1
                current = current.left

            elif index >= right[0] and index <= right[1]:
                lo = mid + 1
                current = current.right
 
        return current 

    
    def index(self, key): 
        current = self.root 
        lo = 0
        hi = self.size() - 1

        key_node = RBT_Node(key, None)

        while current is not self.TNULL: 
            if current.left: 
                mid = lo + current.left.n_desc
            elif current.right: 
                mid = lo
            
            left = (lo, mid)
            right = (mid + 1, hi) 

            if current.n_desc == 1 and key == current.key: 
                return lo

            elif self.equals(key_node, current): 
                return mid 
            
            elif self.comparator(key_node, current): 
                hi = mid - 1
                current = current.left

            elif not self.comparator(key_node, current):
                lo = mid + 1
                current = current.right
 
        return -1 

    def node_range(self, node_a, node_b): 
        current = node_a

        direction = 1
        if not self.comparator(node_a, node_b): 
            direction = -1

        while current is not None: 
            yield current
            if current is node_b:
                return 
            
            if direction == 1: 
                current = current.next 
            elif direction == -1: 
                current = current.prev
            else: 
                raise Exception("Unknown direction.")

    def size(self): 
        return self.count 

    def is_empty(self): 
        return self.size() == 0

    def find(self, key, root = None): 
        if root is None: 
            current = self.root 
        else: 
            current = root 

        key_node = RBT_Node(key, None)

        while current is not self.TNULL: 
            if self.equals(key_node, current): 
                return current
            elif self.comparator(key_node, current):
                current = current.left
            elif not self.comparator(key_node, current): 
                current = current.right
             
        return None

    def find_min(self, root): 
        if root is self.TNULL: 
            return self.TNULL 

        if root.left is self.TNULL and root.right is self.TNULL: 
            return root 
        elif root.left is self.TNULL and root.right is not self.TNULL: 
            return root 

        return self.find_min(root.left)

    def find_max(self, root): 
        if root is self.TNULL: 
            return self.TNULL 

        if root.left is self.TNULL and root.right is self.TNULL: 
            return root 
        elif root.left is not self.TNULL and root.right is self.TNULL: 
            return root 

        return self.find_max(root.right)

    def get_n_desc(self, root): 
        if root is None: 
            return 0 
        return root.n_desc 
      
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def rebalance_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)

            
            if k == self.root:
                break
        self.root.color = 0

    
    def rebalance_delete(self, x):
        while x != self.root and x.color == 0:

            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root


        x.color = 0

    def display(self): 
        self.display_node(self.root, 0, "root")

    def display_node(self, root, indent, orient):
        if root is self.TNULL:
            return 
        left = \
            root.left.key if root.left is not self.TNULL else 'TNULL'
        right = \
            root.right.key if root.right is not self.TNULL else 'TNULL'
        
        print(
            "    " * indent + \
            f"{orient} : {root.key} -> " +
            f"c: {root.color}, " + 
            f"v: {root.value}, " +
            f"pt: {root.parent.key if root.parent else None}, " + 
            f"nd: {root.n_desc}, " + 
            f"l: {left}, " + 
            f"r: {right}, " + 
            f"p: {root.prev.key if root.prev else '[START : None]'}, " +
            f"n: {root.next.key if root.next else '[END: None]'}" 
        )
        
        self.display_node(root.left, indent + 1, "left")
        self.display_node(root.right, indent + 1, "right")
    
    def iterate(self): 
        current = self.find_min(self.root) 
        while current is not None:
            yield current
            current = current.next
        return None

    def keys(self): 
        for item in self.iterate(): 
            yield item.key

    def values(self): 
        for item in self.iterate(): 
            yield item.value 

    def key_prev(self, key): 
        node = self.find(key)
        return self.prev(node)

    def prev(self, node):   

        if node.left is not self.TNULL:  
            return self.find_max(node.left)

        if node.parent is None: 
            return None

        if node.left is self.TNULL: 

            if node.parent.right is node: 
                return node.parent   
            else: 
                current = node.parent
                while True and current.parent is not None: 
                    if current.parent.right is current: 
                        break
                    current = current.parent
                    if current is self.root: 
                        return self.TNULL  
                return current.parent 

        return self.TNULL 

    def key_next(self, key): 
        node = self.find(key)
        return self.next(node)

    def next(self, node): 

        if node.right is not self.TNULL:  
            return self.find_min(node.right)

        if node.parent is None:
            return None

        if node.right is self.TNULL: 
            if node.parent.left is node: 
                return node.parent   
            else: 
                current = node.parent 
                while True and current.parent is not None: 
                    if current.parent.left is current: 
                        break
                    current = current.parent
                    if current is self.root: 
                        return None 
                return current.parent 

        return None

    def update_n_desc(self, root):
        current = root 
        while current is not None: 
            current.n_desc = 1 + self.get_n_desc(current.left) + \
                                 self.get_n_desc(current.right)
            current = current.parent 

    #
    # RANGE FUNCTIONS
    # 
    def key_range(self, key_a, key_b): 
        kn_a = self.find(key_a) 
        kn_b = self.find(key_b) 
        yield from self.node_range(kn_a, kn_b)

    def index_range(self, idx_a, idx_b): 
        kn_a = self.at(idx_a) 
        kn_b = self.at(idx_b)
        yield from self.node_range(kn_a, kn_b)

    def search_left_bound(self, value): 
        key_node = RBT_Node(value, None)
        current = self.root 

        while current is not None: 
            if self.equals(key_node, current): 
                return current 
            elif current.left is self.TNULL and current.right is self.TNULL: 
                if self.comparator(key_node, current): 
                    return current.prev 
                else: 
                    return current     
            elif self.comparator(key_node, current): 
                if current.left is self.TNULL: 
                    return current.prev 
                current = current.left
            elif not self.comparator(key_node, current):
                if current.right is self.TNULL: 
                    return current 
                current = current.right

    def search_right_bound(self, value): 
        key_node = RBT_Node(value, None)
        current = self.root 
        prev = None

        while current is not None: 
            if self.equals(key_node, current): 
                return current 
            elif current.left is self.TNULL and current.right is self.TNULL: 
                if self.comparator(key_node, current): 
                    return current 
                else: 
                    return current.next     
            elif self.comparator(key_node, current): 
                if current.left is self.TNULL: 
                    return current 
                current = current.left
            elif not self.comparator(key_node, current):
                if current.right is self.TNULL: 
                    return current.next
                current = current.right

        
    def interval_nodes(self, a, b): 
        kn_a = RBT_Node(a, None) 
        kn_b = RBT_Node(b, None)

        if self.comparator(kn_a, kn_b): 
            x = self.search_left_bound(a)
            y = self.search_right_bound(b) 
            return x, y 
        elif not self.comparator(kn_a, kn_b): 
            x = self.search_right_bound(a, True) 
            y = self.search_left_bound(b, True)
            return x, y
       
        return a_node, b_node 

    def interval_range(self, a, b): 
        node_a, node_b = self.interval_nodes(a, b) 
        yield from self.node_range(node_a, node_b)
   
    #
    # ROTATION METHODS
    #

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

        x.n_desc = \
            1 + self.get_n_desc(x.left) + self.get_n_desc(x.right) 
        y.n_desc = \
            1 + self.get_n_desc(y.left) + self.get_n_desc(y.right)

        return y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

        x.n_desc = \
            1 + self.get_n_desc(x.left) + self.get_n_desc(x.right) 
        y.n_desc = \
            1 + self.get_n_desc(y.left) + self.get_n_desc(y.right)

        return y

    #
    # THREADED BINARY TREE METHODS 
    # 
    
    def set_prev(self, node, prev): 
        node.prev = prev 
        if prev:
            prev.next = node 

    def set_next(self, node, next_): 
        node.next = next_ 
        if next_:
            next_.prev = node 

    #
    # MAIN OPERATIONS
    # 

    def insert(self, key, value):
        node = RBT_Node(key, value)
        
        node.parent = None

        node.left = self.TNULL
        node.right = self.TNULL

        node.prev = None 
        node.next = None

        node.color = 1

        self.insert_node(node)
        self.count += 1


    def insert_node(self, node): 
        y = None
        x = self.root

        direction = None
        parent = None

        if self.root == None: 
            self.root = node 
            return

        while x != self.TNULL:
            y = x
            if self.comparator(node, x):
                parent = x 
                x = x.left
                direction = -1
            else:
                parent = x
                x = x.right
                direction = 1

        node.parent = y

        if direction == -1: 
            self.set_prev(node, parent.prev) 
            self.set_next(node, parent)
        elif direction == 1: 
            self.set_next(node, parent.next)
            self.set_prev(node, parent) 

        if y == None:
            self.root = node
        elif self.comparator(node, y):
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return node

        if node.parent.parent == None:
            return node

        self.rebalance_insert(node)
        self.update_n_desc(node)

        return node
        

    def delete(self, key): 
        self.delete_key(self.root, key)
        self.count -= 1

    def delete_key(self, node, key):
        z = self.TNULL

        key_node = RBT_Node(key, None)

        while node is not self.TNULL:
            if self.equals(key_node, node):
                z = node
                break            
            elif self.comparator(key_node, node):
                node = node.left
            elif not self.comparator(key_node, node):
                node = node.right

        if z == self.TNULL:
            print(f"{key} is not in the tree")
            return

        return self.delete_node(z)

     
    def delete_node(self, z):
        y = z
        y_original_color = y.color
        p = z.parent 
        x = None 
        
        if z.left is not self.TNULL and z.right is self.TNULL:
            x = z.left
            self.transplant(z, x)

            if p: 
                a = z.prev 
                if p.left is z: 
                    if a: 
                        self.set_next(a, p) 
                else: 
                    if a: 
                        self.set_next(a, z.next) 
          
        elif z.right is not self.TNULL and z.right is self.TNULL:
            x = z.right
            self.transplant(z, x)

            if p: 
                a = z.next 
                if p.left is z: 
                    if a: 
                        self.set_prev(a, z.prev) 
                else: 
                    if a: 
                        self.set_prev(a, p)

        elif z.left is self.TNULL and z.right is self.TNULL: 
            x = p 
            
            if p is None: 
                self.root = self.TNULL 
                return self.TNULL
            else: 
                if p.left is z: 
                    self.set_prev(p, z.prev)
                    p.left = self.TNULL 
                elif p.right is z: 
                    self.set_next(p, z.next)
                    p.right = self.TNULL 

        else:
            y = self.find_min(z.right)
            y_original_color = y.color
            
            x = y.right

            a = z.prev 
            b = y.next 

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, x)
                
                h = y.next
                self.set_prev(h, z.prev)

                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)

            if z.left: 
                z.left.parent = y
                if a: 
                    self.set_next(a, y)
                if b:
                    self.set_prev(b, y)

            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if y_original_color == 0 and x is not self.TNULL:
            self.rebalance_delete(x)

        self.update_n_desc(z)
 
    def clear(self): 
        self.root = self.TNULL 
        self.count = 0  

    def update(self, key, value): 
        if self.find(key) is None:
            raise Exception(f"{key} is not in tree.")
        self.delete(key)
        self.insert(key, value)
