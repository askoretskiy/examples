# run this as:
#   python3.9 -m algorithms.pathfinder
import collections
import heapq
import math
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


class WeightedGraph(Graph):
    def cost(self, from_node: Location, to_node: Location) -> float:
        ...


class SimpleWeightedGraph(SimpleGraph, WeightedGraph):
    weights: Dict[Tuple[Location, Location], float]

    def __init__(self):
        super().__init__()
        self.weights = {}

    def cost(self, from_node: Location, to_node: Location) -> float:
        return self.weights.get((from_node, to_node), 1)


class PriorityQueue:
    items: List[Tuple[float, T]]

    def __init__(self):
        self.items = []

    def __bool__(self):
        return bool(self.items)

    def pop(self):
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

    return get_route(goal, node_parent)


def dijkstra_search(
    graph: WeightedGraph, start: Location, goal: Location
) -> Optional[List[Location]]:
    frontier = PriorityQueue()
    frontier.put(0, start)
    node_parent = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        node = frontier.pop()
        if node == goal:
            break

        for child in graph.neighbors(node):
            new_cost = graph.cost(node, child) + cost_so_far[node]
            if new_cost < cost_so_far.get(child, math.inf):
                cost_so_far[child] = new_cost
                node_parent[child] = node
                frontier.put(new_cost, child)

    return get_route(goal, node_parent)


def get_route(
    goal: Location, node_parent: Dict[Location, Optional[Location]]
) -> Optional[List[Location]]:
    if goal not in node_parent:
        return

    path_to_child = []
    parent = goal
    while parent:
        path_to_child.append(parent)
        parent = node_parent[parent]

    return path_to_child[::-1]


class TestPathfinder:
    @pytest.fixture
    def edges(self):
        return {
            "A": ["B"],
            "B": ["C"],
            "C": ["B", "D", "F"],
            "D": ["C", "E"],
            "E": ["F"],
            "F": [],
        }

    def test_breadth_first_search(self, edges):
        graph = SimpleGraph()
        graph.edges = edges
        assert breadth_first_search(graph, "A", "F") == ["A", "B", "C", "F"]
        assert breadth_first_search(graph, "A", "E") == ["A", "B", "C", "D", "E"]
        assert breadth_first_search(graph, "F", "A") is None

    def test_two(self, edges):
        graph = SimpleWeightedGraph()
        graph.edges = edges
        assert dijkstra_search(graph, "A", "F") == ["A", "B", "C", "F"]
        graph.weights = {("C", "F"): 3}
        assert dijkstra_search(graph, "A", "F") == ["A", "B", "C", "F"]
        graph.weights = {("C", "F"): 4}
        assert dijkstra_search(graph, "A", "F") == ["A", "B", "C", "D", "E", "F"]


if __name__ == "__main__":
    pytest.main(sys.argv)
