# run this as:
#   python3.9 -m algorithms.quicksort
import random
import sys
from pathlib import Path
from typing import List, TypeVar

import pytest

T = TypeVar("T")


def quicksort(args: List[T]) -> List[T]:
    """
    >>> quicksort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> quicksort([4, 2, 3, 1])
    [1, 2, 3, 4]
    >>> quicksort([1, 2, 4, 3])
    [1, 2, 3, 4]
    >>> data = list(range(100))
    >>> random.shuffle(data)
    >>> quicksort(data) == list(range(100))
    True
    """
    quicksort_(args, 0, len(args) - 1)
    return args


def swap(arr: List[T], a: int, b: int):
    if a == b:
        return
    arr[a], arr[b] = arr[b], arr[a]


def partition(arr: List[T], low: int, high: int) -> int:
    next_smaller_index = low - 1  # index of smaller element
    pivot_index = random.randint(low, high)
    pivot = arr[pivot_index]
    swap(arr, pivot_index, high)

    for j in range(low, high + 1):
        if arr[j] <= pivot:
            # put it to the next smaller index
            next_smaller_index += 1
            swap(arr, j, next_smaller_index)

    # next_smaller_index contains the reference to pivot (the highest element that is <= pivot)
    return next_smaller_index


def quicksort_(array: List[T], begin: int, end: int):
    if begin >= end:
        return
    pivot_index = partition(array, begin, end)
    quicksort_(array, begin, pivot_index - 1)
    quicksort_(array, pivot_index + 1, end)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        pytest.main(sys.argv[:1])
    elif len(sys.argv) > 1:
        path, *values = sys.argv
        values = [int(value) for value in values]
        result = quicksort(values)
        result = (str(x) for x in result)
        print(f"For values {' '.join(sys.argv[1:])} quicksort is {' '.join(result)}")
    else:
        file_path = Path(sys.argv[0]).name
        print(f"Usage: {file_path} test OR {file_path} *<VALUE>", file=sys.stderr)
        exit(1)
