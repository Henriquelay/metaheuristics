from utils.dropping_stack import DroppingStack


def test_more_than_max_size():
    """Test that the stack drops the oldest element when it is full"""

    stack = DroppingStack(max_size=5)
    for i in range(1, 7):
        stack.push(i)

    result = [item for item in stack.stack]

    assert result == [2, 3, 4, 5, 6]


def test_len_works():
    """Test that the len is consistent with the stack size"""

    stack = DroppingStack(max_size=5)
    assert len(stack) == 0
    for i in range(1, 7):
        stack.push(i)
        assert len(stack) == min(i, 5)


def test_getitem_works():
    """Test that getitem works"""
    stack = DroppingStack(max_size=5)
    for i in range(1, 7):
        stack.push(i)
    assert stack[0] == 2
    assert stack[1] == 3
    assert stack[2] == 4
    assert stack[3] == 5
    assert stack[4] == 6
