# run this as:
#   python3.9 -m algorithms.binary_search

import logging
import sys
from contextvars import ContextVar
from typing import Optional, Sequence, TypeVar

import pytest

from algorithms.counter import AbstractCounter, FakeCounter, get_counter

var_counter: ContextVar[AbstractCounter] = ContextVar("counter", default=FakeCounter)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    pytest.main(sys.argv)


T = TypeVar("T")


def get_index_binary(data: Sequence[T], value: T) -> Optional[int]:
    counter = var_counter.get()
    left = 0
    right = len(data) - 1

    while left <= right:
        index = (left + right) // 2
        center = data[index]
        if center == value:
            counter.increase(f"[{left}..{right}] {value} = {center}@{index}")
            counter.finish()
            return index
        elif value < center:
            counter.increase(f"[{left}..{right}] {value} < {center}@{index}")
            right = index - 1  # exclude right
        else:
            counter.increase(f"[{left}..{right}] {center}@{index} > {value}")
            left = index + 1  # exclude left

    counter.finish("Not found")


class TestFindBinary:
    @pytest.fixture
    def range_1000(self):
        points = list(range(1000, 2000))
        assert points[0] == 1000
        assert len(points) == 1000
        assert points[999] == 1999
        return points

    @pytest.mark.parametrize("value", range(1000, 2000))
    def test_range(self, range_1000, value: int):
        with get_counter(var_counter, get_index_binary) as counter:
            index = get_index_binary(data=range_1000, value=value)
        assert index is not None
        assert index == value - 1000
        assert 1 <= counter.value <= 10

    def test_before(self, range_1000):
        with get_counter(var_counter, get_index_binary) as counter:
            value = -1
            index = get_index_binary(data=range_1000, value=value)
        assert index is None
        assert counter.value == 9

    def test_after(self, range_1000):
        with get_counter(var_counter, get_index_binary) as counter:
            value = 2000
            index = get_index_binary(data=range_1000, value=value)
        assert index is None
        assert counter.value == 10

    def test_complexity_range_1000(self, range_1000):
        with get_counter(var_counter, get_index_binary) as counter:
            for value in range_1000:
                get_index_binary(data=range_1000, value=value)
        assert counter.value == 8987

    def test_without_counter(self, range_1000):
        index = get_index_binary(data=range_1000, value=1500)
        assert index == 500


if __name__ == "__main__":
    main()
