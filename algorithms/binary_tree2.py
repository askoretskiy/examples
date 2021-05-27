from __future__ import annotations

import dataclasses
from collections import deque
from typing import Iterator, Optional, Sequence, TypeVar

T = TypeVar("T")


@dataclasses.dataclass(init=False, repr=False)
class Node:
    parent: Node
    value: T
    left: Optional[Node]
    right: Optional[Node]

    def __init__(self, value: T, parent: Node):
        self.value = value
        self.parent = parent
        self.left = self.right = None

    def __repr__(self):
        return f"<Node: {self.value} depth={self.depth}>"

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

    def __contains__(self, value: T):
        return bool(self.find(value))

    def find(self, value: T) -> Optional[Node]:
        if value == self.value:
            return self
        elif value < self.value:
            # look left
            if not self.left:
                return None
            return self.left.find(value)
        elif self.value < value:
            # look right
            if not self.right:
                return None
            return self.right.find(value)


@dataclasses.dataclass(init=False, repr=False)
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

    def __repr__(self):
        return "\n".join(
            "{}[{}]".format(" " * node.depth * 2, node.value)
            for node in self.traverse_deep()
        )


def fill_values(tree: BinaryTree, values: Sequence[T]):
    middle = (len(values) - 1) // 2
    tree.insert(values[middle])

    if len(values) > 3:
        fill_values(tree, values[:middle])
        fill_values(tree, values[middle + 1 :])
        return

    for i in range(1, middle + 1):
        tree.insert(values[middle - i])
        tree.insert(values[middle + i])

    for i in range(middle * 2 + 1, len(values)):
        tree.insert(values[i])


def main():
    tree = BinaryTree()

    values = list(range(0, 63))

    # for value in values:
    #     tree.insert(value)

    # insert already balanced tree
    fill_values(tree, values)

    print(tree)

    print("Wide:")
    for node in tree.traverse_wide():
        print("{}[{}]".format(" " * node.depth * 2, node.value))

    value = values[0]
    print("Search {}: {}".format(value, tree.find(value)))
    print("{} in tree: {}".format(value, value in tree))

    value = values[-1]
    print("Search {}: {}".format(value, tree.find(value)))
    print("{} in tree: {}".format(value, value in tree))


if __name__ == "__main__":
    main()
