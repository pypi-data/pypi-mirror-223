import pytest
from dsap.bsts.structs.avlt import AVLT, AVLT_Node

BST = AVLT
Node = AVLT_Node

def test_insert(): 
    bst = BST() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    assert(bst.count == 8)

@pytest.mark.depends(on=["test_insert"])
def test_size(): 
    bst = BST()

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    assert(bst.find_max(bst.root).key == "H")
 
@pytest.mark.depends(on=["test_insert"]) 
def test_iterate(): 
    bst = BST() 

    items = [
        ("A", 20),
        ("B", 5),
        ("C", 36),
        ("D", 28),
        ("E", 91),
        ("F", 47),
        ("G", 11),
        ("H", 28)
    ]

    for item in items:
        bst.insert(*item) 

    i = 0
    for item in bst.iterate(): 
        assert(item.key == items[i][0])
        assert(item.value == items[i][1])
        i += 1

@pytest.mark.depends(on=["test_insert"]) 
def test_keys(): 
    bst = BST() 

    items = [
        ("A", 20),
        ("B", 5),
        ("C", 36),
        ("D", 28),
        ("E", 91),
        ("F", 47),
        ("G", 11),
        ("H", 28)
    ]

    for item in items:
        bst.insert(*item) 

    keys = list(bst.keys())

    i = 0
    for item in items: 
        assert(item[0] in keys)
        i += 1


@pytest.mark.depends(on=["test_insert"]) 
def test_values(): 
    bst = BST() 

    items = [
        ("A", 20),
        ("B", 5),
        ("C", 36),
        ("D", 28),
        ("E", 91),
        ("F", 47),
        ("G", 11),
        ("H", 28)
    ]

    for item in items:
        bst.insert(*item) 

    values = list(bst.values())

    i = 0
    for item in items: 
        assert(item[1] in values)
        i += 1

@pytest.mark.depends(on=["test_insert"])
def test_key_prev(): 
    bst = BST() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    assert(bst.key_prev("E").key == "D")
    assert(bst.key_prev("A") is None)
    assert(bst.key_prev("H").key == "G")


@pytest.mark.depends(on=["test_insert"])
def test_prev(): 
    bst = BST() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    assert(bst.prev(bst.find("E")).key == "D")
    assert(bst.prev(bst.find("A")) is None)
    assert(bst.prev(bst.find("H")).key == "G")


@pytest.mark.depends(on=["test_insert"])
def test_key_next(): 
    bst = BST() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    assert(bst.key_next("E").key == "F")
    assert(bst.key_next("A").key == "B")
    assert(bst.key_next("H") is None)


@pytest.mark.depends(on=["test_insert"])
def test_next(): 
    bst = BST() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    assert(bst.next(bst.find("E")).key == "F")
    assert(bst.next(bst.find("A")).key == "B")
    assert(bst.next(bst.find("H")) is None)


@pytest.mark.depends(on=["test_insert"])
def test_node_range(): 
    bst = AVLT() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

    for key_a in keys: 
        for key_b in keys: 
            if key_a > key_b: 
                continue
            range_ = bst.node_range(bst.find(key_a), bst.find(key_b))
            range_ = [x.key for x in list(range_)]
            match_ = keys[keys.index(key_a):keys.index(key_b)+1]
            assert(range_ == match_) 

@pytest.mark.depends(on=["test_insert"])
def test_key_range(): 
    bst = AVLT() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

    for key_a in keys: 
        for key_b in keys: 
            if key_a > key_b: 
                continue
            range_ = bst.key_range(key_a, key_b)
            range_ = [x.key for x in list(range_)]
            match_ = keys[keys.index(key_a):keys.index(key_b)+1]
            assert(range_ == match_) 

@pytest.mark.depends(on=["test_insert"])
def test_key_range(): 
    bst = AVLT() 

    bst.insert("A", 20)
    bst.insert("B", 5)
    bst.insert("C", 36) 
    bst.insert("D", 28)
    bst.insert("E", 91) 
    bst.insert("F", 47) 
    bst.insert("G", 11)
    bst.insert("H", 28)

    keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

    for i in range(len(keys)): 
        for j in range(len(keys)): 
            if i > j: 
                continue
            range_ = bst.index_range(i, j)
            range_ = [x.key for x in list(range_)]
            match_ = keys[i:j+1]
            assert(range_ == match_) 


