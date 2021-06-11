#!/usr/bin/env python3
from __future__ import annotations

import sys
from typing import List, TypeVar

import pytest

T = TypeVar("T")


class MaxBinaryHeap:
    items: List[T]

    def __init__(self):
        self.items = []

    @staticmethod
    def get_parent_index(index: int) -> int:
        return index // 2

    @staticmethod
    def get_left_child_index(index: int) -> int:
        return 2 * index + 1

    @staticmethod
    def get_right_child_index(index: int) -> int:
        return 2 * index + 2

    def get_max(self) -> T:
        if not self.items:
            raise ValueError
        return self.items[0]

    def append(self, value: T):
        self.items.append(value)
        item_index = len(self.items) - 1
        while item_index:
            parent_index = self.get_parent_index(item_index)
            parent_value = self.items[parent_index]
            if value == parent_value:
                raise ValueError
            elif value < parent_value:
                # all good -> nothing to do
                return
            # parent_value < value -> swap them
            self.items[item_index], self.items[parent_index] = (
                self.items[parent_index],
                self.items[item_index],
            )
            item_index = parent_index


class Test:
    def test_increase(self):
        heap = MaxBinaryHeap()
        for i in range(10):
            heap.append(i)
        assert heap.get_max() == 9

    def test_decrease(self):
        heap = MaxBinaryHeap()
        for i in range(9, 0, -1):
            heap.append(i)
        assert heap.get_max() == 9

    def test_random(self):
        heap = MaxBinaryHeap()
        for i in (1, 3, 2, 5, 4, 7, 8, 6, 9):
            heap.append(i)
        assert heap.get_max() == 9

    def test_empty(self):
        heap = MaxBinaryHeap()
        with pytest.raises(ValueError):
            heap.get_max()

    def test_dupe(self):
        heap = MaxBinaryHeap()
        heap.append(1)
        with pytest.raises(ValueError):
            heap.append(1)


if __name__ == "__main__":
    pytest.main(sys.argv)
