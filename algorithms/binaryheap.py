#!/usr/bin/env python3
from __future__ import annotations

import sys
from typing import List, TypeVar

import pytest

T = TypeVar("T")


class MaxBinaryHeap:
    items: List[T]

    def __init__(self, *args: T):
        self.items = []
        for value in args:
            self.append(value)

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
        child_index = len(self.items) - 1
        while child_index:
            parent_index = self.get_parent_index(child_index)
            parent_value = self.items[parent_index]
            if value == parent_value:
                raise ValueError
            elif value < parent_value:
                # all good -> nothing to do
                return
            # parent_value < value -> swap them
            self.items[child_index], self.items[parent_index] = (
                self.items[parent_index],
                self.items[child_index],
            )
            child_index = parent_index

    def pop_max(self) -> T:
        if len(self.items) == 1:
            return self.items.pop()

        max_value = self.get_max()
        value = self.items.pop()
        self.items[0] = value
        self.balance_index(index=0, value=value)
        return max_value

    def balance_index(self, index: int, value: T):
        max_index = len(self.items) - 1

        while True:
            left_child_index = self.get_left_child_index(index)
            right_child_index = self.get_right_child_index(index)

            children_indexes = [left_child_index, right_child_index]
            children_indexes = [idx for idx in children_indexes if idx <= max_index]
            children_values = [self.items[i] for i in children_indexes]

            if all(children_value < value for children_value in children_values):
                break

            if len(children_indexes) == 1:
                # parent has only one child and it is bigger than it is
                child_index = children_indexes[0]
            else:
                if children_values[0] < children_values[1]:
                    child_index = children_indexes[1]
                else:
                    child_index = children_indexes[0]

            self.items[index], self.items[child_index] = (
                self.items[child_index],
                self.items[index],
            )
            index = child_index

    def pop_all(self):
        while self.items:
            yield self.pop_max()


class Test:
    random_items = [0, 1, 3, 2, 5, 6, 4, 8, 7, 9]

    @pytest.mark.parametrize("max_value", range(10))
    def test_max_increase(self, max_value):
        heap = MaxBinaryHeap(*range(max_value + 1))
        assert heap.get_max() == max_value

    @pytest.mark.parametrize("max_value", range(10))
    def test_max_decrease(self, max_value):
        heap = MaxBinaryHeap(*range(max_value, -1, -1))
        assert heap.get_max() == max_value

    @pytest.mark.parametrize("max_index", range(10))
    def test_max_random(self, max_index):
        items = self.random_items[: max_index + 1]
        heap = MaxBinaryHeap(*items)
        assert heap.get_max() == max(items)
        assert 0 <= heap.get_max() <= 9

    def test_max_empty(self):
        with pytest.raises(ValueError):
            MaxBinaryHeap().get_max()

    def test_pop_empty(self):
        with pytest.raises(ValueError):
            MaxBinaryHeap().pop_max()

    def test_add_dupe(self):
        with pytest.raises(ValueError):
            MaxBinaryHeap(1, 1)

    @pytest.mark.parametrize("max_value", range(10))
    def test_pop_increase(self, max_value):
        heap = MaxBinaryHeap(*range(max_value + 1))
        result = list(heap.pop_all())
        assert result == list(range(max_value, -1, -1))

    @pytest.mark.parametrize("max_value", range(10))
    def test_pop_decrease(self, max_value):
        heap = MaxBinaryHeap(*range(max_value, -1, -1))
        result = list(heap.pop_all())
        assert result == list(range(max_value, -1, -1))

    @pytest.mark.parametrize("max_index", range(10))
    def test_pop_random(self, max_index):
        items = self.random_items[: max_index + 1]
        heap = MaxBinaryHeap(*items)
        result = list(heap.pop_all())
        assert result == sorted(items, reverse=True)


if __name__ == "__main__":
    pytest.main(sys.argv)