@pytest.mark.depends(on=["test_insert"])
def test_search_left_bound(): 
    bst = AVLT() 

    bst.insert(10, 20)
    bst.insert(20, 5)
    bst.insert(30, 36) 
    bst.insert(40, 28)
    bst.insert(50, 91) 
    bst.insert(60, 47) 
    bst.insert(70, 11)
    bst.insert(80, 28)

    left_bounds = [10, 20, 30, 40, 50, 60, 70, 80]

    assert(bst.search_left_bound(10.3).key == 10)
    assert(bst.search_left_bound(10.8).key == 10)

    assert(bst.search_left_bound(20.3).key == 20)
    assert(bst.search_left_bound(20.8).key == 20)

    assert(bst.search_left_bound(30.3).key == 30)
    assert(bst.search_left_bound(30.8).key == 30)

    assert(bst.search_left_bound(40.3).key == 40)
    assert(bst.search_left_bound(40.8).key == 40)

    assert(bst.search_left_bound(50.3).key == 50)
    assert(bst.search_left_bound(50.8).key == 50)

    assert(bst.search_left_bound(60.3).key == 60)
    assert(bst.search_left_bound(60.8).key == 60)

    assert(bst.search_left_bound(70.3).key == 70)
    assert(bst.search_left_bound(70.8).key == 70)

    assert(bst.search_left_bound(80.3).key == 80)
    assert(bst.search_left_bound(80.8).key == 80)

@pytest.mark.depends(on=["test_insert"])
def test_search_right_bound(): 
    bst = AVLT() 

    bst.insert(10, 20)
    bst.insert(20, 5)
    bst.insert(30, 36) 
    bst.insert(40, 28)
    bst.insert(50, 91) 
    bst.insert(60, 47) 
    bst.insert(70, 11)
    bst.insert(80, 28)

    left_bounds = [10, 20, 30, 40, 50, 60, 70, 80]

    assert(bst.search_right_bound(9.3).key == 10)
    assert(bst.search_right_bound(9.8).key == 10)

    assert(bst.search_right_bound(10.3).key == 20)
    assert(bst.search_right_bound(10.8).key == 20)

    assert(bst.search_right_bound(20.3).key == 30)
    assert(bst.search_right_bound(20.8).key == 30)

    assert(bst.search_right_bound(30.3).key == 40)
    assert(bst.search_right_bound(30.8).key == 40)

    assert(bst.search_right_bound(40.3).key == 50)
    assert(bst.search_right_bound(40.8).key == 50)

    assert(bst.search_right_bound(50.3).key == 60)
    assert(bst.search_right_bound(50.8).key == 60)

    assert(bst.search_right_bound(60.3).key == 70)
    assert(bst.search_right_bound(60.8).key == 70)

    assert(bst.search_right_bound(70.3).key == 80)
    assert(bst.search_right_bound(70.8).key == 80)

@pytest.mark.depends(on=["test_insert"])
def test_interval_nodes(): 
    bst = AVLT() 

    bst.insert(10, 20)
    bst.insert(20, 5)
    bst.insert(30, 36) 
    bst.insert(40, 28)
    bst.insert(50, 91) 
    bst.insert(60, 47) 
    bst.insert(70, 11)
    bst.insert(80, 28)

    interval = bst.interval_nodes(20.5, 60.5)
    assert(interval[0].key == 20 and interval[1].key == 70)

    interval = bst.interval_nodes(30.5, 50.5)
    assert(interval[0].key == 30 and interval[1].key == 60)

@pytest.mark.depends(on=["test_insert"])
def test_interval_range(): 
    bst = AVLT() 

    bst.insert(10, 20)
    bst.insert(20, 5)
    bst.insert(30, 36) 
    bst.insert(40, 28)
    bst.insert(50, 91) 
    bst.insert(60, 47) 
    bst.insert(70, 11)
    bst.insert(80, 28)

    interval = bst.interval_range(20.5, 60.5)

    keys = [20, 30, 40, 50, 60, 70]

    i = 0
    for item in interval: 
        assert(item.key == keys[i])
        i += 1
