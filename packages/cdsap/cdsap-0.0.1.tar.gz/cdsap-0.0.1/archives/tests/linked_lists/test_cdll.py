import pytest 
from dsap.linked_lists.structs.cdll import CDLL, CDLL_Node

List = CDLL
Node = CDLL_Node

def test_prepend():
    list_ = List() 

    list_.prepend(1)
    list_.prepend(2)
    list_.prepend(3) 

    assert(list_.count == 3)
    assert(list_.head.value == 3)
    assert(list_.tail.value == 1)

def test_append(): 
    list_ = List() 

    list_.append(1) 
    list_.append(2)
    list_.append(3)

    assert(list_.count == 3) 
    assert(list_.head.value == 1)
    assert(list_.tail.value == 3)

@pytest.mark.depends(on=["test_append"])
def test_at(): 
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 

    assert(list_.at(1).value == 2)

@pytest.mark.depends(on=["test_append"])
def test_search(): 
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 

    assert(list_.search(1) is not None) 
    assert(list_.search(4) is None)


@pytest.mark.depends(on=["test_append"])
def test_search_node(): 
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 

    node = CDLL_Node(None)
    middle = list_.at(1)

    assert(list_.search_node(middle) is not None) 
    assert(list_.search_node(node) is None)


@pytest.mark.depends(on=["test_append"])
def test_index(): 
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 

    assert(list_.index(2) == 1)
    assert(list_.index(4) == -1)

@pytest.mark.depends(on=["test_append"])
def test_node_index(): 
    list_ = List() 
        
    list_.append(1)
    list_.append(2)
    list_.append(3) 

    second = list_.head.next 
    node = Node(None)

    assert(list_.node_index(second) == 1)
    assert(list_.node_index(node) == -1)

@pytest.mark.depends(on=["test_append", "test_at"])
def test_node_insert():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.insert(2, 3.5) 

    assert(list_.at(2).value == 3.5)
    assert(list_.at(1).value == 2)
    assert(list_.at(3).value == 3)
 

@pytest.mark.depends(on=["test_append", "test_at"])
def test_insert_node():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    node = Node(3.5)
    list_.insert_node(2, node) 

    assert(list_.at(2).value == 3.5)
    assert(list_.at(1).value == 2)
    assert(list_.at(3).value == 3)
 

@pytest.mark.depends(on=["test_append", "test_at"])
def test_insert_after():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.insert_after(list_.at(2), 3.5) 

    assert(list_.at(3).value == 3.5)
    assert(list_.at(2).value == 3)
    assert(list_.at(1).value == 2)
 

@pytest.mark.depends(on=["test_append", "test_at"])
def test_insert_node_after():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    node = Node(3.5)
    list_.insert_node_after(list_.at(2), node) 

    assert(list_.at(3).value == 3.5)
    assert(list_.at(2).value == 3)
    assert(list_.at(1).value == 2)
 

@pytest.mark.depends(on=["test_append", "test_at"])
def test_insert_before():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.insert_before(list_.at(2), 3.5) 

    assert(list_.at(2).value == 3.5)
    assert(list_.at(3).value == 3)
    assert(list_.at(4).value == 4)
 

@pytest.mark.depends(on=["test_append", "test_at"])
def test_insert_node_before():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    node = Node(3.5)
    list_.insert_node_before(list_.at(2), node) 

    assert(list_.at(2).value == 3.5)
    assert(list_.at(3).value == 3)
    assert(list_.at(4).value == 4)

@pytest.mark.depends(on=["test_append", "test_at"]) 
def test_delete():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.delete(2)

    assert(list_.at(2).value == 4)

@pytest.mark.depends(on=["test_append", "test_at"]) 
def test_delete_node():  
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    middle = list_.at(2)

    list_.delete_node(middle)

    assert(list_.at(2).value == 4)

@pytest.mark.depends(on=["test_append", "test_at"])
def test_delete_head():
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.delete_head() 

    assert(list_.head.value == 2)

@pytest.mark.depends(on=["test_append", "test_at"])
def test_delete_tail():
    list_ = List() 

    list_.append(1)
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.delete_tail() 

    assert(list_.tail.value == 4)

@pytest.mark.depends(on=["test_append", "test_at"])
def test_delete_after():
    list_ = List() 

    list_.append(1) 
    list_.append(2)
    list_.append(3)
    list_.append(4) 
    list_.append(5) 

    node = list_.at(2)

    list_.delete_after(node) 

    assert(list_.at(3).value == 5) 


@pytest.mark.depends(on=["test_append", "test_at"])
def test_delete_before(): 
    list_ = List() 

    list_.append(1) 
    list_.append(2)
    list_.append(3) 
    list_.append(4) 
    list_.append(5)

    node = list_.at(2)

    list_.delete_before(node) 

    assert(list_.at(1).value == 3) 
    assert(list_.at(2).value == 4)

@pytest.mark.depends(on=["test_append", "test_search"]) 
def test_delete_remove(): 
    list_ = List()

    list_.append(1) 
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    list_.remove(3) 

    assert(list_.search(3) is None)

@pytest.mark.depends(on=["test_append"])
def test_predecessor(): 
    list_ = List() 

    list_.append(1) 
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5)

    node = list_.at(2) 
    predecessor = list_.predecessor(node) 

    assert(predecessor.value == 2) 

@pytest.mark.depends(on=["test_append"])
def test_successor(): 
    list_ = List() 

    list_.append(1)
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    node = list_.at(2) 
    successor = list_.successor(node)

    assert(successor.value == 4)
 
@pytest.mark.depends(on=["test_append"])
def test_predecessor(): 
    list_ = List() 

    list_.append(1) 
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    node = list_.at(2) 
    prepredecessor = list_.prepredecessor(node) 

    assert(prepredecessor.value == 1)

@pytest.mark.depends(on=["test_append"])
def test_size(): 
    list_ = List() 

    list_.append(1) 
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    assert(list_.size() == 5)

@pytest.mark.depends(on=["test_append"]) 
def test_is_empty(): 
    list_ = List() 

    assert(list_.is_empty()) 

    list_.append(1) 
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    assert(not list_.is_empty())

@pytest.mark.depends(on=["test_append"]) 
def test_iterate(): 
    list_ = List() 

    values = [1, 2, 3, 4, 5]

    for value in values: 
        list_.append(value) 

    i = 0
    for node in list_.iterate(): 
        assert(node.value == values[i])
        i += 1

@pytest.mark.depends(on=["test_append", "test_size"]) 
def test_clear(): 
    list_ = List() 

    list_.append(1) 
    list_.append(2) 
    list_.append(3) 
    list_.append(4) 
    list_.append(5) 

    assert(list_.size() == 5)
    
    list_.clear()

    assert(list_.size() == 0)