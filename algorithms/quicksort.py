# run this as:
#   python3.9 -m algorithms.quicksort
import sys
from pathlib import Path
from random import randint
from typing import Sequence

import pytest as pytest


def quicksort(args: Sequence[int]) -> Sequence[int]:
    """
    >>> quicksort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> quicksort([4, 2, 3, 1])
    [1, 2, 3, 4]
    >>> quicksort([1, 2, 4, 3])
    [1, 2, 3, 4]
    """
    if not args or len(args) == 1:
        return args

    index = randint(0, len(args) - 1)
    pivot = args[index]

    less = []
    greater = []

    for i, v in enumerate(args):
        if i == index:
            continue
        if v <= pivot:
            less.append(v)
        else:
            greater.append(v)

    return [*quicksort(less), pivot, *quicksort(greater)]


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
