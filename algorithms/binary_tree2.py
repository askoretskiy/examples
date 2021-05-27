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
            if child := self.left:
                child.insert(value)
            else:
                self.left = Node(value=value, parent=self)
        elif self.value < value:
            # add to the right
            if child := self.right:
                child.insert(value)
            else:
                self.right = Node(value=value, parent=self)
        else:
            raise ValueError("Duplicate value: {!r}".format(value))

    def traverse_deep(self) -> Iterator[Node]:
        if child := self.left:
            yield from child.traverse_deep()
        yield self
        if child := self.right:
            yield from child.traverse_deep()

    def traverse_wide(self) -> Iterator[Node]:
        nodes = deque([self])

        while nodes:
            node = nodes.popleft()
            yield node

            if child := node.left:
                nodes.append(child)

            if child := node.right:
                nodes.append(child)

    @property
    def depth(self) -> int:
        node = self
        depth = 0

        while node := node.parent:
            depth += 1

        return depth

    def __contains__(self, value: T):
        return bool(self.find(value))

    def find(self, value: T) -> Optional[Node]:
        if value == self.value:
            return self
        elif value < self.value:
            # look left
            if child := self.left:
                return child.find(value)
            return None
        elif self.value < value:
            # look right
            if child := self.right:
                return child.find(value)
            return None

    def delete(self, value: T):
        node = self.find(value)
        if not node:
            return

        raise NotImplementedError()


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

    tree.delete(10)


if __name__ == "__main__":
    main()
