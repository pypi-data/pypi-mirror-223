""" 
    ##############################################
    # KEYED MIN-MAX HEAP IMPLEMENTATION [PYTHON] #
    ############################################## 
    
    NOTES 
        * array based 
        * source: wikipedia.org (modified implementation)
		* does not require other files
		* printable / narrow width

    API 
        KBH_Item 
            Properties 
                - key 
                - value 
                - data 

        KBH 
            Properties 
                - items 
                - type 
                - key_no 
                - key_map
            
            Utility Methods 
                - comparator(a, b) 
                - keyfy(items) 
                - swap_key_map(i, j)
                - parent(i)
                - left_child(i) 
                - right_child(i) 
                - smallest_child_or_grandchild(h, i) 
                - largest_child_or_grandchild(h, i) 
                - push_down(h, i) 
                - push_down_min(h, i) 
                - push_down_max(h, i) 
                - push_down_iter(h, m) 
                - push_up(h, i) 
                - push_up_min(h, i) 
                - push_up_max(h, i) 
                - push_up_min_iter(h, i) 
                - push_up_max_iter(h, i)
                - update_a(key, value)
                - update_b(key, value)
                - display()

            Main Operations
                - build_heap(h, keyfy)
                - insert(key, value, data)
                - pop_min()  
                - pop_max()
                - delete(key)
                - clear()

            Accessors / Mutators  
                - update(key, new_value)
                - items()
                - keys()    
                - values() 
                - min()
                - max()
                - min_value()
                - max_value() 
                - min_key() 
                - max_key() 
                - size() 
                - is_empty()
                - get_data(key) 
                - set_data(key, data) 
                - get_value(key) 
                - set_value(key, value) 
                - get_item(key) 
                - set_item(key, item) 
                - has_key(key)
                
    
""" 
import math

class KMMH_Item: 
    def __init__(self, key, value, data = None): 
        self.key = key 
        self.value = value 
        self.data = data 

