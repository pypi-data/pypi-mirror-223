""" 
    SEGMENT TREE DATA STRUCTURE
    Source: https://www.educative.io/answers/what-is-a-segment-tree
""" 

class SegmentTree: 
    def __init__(self, items): 
        self.length     = len(items)
        self.items      = [None] * (len(items) * 4)
        self.size       = len(self.items) 
        self.default    = 0
        self.key_map    = [None] * len(items) 

        self.construct(items, 0, 0, self.length - 1) 

    def operation(self, a, b):
        return a + b 

    def construct(self, items, i, lb, rb, level = 0): 
        if i >= self.size or lb == rb: 
            self.items[i] = items[lb]
            self.key_map[lb] = i
            return
        else: 
            mid = (lb + rb) // 2

            self.construct(items, 2 * i + 1, lb, mid, level + 1) 
            self.construct(items, 2 * i + 2, mid + 1, rb, level + 1) 

            self.items[i] = self.items[2 * i + 1] + self.items[2 * i + 2]

    def update(self, i, new_value): 
        idx = self.key_map[i]
        old_value = self.items[idx] 
        diff = new_value - old_value

        while idx >= 0: 
            self.items[idx] += old_value 
            idx = (idx - 1) // 2

    def range_sum(self, a, b, lb = None, rb = None, i = 0):        

        if lb is None: 
            lb = 0 
        if rb is None: 
            rb = self.length - 1

        
        mid = (lb + rb) // 2 

        # print(a, b, " : ", lb, rb,  " : ", mid)

        if a == lb and b == rb:
            # print("Case A")
            return self.items[i]
        if a <= mid and b <= mid:
            # print("Case B") 
            m = b
            if b > mid: 
                m = mid 
            return self.range_sum(a, m, lb, mid, 2 * i + 1) 
        elif a > mid and b > mid:
            # print("Case C") 
            m = a
            if a < mid: 
                m = mid
            return self.range_sum(m, b, mid + 1, rb, 2 * i + 2)
        elif a <= mid and b > mid:
            # print("Case D")
            m = mid
            left = self.range_sum(a, m, lb, mid, 2 * i + 1) 
            right = self.range_sum(m + 1, b, mid + 1, rb, 2 * i + 2) 
            return left + right
        else:
            raise Exception("Unknown case")

    def find_interval(self, value): 
        
        # PHASE A: FIND KEY LOCATION
        i = 0 

        lb = 0 
        rb = self.length - 1
        
        tentative = None

        while i < self.size : 
            left = self.left(i)
            right = self.right(i)

            if tentative is None: 
                tentative = left
            
            if left is None and right is None:
                break

            if lb == rb: 
                break
            
            mid = (lb + rb) // 2

            if value > tentative: 
                tentative = tentative + right 
                lb = mid + 1
                i = 2 * i + 2 
            else: 
                tentative = tentative - right
                rb = mid
                i = 2 * i + 1  
        
        # PHASE 2: FIX LOCATION         
        center = self.range_sum(0, lb, 0, self.length - 1)
        left = self.range_sum(0, lb - 1, 0, self.length - 1) 
        right = self.range_sum(0, lb + 1, 0, self.length - 1)

        res = None

        if value < center and value >= left:
            res = max(lb - 1, 0) 
        if value < center and value < left: 
            res = max(lb - 2, 0) 
        if value > center and value <= right: 
            res = lb 
        if value > center and value > right: 
            res = lb + 1 
        if value == center: 
            res = lb
    
        return (res, res + 1)     
   
    def left(self, i): 
        return self.items[2 * i + 1] 
    
    def right(self, i): 
        return self.items[2 * i + 2]

    def is_leaf(self, i): 
        return 

if __name__ == "__main__": 
    items = [4, 1, 8, 9, 2, 6, 4, 1]
    segment_tree = SegmentTree(items)

    print(segment_tree.items)

    for i in range(36): 
        print(i, segment_tree.find_interval(i))
        print()
    
    print( segment_tree.find_interval(34.5))
