import pytest 
from dsap.queues.structs.deque import Deque 

def test_size(): 
    queue = Deque() 
    assert(queue.size() == 0)

@pytest.mark.depends(on=["test_size"])
def test_enqueue_front():
    queue = Deque() 
    
    assert(queue.size() == 0)

    queue.enqueue_front(1) 
    queue.enqueue_front(2)
    queue.enqueue_front(3) 

    assert(queue.size() == 3)

@pytest.mark.depends(on=["test_size"])
def test_enqueue_back():
    queue = Deque() 

    assert(queue.size() == 0)

    queue.enqueue_front(1) 
    queue.enqueue_front(2)
    queue.enqueue_front(3) 

    assert(queue.size() == 3)

@pytest.mark.depends(on=["enqueue_back"])
def test_front_a(): 
    queue = Deque()  

    queue.enqueue_back(1)
    queue.enqueue_back(2)
    queue.enqueue_back(3)

    assert(queue.front().value == 1)

@pytest.mark.depends(on=["enqueue_front"])
def test_front_b(): 
    queue = Deque()  

    queue.enqueue_front(1)
    queue.enqueue_front(2)
    queue.enqueue_front(3)

    assert(queue.front().value == 3)

@pytest.mark.depends(on=["enqueue_back"])
def test_back_a(): 
    queue = Deque()  

    queue.enqueue_back(1)
    queue.enqueue_back(2)
    queue.enqueue_back(3)

    assert(queue.back().value == 3)

@pytest.mark.depends(on=["enqueue_front"])
def test_back_a(): 
    queue = Deque()  

    queue.enqueue_front(1)
    queue.enqueue_front(2)
    queue.enqueue_front(3)

    assert(queue.back().value == 1)

@pytest.mark.depends(on=["enqueue_back", "front"])
def test_dequeue_front(): 
    queue = Deque()  

    queue.enqueue_back(1)
    queue.enqueue_back(2)
    queue.enqueue_back(3)

    queue.dequeue_front()

    assert(queue.front().value == 2)

@pytest.mark.depends(on=["enqueue_back", "back"])
def test_dequeue_back(): 
    queue = Deque()  

    queue.enqueue_back(1)
    queue.enqueue_back(2)
    queue.enqueue_back(3)

    queue.dequeue_back()

    assert(queue.back().value == 2)

@pytest.mark.depends(on=["enqueue_back", "size"])
def test_clear(): 
    queue = Deque()  

    queue.enqueue_back(1)
    queue.enqueue_back(2)
    queue.enqueue_back(3)

    queue.clear()

    assert(queue.size() == 0)