class KMMH: 
    def __init__(self): 
        self.items = [] 
        self.key_no = 0  
        self.key_map = {}

    #
    # GENERAL OPERATIONS
    #  

    def comparator(self, a, b):
        if a.value == b.value: 
            return a.key < b.key 
        else: 
            return a.value < b.value
      
    def keyfy(self, items): 
        if type(items) is list: 
            for i in range(len(items)): 
                items[i] = KMMH_Item(self.key_no, items[i])
                self.key_map[items[i].key] = i
                self.key_no += 1 
            return items
        elif type(items) is dict: 
            i = 0
            new_items = []
            for key in items: 
                value = items[key]
                new_items.append(KMMH_Item(key, value))
                self.key_map[key] = i
                self.key_no += 1 
                i += 1
            return new_items

    def swap_key_map(self, i, j): 
        arr = self.items
        self.key_map[arr[i].key] = j
        self.key_map[arr[j].key] = i

    def level(self, i): 
        return int(math.log2(i + 1)) 

    def parent(self, i): 
        return (i - 1) // 2 

    def left_child(self, i): 
        return 2 * i + 1 
    
    def right_child(self, i): 
        return 2 * i + 2

    def smallest_child_or_grandchild(self, h,  i):
        n = len(h)

        # indices of the children and grandchildren of i
        lc = self.left_child(i)
        rc = self.right_child(i)

        indices = [
            lc, 
            rc,
            self.left_child(lc), 
            self.right_child(lc), 
            self.left_child(rc), 
            self.right_child(rc)
        ] 

        # get the index of the smallest children or grandchildren
        mv_ = KMMH_Item(None, float('inf'))
        m = -1

        for index in indices: 
            if index >= n: 
                break 
            if h[index].value < mv_.value:
                mv_ = h[index]
                m = index

        return m

    def largest_child_or_grandchild(self, h, i):
        n = len(h) 

        # indices of the children and grandchildren of i
        lc = self.left_child(i)
        rc = self.right_child(i)

        indices = [
            lc, 
            rc,
            self.left_child(lc), 
            self.right_child(lc), 
            self.left_child(rc), 
            self.right_child(rc)
        ] 

        # get the index of the smallest children or grandchildren
        mv_ = KMMH_Item(None, float('-inf'))
        m = -1

        for index in indices: 
            if index >= n: 
                break 
            if h[index].value > mv_.value: 
                mv_ = h[index]
                m = index 

        return m

    
    def push_down(self, h, i): 
        if self.level(i) % 2 == 0: 
            self.push_down_min(h, i)
        else:   
            self.push_down_max(h, i)

    def push_down_min(self, h, i):
        n = len(h)
        if 2 * i + 1 < n: 
            m = self.smallest_child_or_grandchild(h, i)

            # if m is a grandchild of i 
            if m > 2 * i + 2: 
                if self.comparator(h[m], h[i]): 
                    self.swap_key_map(m, i) 
                    h[m], h[i] = h[i], h[m]

                    pm = self.parent(m)
                    if not self.comparator(h[m], h[pm]): 
                        self.swap_key_map(m, pm) 
                        h[m], h[pm] = h[pm], h[m] 
                        
                    self.push_down(h, m)
            
            elif self.comparator(h[m], h[i]): 
                self.swap_key_map(m, i) 
                h[m], h[i] = h[i], h[m]

    def push_down_max(self, h, i): 
        n = len(h)
        if 2 * i + 1 < n: 
            m = self.largest_child_or_grandchild(h, i)
    
            # if m is a grandchild of i 
            if m > 2 * i + 2: 
                if not self.comparator(h[m], h[i]): 
                    self.swap_key_map(m, i) 
                    h[m], h[i] = h[i], h[m]

                    pm = self.parent(m)
                    if self.comparator(h[m], h[pm]): 
                        self.swap_key_map(m, pm)
                        h[m], h[pm] = h[pm], h[m]

                    self.push_down(h, m)
            
            elif not self.comparator(h[m], h[i]): 
                self.swap_key_map(m, i) 
                h[m], h[i] = h[i], h[m]

    def push_down_iter(self, h, m): 
        n = len(h)
        while 2 * m + 1 < n: 
            i = m
            if self.level(i) % 2 == 0: 
                m = self.smallest_child_or_grandchild(h, i)
                
                if self.comparator(h[m], h[i]): 
                    self.swap_key_map(m, i) 
                    h[m], h[i] = h[i], h[m] 
                    
                    if m > 2 * i + 2: 
                        pm = self.parent(m)
                        if not self.comparator(h[m], h[pm]): 
                            self.swap_key_map(m, pm) 
                            h[m], h[pm] = h[pm], h[m]
                        else: 
                            break 
                    else: 
                        break 

            else: 
                m = self.largest_child_or_grandchild(h, i)
                
                if not self.comparator(h[m], [i]): 
                    self.swap_key_map(m, i) 
                    h[m], h[i] = h[i], h[m] 
                    
                    if m > 2 * i + 2: 
                        pm = self.parent(m)
                        if self.comparator(h[m], h[pm]): 
                            self.swap_key_map(m, pm) 
                            h[m], h[pm] = h[pm], h[m]
                        else: 
                            break 
                    else: 
                        break 

    def push_up(self, h, i): 
        if i != 0: 
            pi = self.parent(i) 
            if self.level(i) % 2 == 0:
                if not self.comparator(h[i], h[pi]): 
                    self.swap_key_map(i, pi)
                    h[i], h[pi] = h[pi], h[i]
                    self.push_up_max(h, pi) 
                else: 
                    self.push_up_min(h, i) 
            else: 
                if self.comparator(h[i], h[pi]):
                    self.swap_key_map(i, pi)
                    h[i], h[pi] = h[pi], h[i] 
                    self.push_up_min(h, pi) 
                else: 
                    self.push_up_max(h, i) 

    def push_up_min(self, h, i): 
        gpi = self.parent(self.parent(i))
   
        if i >= 3 and self.comparator(h[i], h[gpi]): 
            self.swap_key_map(i, gpi) 
            h[i], h[gpi] = h[gpi], h[i] 
            self.push_up_min(h, gpi) 
        
    def push_up_max(self, h, i): 
        gpi = self.parent(self.parent(i))
        if i >= 3 and not self.comparator(h[i], h[gpi]): 
            self.swap_key_map(i, gpi) 
            h[i], h[gpi] = h[gpi], h[i] 
            self.push_up_max(h, gpi)

    def push_up_min_iter(self, h, i): 
        gpi = self.parent(self.parent(i))
        while i > 0 and self.comparator(h[i], h[gpi]): 
            self.swap_key_map(i, gpi)
            h[i], h[gpi] = h[gpi], h[i]

            i = gpi 
            gpi = self.parent(self.parent(i)) 

    def push_up_max_iter(self, h, i): 
        gpi = self.parent(self.parent(i))
        while i > 0 and not self.comparator(h[i], h[gpi]): 
            self.swap_key_map(i, gpi)
            h[i], h[gpi] = h[gpi], h[i]

            i = gpi 
            gpi = self.parent(self.parent(i))

    def display(self): 
        text = [] 
        for item in self.items: 
            text.append(f"(k: {item.key}, v: {item.value}, " + \
                        f"d: {item.data})")
        print(", ".join(text))

    # 
    # MAIN OPERATIONS
    # 

    def build_heap(self, h, keyfy = True): 
        if keyfy: 
            h = self.keyfy(h)
        
        self.items = h

        n = len(h)
        for i in range(n // 2, -1, -1): 
            self.push_down(h, i)
        
        return h 
         
    def insert(self, key, value, data = None): 
        item = KMMH_Item(key, value, data)

        arr = self.items
        arr.append(item)
        i = len(arr) - 1 
        self.key_map[key] = i  

        self.push_up(arr, i)

    def pop_min(self):
        if len(self.items) == 1: 
            self.items = [] 
            return 

        arr = self.items 
        n = len(arr)
        l = n - 1 

        item = arr[0]
        del self.key_map[arr[0].key]
        self.key_map[arr[l].key] = 0
        arr[0] = arr[l]

        arr.pop(l)
        n = len(arr)

        self.push_down(arr, 0)

    def pop_max(self): 
        if len(self.items) == 1: 
            self.items = [] 
            return 
        elif len(self.items) == 2: 
            i = 1
        elif len(self.items) > 2:
            i = None
            a = self.items[1]
            b = self.items[2]
            if not self.comparator(a, b): 
                i = 1 
            else: 
                i = 2 
        
        arr = self.items 
        n = len(arr)
        l = n - 1 

        item = arr[i]
        del self.key_map[item.key]
        self.key_map[arr[l].key] = 0
        arr[i] = arr[l]

        arr.pop(l)
        n = len(arr)

        self.push_down(arr, i)

    def delete(self, key):
        if key not in self.key_map: 
            raise Exception(f"{key} is not a key in heap.")
        arr = self.items
        i = self.key_map[key] 
        arr[i].value = float('-inf') 
        self.push_up(arr, i)
        self.pop_min()

    def clear(self): 
        self.items = []

    #
    # ACCESSORS / MUTATORS
    # 

    def update(self, key, new_value): 
        arr = self.items
        i = self.key_map[key]
        item = arr[i]
        self.delete(key)
        self.insert(key, new_value, item.data) 

    def items(self): 
        for item in self.items: 
            yield item
            
    def keys(self): 
        for item in self.items: 
            yield item.key
    
    def values(self): 
        for item in self.items: 
            yield item.value

    def min(self): 
        if self.size() == 0: 
            return None
        else: 
            return self.items[0]
    
    def max(self): 
        if self.size() == 0: 
            return None 
        elif self.size() == 1: 
            return self.items[0] 
        elif self.size() == 2: 
            return self.items[1] 
        else: 
            a = self.items[1]
            b = self.items[2]
            if not self.comparator(a, b):
                return self.items[1] 
            else: 
                return self.items[2]

    def min_value(self): 
        return self.min().value 
    
    def max_value(self): 
        return self.max().value

    def min_key(self): 
        return self.min().key 
    
    def max_key(self): 
        return self.max().key

    def size(self): 
        return len(self.items)

    def is_empty(self): 
        return self.size() == 0

    def get_data(self, key): 
        return self.get_item(key).data

    def set_data(self, key, data): 
        self.get_item(key).data = data

    def get_value(self, key): 
        return self.get_item(key).value 

    def set_value(self, key, value): 
        self.get_item(key).value = value

    def get_item(self, key): 
        return self.items[self.key_map[key]]

    def set_item(self, key, item): 
        self.key_map[key] = item

    def has_key(self, key): 
        return key in self.key_map

    def clear(self): 
        self.items = []
        self.key_no = 0
        self.key_map = {}