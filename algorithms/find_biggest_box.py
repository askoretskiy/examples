# run this as:
#   python3.9 -m algorithms.find_biggest_box
import sys
from pathlib import Path

import pytest


def find_biggest_box(length: int, width: int) -> int:
    """
    >>> find_biggest_box(1, 1)
    1
    >>> find_biggest_box(1680, 640)
    80
    >>> find_biggest_box(640, 1680)
    80
    """
    if length < width:
        length, width = width, length
    rest = length % width
    if not rest:
        return width
    return find_biggest_box(width, rest)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        pytest.main(sys.argv[:1])
    elif len(sys.argv) == 3:
        path, x, y = sys.argv
        x = int(x)
        y = int(y)
        a = find_biggest_box(x, y)
        print(f"For box {x}x{y} biggest box is {a}x{a}: {x//a}x{y//a}")
    else:
        file_path = Path(sys.argv[0]).name
        print(f"Usage: {file_path} test OR {file_path} <LENGTH> <HEIGHT>", file=sys.stderr)
        exit(1)
