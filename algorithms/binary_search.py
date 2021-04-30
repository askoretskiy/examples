#!/usr/bin/env python3.9
from typing import Sequence, Optional


def main():
    data = list(range(1, 1000, 2))
    value = 800
    index = find_binary(data, value)
    print(f"Found with binary: #{index}")


def find_binary(data: Sequence[int], value: int) -> Optional[int]:
    left = 0
    right = len(data) - 1
    step = 1

    while left <= right:
        index = (left + right) // 2
        center = data[index]
        if center == value:
            print(f"{step}. {left}..{right} @{index}:{center} = {value}")
            return index
        elif value < center:
            print(f"{step}. {left}..{right} @{index}:{center} > {value}")
            right = index - 1  # exclude right
        else:
            print(f"{step}. {left}..{right} @{index}:{center} < {value}")
            left = index + 1  # exclude left
        step += 1

    print(f"{step}. not found")


if __name__ == "__main__":
    main()
