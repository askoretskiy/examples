# run this as:
#   python3.9 -m algorithms.sort_merge
import random
import sys
from pathlib import Path
from typing import Iterable, Iterator, List, TypeVar

import pytest

T = TypeVar("T")


def mergesort(args: List[T]) -> List[T]:
    """
    >>> mergesort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> mergesort([4, 2, 3, 1])
    [1, 2, 3, 4]
    >>> mergesort([1, 2, 4, 3])
    [1, 2, 3, 4]
    >>> data = list(range(100))
    >>> random.shuffle(data)
    >>> mergesort(data) == list(range(100))
    True
    """
    mergesort_(args, 0, len(args) - 1)
    return args


def sort_merge(a: Iterator[T], b: Iterator[T]) -> Iterable[T]:
    a_next = next(a, None)
    b_next = next(b, None)

    while a_next is not None or b_next is not None:
        if b_next is None or (a_next is not None and a_next < b_next):
            yield a_next
            a_next = next(a, None)
        else:
            yield b_next
            b_next = next(b, None)


def merge(arr: List[T], left: int, middle: int, right: int):
    left_copy = list(arr[left : middle + 1])
    right_copy = list(arr[middle + 1 : right + 1])

    left_iter = iter(left_copy)
    right_iter = iter(right_copy)

    for i, value in enumerate(sort_merge(left_iter, right_iter), left):
        arr[i] = value


def mergesort_(array: List[T], left: int, right: int):
    if left >= right:
        return

    middle = (left + right - 1) // 2
    mergesort_(array, left, middle)
    mergesort_(array, middle + 1, right)
    merge(array, left, middle, right)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        pytest.main(sys.argv[:1])
    elif len(sys.argv) > 1:
        path, *values = sys.argv
        values = [int(value) for value in values]
        result = mergesort(values)
        result = (str(x) for x in result)
        print(f"For values {' '.join(sys.argv[1:])} quicksort is {' '.join(result)}")
    else:
        file_path = Path(sys.argv[0]).name
        print(f"Usage: {file_path} test OR {file_path} *<VALUE>", file=sys.stderr)
        exit(1)
