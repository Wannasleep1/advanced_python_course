from typing import List, TypeVar


T = TypeVar("T")


class Stack:

    def __init__(self) -> None:
        self.__container: List[T] = []

    def isEmpty(self) -> bool:
        return not self.__container

    def push(self, item: T) -> None:
        self.__container.append(item)

    def pop(self) -> T:
        return self.__container.pop()

    def peek(self):
        return self.__container[-1]

    def size(self):
        return len(self.__container)
