from __future__ import annotations

import dataclasses
import random
from collections import deque
from typing import Iterator, Optional, TypeVar

T = TypeVar("T")


@dataclasses.dataclass(init=False)
class Node:
    parent: Node
    value: T
    left: Optional[Node]
    right: Optional[Node]

    def __init__(self, value: T, parent: Node):
        self.value = value
        self.parent = parent
        self.left = self.right = None

    def insert(self, value: T):
        if value < self.value:
            # add to the left
            if self.left:
                self.left.insert(value)
            else:
                self.left = Node(value=value, parent=self)
        elif self.value < value:
            # add to the right
            if self.right:
                self.right.insert(value)
            else:
                self.right = Node(value=value, parent=self)
        else:
            raise ValueError("Duplicate value: {!r}".format(value))

    def traverse_deep(self) -> Iterator[Node]:
        if self.left:
            yield from self.left.traverse_deep()
        yield self
        if self.right:
            yield from self.right.traverse_deep()

    def traverse_wide(self) -> Iterator[Node]:
        nodes = deque([self])

        while nodes:
            node = nodes.popleft()
            yield node
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)

    @property
    def depth(self) -> int:
        return 1 + self.parent.depth


@dataclasses.dataclass(init=False)
class BinaryTree(Node):
    parent = None
    value: Optional[T]
    left: Optional[Node]
    right: Optional[Node]
    depth = 0

    def __init__(self):
        self.parent = self.value = self.left = self.right = None

    def insert(self, value: T):
        if self.value is None:
            self.value = value
        else:
            super().insert(value)


def main():
    tree = BinaryTree()

    values = list(range(0, 100, 3))

    # random.shuffle(values)
    # for value in values:
    #     tree.insert(value)

    middle = (len(values) - 1) // 2
    tree.insert(values[middle])

    for i in range(1, middle + 1):
        tree.insert(values[middle - i])
        tree.insert(values[middle + i])

    for i in range(middle * 2 + 1, len(values)):
        tree.insert(values[i])

    print("Deep")
    for node in tree.traverse_deep():
        print("{}{:02}".format(" " * node.depth * 2, node.value))

    print("Wide")
    for node in tree.traverse_wide():
        print("{}{:02}".format(" " * node.depth * 2, node.value))


if __name__ == "__main__":
    main()
