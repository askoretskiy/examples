# run this as:
#   python3.9 -m algorithms.pathfinder
import collections
import heapq
import sys
from typing import Dict, List, Optional, Protocol, Tuple, TypeVar

import pytest

T = TypeVar("T")

Location = TypeVar("Location")


class Graph(Protocol):
    def neighbors(self, node: Location) -> List[Location]:
        ...


class SimpleGraph(Graph):
    edges: Dict[Location, List[Location]]

    def __init__(self):
        self.edges = {}

    def neighbors(self, node: Location) -> List[Location]:
        return self.edges[node]


class PriorityQueue:
    items: List[Tuple[float, T]]

    def __init__(self):
        self.items = []

    def __bool__(self):
        return bool(self.items)

    def get(self):
        _priority, item = heapq.heappop(self.items)
        return item

    def put(self, priority: float, item: T):
        heapq.heappush(self.items, (priority, item))


def breadth_first_search(
    graph: Graph, start: Location, goal: Location
) -> Optional[List[Location]]:
    frontier = collections.deque()
    frontier.appendleft(start)
    node_parent = {start: None}

    while frontier:
        node = frontier.pop()

        if node == goal:
            break

        for child in graph.neighbors(node):
            if child not in node_parent:
                node_parent[child] = node
                frontier.append(child)

    if goal not in node_parent:
        return

    path_to_child = []
    parent = goal
    while parent:
        path_to_child.append(parent)
        parent = node_parent[parent]

    return path_to_child[::-1]


class TestPathfinder:
    def test_breadth_first_search(self):
        graph = SimpleGraph()
        graph.edges = {
            "A": ["B"],
            "B": ["C"],
            "C": ["B", "D", "F"],
            "D": ["C", "E"],
            "E": ["F"],
            "F": [],
        }
        assert breadth_first_search(graph, "A", "F") == ["A", "B", "C", "F"]
        assert breadth_first_search(graph, "A", "E") == ["A", "B", "C", "D", "E"]
        assert breadth_first_search(graph, "F", "A") is None


if __name__ == "__main__":
    pytest.main(sys.argv[:1])
