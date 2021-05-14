# run this as:
#   python3.9 -m algorithms.recursive_sum
import sys
from pathlib import Path
from typing import Sequence

import pytest as pytest


def recursive_sum(args: Sequence[int]) -> int:
    """
    >>> recursive_sum([1, 2, 3, 4])
    10
    """
    if not args:
        return 0
    return args[0] + recursive_sum(args[1:])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        pytest.main(sys.argv[:1])
    elif len(sys.argv) > 1:
        path, *values = sys.argv
        values = [int(value) for value in values]
        result = recursive_sum(values)
        print(f"For values {' '.join(sys.argv[1:])} sum is {result}")
    else:
        file_path = Path(sys.argv[0]).name
        print(
            f"Usage: {file_path} test OR {file_path} *<VALUE>", file=sys.stderr
        )
        exit(1)
