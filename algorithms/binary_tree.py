# run this as:
#   python3.9 -m algorithms.binary_tree

from __future__ import annotations

import dataclasses
import logging
import string
import sys
from enum import Enum
from typing import Any, Iterable, Optional, Tuple, TypeVar

import pytest


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    pytest.main(sys.argv)


T = TypeVar("T")


@dataclasses.dataclass
class BinaryTree:
    node: Optional[RootNode] = None

    def add(self, value: T, payload: Any):
        if not self.node:
            self.node = RootNode(value=value, payload=payload, left=None, right=None)
            return

        self.node.add(value=value, payload=payload)

    def traverse(self) -> Iterable[Tuple[int, BaseNode]]:
        if not self.node:
            return
        yield from self.node.traverse()

    def __iter__(self):
        if not self.node:
            return
        yield from self.node

    def __len__(self):
        if not self.node:
            return 0
        return len(self.node)


class Position(Enum):
    LESS = 1
    EQUAL = 2
    GREATER = 3


@dataclasses.dataclass
class NodeWithPosition:
    node: BaseNode
    position: Position


@dataclasses.dataclass
class BaseNode:
    value: T
    payload: Any

    left: Optional[Node]
    right: Optional[Node]

    def find_node_to_add(self, value: T) -> NodeWithPosition:
        node = self

        while True:
            if node.value == value:
                return NodeWithPosition(node=node, position=Position.EQUAL)
            elif value < node.value:
                # check left tree
                if not node.left:
                    return NodeWithPosition(node=node, position=Position.LESS)
                node = node.left
            elif node.value < value:
                # check right tree
                if not node.right:
                    return NodeWithPosition(node=node, position=Position.GREATER)
                node = node.right

    def add(self, value: T, payload: Any):
        node_to_add = self.find_node_to_add(value=value)

        if node_to_add.position == Position.EQUAL:
            # same value => overwrite payload
            node_to_add.node.payload = payload
            return

        node = Node(
            parent=node_to_add.node, value=value, payload=payload, left=None, right=None
        )

        if node_to_add.position == Position.LESS:
            # value is less => assign as left node
            node_to_add.node.left = node
        elif node_to_add.position == Position.GREATER:
            # value is greater => assign as right node
            node_to_add.node.right = node
        else:
            raise ValueError(node_to_add.position)

    def traverse(self) -> Iterable[Tuple[int, BaseNode]]:
        if self.left:
            for level_, node in self.left.traverse():
                yield level_ + 1, node
        yield 0, self
        if self.right:
            for level_, node in self.right.traverse():
                yield level_ + 1, node

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self
        if self.right:
            yield from self.right

    def __len__(self):
        return sum(1 for _node in self)


@dataclasses.dataclass
class RootNode(BaseNode):
    parent: None = None


@dataclasses.dataclass
class Node(BaseNode):
    parent: BaseNode


class TestBinaryTree:
    @pytest.fixture
    def tree(self):
        tree = BinaryTree()

        values = 50, 50, 30, 35, 25, 20, 26, 71, 72, 73
        assert len(values) == 10
        payloads = string.ascii_lowercase

        for value, payload in zip(values, payloads):
            tree.add(value=value, payload=payload)
        return tree

    def test_add(self, tree):
        for level, node in tree.traverse():
            print("{} {!r}:{!r}".format(" " * (level * 4), node.value, node.payload))

        for node in tree:
            print("{!r}:{!r}".format(node.value, node.payload))

        assert len(tree) == 9
        # assert False


if __name__ == "__main__":
    main()
