"""A limited-size stack that drops the oldest element when it is full"""

from ast import TypeVar
from typing import Iterator

T = TypeVar("T", covariant=True)


class DroppingStack[T]:
    """A stack that drops the oldest element when it is full"""

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.stack: list[T] = []

    def push(self, item: T):
        """Pushes an element to the stack"""
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)  # Remove the oldest element
        self.stack.append(item)

    def pop(self) -> T | None:
        """Pops the latest element"""
        return self.stack.pop()

    def peek(self) -> T | None:
        """Peeks the next element to be popped"""
        if self.stack:
            return self.stack[-1]
        return None

    def is_empty(self) -> bool:
        """Returns whether the stack is empty or not"""
        return not bool(self.stack)

    def is_full(self) -> bool:
        """Returns whether the stack is full or not"""
        return len(self.stack) == self.max_size

    def clear(self):
        """Clears the stack"""
        self.stack.clear()

    def __len__(self) -> int:
        return len(self.stack)

    def __getitem__(self, index: int) -> T:
        return self.stack[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self.stack)

    def __str__(self) -> str:
        return f"DroppingStack({self.stack})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DroppingStack):
            return NotImplemented
        return self.stack == other.stack
