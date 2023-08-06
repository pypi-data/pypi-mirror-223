import pytest 
from dsap.heaps.structs.kkah import KKAH

Heap = KKAH

def test_insert():
    heap = Heap(3) 
    
    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(len(heap.items))

@pytest.mark.depends(on=["test_insert"])
def test_type_min():
    heap = Heap(3, "min") 
        
    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.items[0].key == "B") 

@pytest.mark.depends(on=["test_insert"])
def test_type_max():
    heap = Heap(3, "max") 
        
    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.items[0].key == "F") 

@pytest.mark.depends(on=["test_insert"])
def test_comparator():
    heap = Heap(3) 

    def comparator(a, b): 
        return a.value[1] < b.value[1]

    heap.comparator = comparator
        
    heap.insert("A", (None, 25), "Data A")
    heap.insert("B", (None, 10), "Data B")
    heap.insert("C", (None, 38), "Data C")
    heap.insert("D", (None, 22), "Data D")
    heap.insert("E", (None, 17), "Data E") 
    heap.insert("F", (None, 40), "Data F")
    heap.insert("G", (None, 30), "Data G") 
    heap.insert("H", (None, 29), "Data H")

    assert(heap.items[0].key == "B") 

@pytest.mark.depends(on=["test_insert"]) 
def test_size(): 
    heap = Heap(3) 

    assert(heap.size() == 0) 

    heap.insert("A", (None, 25), "Data A")
    heap.insert("B", (None, 10), "Data B")
    heap.insert("C", (None, 38), "Data C")
    heap.insert("D", (None, 22), "Data D")
    heap.insert("E", (None, 17), "Data E") 
    heap.insert("F", (None, 40), "Data F")
    heap.insert("G", (None, 30), "Data G") 
    heap.insert("H", (None, 29), "Data H")

    assert(heap.size() == 8)

@pytest.mark.depends(on=["test_insert"])
def test_top(): 
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")  

    assert(heap.top().key == "B")

@pytest.mark.depends(on=["test_insert"])
def test_pop():
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")  

    heap.pop()

    assert(heap.top().key == "E")

@pytest.mark.depends(on=["test_insert", "test_top"])
def test_pop():
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")  

    heap.pop()

    assert(heap.top().key == "E")

@pytest.mark.depends(on=["test_insert", "test_size"])
def test_delete(): 
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")  

    assert(heap.size() == 8)

    heap.delete("D") 

    assert(heap.size() == 7)

@pytest.mark.depends(on=["test_insert", "test_size"]) 
def test_clear(): 
    heap = Heap(3) 

    heap.insert("A", (None, 25), "Data A")
    heap.insert("B", (None, 10), "Data B")
    heap.insert("C", (None, 38), "Data C")
    heap.insert("D", (None, 22), "Data D")
    heap.insert("E", (None, 17), "Data E") 
    heap.insert("F", (None, 40), "Data F")
    heap.insert("G", (None, 30), "Data G") 
    heap.insert("H", (None, 29), "Data H")

    assert(heap.size() == 8)
    assert(heap.top().key == "B")
    assert(len(heap.key_map) == 8)
    
    heap.clear() 

    assert(heap.size() == 0)
    assert(heap.top() is None)
    assert(len(heap.key_map) == 0)


@pytest.mark.depends(on=["test_insert", "test_top"])
def test_update(): 
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.top().key == "B") 

    heap.update("G", 1)

    assert(heap.top().key == "G") 

    heap.update("H", 0)

    assert(heap.top().key == "H") 

    heap.update("H", 100)

    assert(heap.top().key == "G") 

@pytest.mark.depends(on=["test_insert"])
def test_keys(): 
    heap = Heap(3)

    items = [
       ("A", 25, "Data A"),
       ("B", 10, "Data B"),
       ("C", 38, "Data C"),
       ("D", 22, "Data D"),
       ("E", 17, "Data E"),
       ("F", 40, "Data F"),
       ("G", 30, "Data G"),
       ("H", 29, "Data H")
    ]
    
    for item in items: 
        heap.insert(*item) 

    keys = list(heap.keys())

    assert(len(keys) == len(items))

    for i in range(len(keys)): 
        item = items[i]
        assert(item[0] in keys)

@pytest.mark.depends(on=["test_insert"])
def test_values(): 
    heap = Heap(3)

    items = [
       ("A", 25, "Data A"),
       ("B", 10, "Data B"),
       ("C", 38, "Data C"),
       ("D", 22, "Data D"),
       ("E", 17, "Data E"),
       ("F", 40, "Data F"),
       ("G", 30, "Data G"),
       ("H", 29, "Data H")
    ]
    
    for item in items: 
        heap.insert(*item) 

    values = list(heap.values())

    assert(len(values) == len(items))

    for i in range(len(values)): 
        item = items[i]
        assert(item[1] in values)

@pytest.mark.depends(on=["test_insert"]) 
def test_is_empty(): 
    heap = Heap(3) 
    
    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(not heap.is_empty())

    heap.clear()

    assert(heap.is_empty())

@pytest.mark.depends(on=["test_insert"]) 
def test_get_data(): 
    heap = Heap(3) 
    
    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.get_data("D") == "Data D")

@pytest.mark.depends(on=["test_insert", "test_get_data"]) 
def test_set_data(): 
    heap = Heap(3) 
    
    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    heap.set_data("D", "Data D - Changed")

    assert(heap.get_data("D") == "Data D - Changed")

@pytest.mark.depends(on=["test_insert"]) 
def test_get_value(): 
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")
    
    assert(heap.get_value("D") == 22)


@pytest.mark.depends(on=["test_insert", "test_get_value"]) 
def test_set_value(): 
    heap = Heap(3) 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    heap.set_value("D", 44)
    
    assert(heap.get_value("D") == 44)


@pytest.mark.depends(on=["test_insert"]) 
def test_min(): 
    heap = Heap(3, "min") 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.min().key == "B")

@pytest.mark.depends(on=["test_insert"]) 
def test_max(): 
    heap = Heap(3, "max") 

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.max().key == "F")

@pytest.mark.depends(on=["test_insert"])
def test_has_key(): 
    heap = Heap(3)

    heap.insert("A", 25, "Data A")
    heap.insert("B", 10, "Data B")
    heap.insert("C", 38, "Data C")
    heap.insert("D", 22, "Data D")
    heap.insert("E", 17, "Data E") 
    heap.insert("F", 40, "Data F")
    heap.insert("G", 30, "Data G") 
    heap.insert("H", 29, "Data H")

    assert(heap.has_key("F")) 
    assert(not heap.has_key("Z"))
