# run this as:
#   python3.9 -m algorithms.recursive_max
import sys
from pathlib import Path
from typing import Optional, Sequence

import pytest as pytest


def recursive_max(args: Sequence[int]) -> Optional[int]:
    """
    >>> recursive_max([])
    >>> recursive_max([1])
    1
    >>> recursive_max([1, 2])
    2
    >>> recursive_max([2, 1])
    2
    >>> recursive_max([1, 2, 3])
    3
    >>> recursive_max([5, 2, 3, 4, 1])
    5
    """
    if not args:
        return None

    left = args[0]

    if len(args) == 1:
        return left

    if len(args) == 2:
        right = args[1]
    else:
        right = recursive_max(args[1:])

    if left < right:
        return right
    return left


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        pytest.main(sys.argv[:1])
    elif len(sys.argv) > 1:
        path, *values = sys.argv
        values = [int(value) for value in values]
        result = recursive_max(values)
        print(f"For values {' '.join(sys.argv[1:])} max is {result}")
    else:
        file_path = Path(sys.argv[0]).name
        print(f"Usage: {file_path} test OR {file_path} *<VALUE>", file=sys.stderr)
        exit(1)
