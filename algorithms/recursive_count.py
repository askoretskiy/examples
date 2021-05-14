# run this as:
#   python3.9 -m algorithms.recursive_count
import sys
from pathlib import Path
from typing import Sequence, Any

import pytest as pytest


def recursive_count(args: Sequence[Any]) -> int:
    """
    >>> recursive_count([1, 2, 3, 4])
    4
    """
    if not args:
        return 0
    return 1 + recursive_count(args[1:])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        pytest.main(sys.argv[:1])
    elif len(sys.argv) > 1:
        path, *values = sys.argv
        result = recursive_count(values)
        print(f"For values {' '.join(sys.argv[1:])} count is {result}")
    else:
        file_path = Path(sys.argv[0]).name
        print(
            f"Usage: {file_path} test OR {file_path} <LENGTH> <HEIGHT>", file=sys.stderr
        )
        exit(1)
