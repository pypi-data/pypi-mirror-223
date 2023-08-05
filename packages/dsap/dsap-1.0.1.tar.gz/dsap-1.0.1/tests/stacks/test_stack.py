import pytest
from dsap.stacks.structs.stack import Stack 

@pytest.mark.depends(on=["test_stack_push"])
def test_stack_size():
    stack = Stack() 
    
    stack.push(1)
    stack.push(2)
    stack.push(3) 

    assert(stack.size() == 3)

@pytest.mark.depends(on=["test_stack_push"])
def test_stack_top(): 
    stack = Stack() 

    stack.push(1) 
    stack.push(2)
    stack.push(3) 

    assert(stack.top() == 3) 

def test_stack_push(): 
    stack = Stack() 
    
    stack.push(1)

    assert(len(stack.items) == 1) 

@pytest.mark.depends(on=["test_stack_top", "test_stack_push"])
def test_stack_pop(): 
    stack = Stack() 

    stack.push(1)
    stack.push(2)
    stack.push(3)

    stack.pop()

    assert(stack.top() == 2)  

@pytest.mark.depends(on=["test_stack_push", "test_stack_pop", "test_stack_size"])
def test_stack_is_empty(): 
    stack = Stack() 

    stack.push(1) 
    stack.push(2)
    stack.push(3)

    stack.pop() 
    stack.pop() 
    stack.pop() 

    assert(stack.size() == 0)

@pytest.mark.depends(on=["test_push", "test_size"])
def test_stack_clear():
    stack = Stack() 

    stack.push(1)
    stack.push(2) 
    stack.push(3)

    stack.clear() 

    assert(stack.size() == 0)