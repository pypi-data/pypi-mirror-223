
import pytest 
from dsap.queues.structs.priority_queue import PriorityQueue 

def test_size(): 
    queue = PriorityQueue() 
    assert(queue.size() == 0)

@pytest.mark.depends(on=["test_size"])
def test_enqueue():
    queue = PriorityQueue() 
    
    assert(queue.size() == 0)

    queue.enqueue(2, "C") 
    queue.enqueue(1, "A") 
    queue.enqueue(3, "B")
    queue.enqueue(1, "D") 
    queue.enqueue(2, "E") 
    queue.enqueue(3, "F")

    assert(queue.size() == 6)

@pytest.mark.depends(on=["enqueue"])
def test_front_a(): 
    queue = PriorityQueue()  

    queue.enqueue("C", 2) 
    queue.enqueue("A", 1) 
    queue.enqueue("B", 3)
    queue.enqueue("D", 1) 
    queue.enqueue("E", 2) 
    queue.enqueue("F", 3)

    assert(queue.front().key == "A")

@pytest.mark.depends(on=["enqueue"])
def test_back_a(): 
    queue = PriorityQueue()  

    queue.enqueue("C", 2) 
    queue.enqueue("A", 1) 
    queue.enqueue("B", 3)
    queue.enqueue("D", 1) 
    queue.enqueue("F", 3)
    queue.enqueue("E", 2) 

    assert(queue.back().key == "F")


@pytest.mark.depends(on=["enqueue", "front"])
def test_dequeue_front(): 
    queue = Deque()  

    queue.enqueue("C", 2) 
    queue.enqueue("A", 1) 
    queue.enqueue("B", 3)
    queue.enqueue("D", 1) 
    queue.enqueue("F", 3)
    queue.enqueue("E", 2) 

    queue.dequeue_front()

    assert(queue.front().key == "D")

@pytest.mark.depends(on=["enqueue", "front"])
def test_dequeue_front(): 
    queue = PriorityQueue()  

    queue.enqueue("C", 2) 
    queue.enqueue("A", 1) 
    queue.enqueue("B", 3)
    queue.enqueue("D", 1) 
    queue.enqueue("F", 3)
    queue.enqueue("E", 2) 

    queue.dequeue_back()

    assert(queue.back().key == "B")


@pytest.mark.depends(on=["enqueue", "size"])
def test_dequeue_front(): 
    queue = PriorityQueue()  

    queue.enqueue("C", 2) 
    queue.enqueue("A", 1) 
    queue.enqueue("B", 3)
    queue.enqueue("D", 1) 
    queue.enqueue("F", 3)
    queue.enqueue("E", 2) 

    queue.clear()

    assert(queue.size() == 0)
