# run this as:
#   python3.9 -m algorithms.pathfinder
import collections
import heapq
import math
import sys
from typing import Callable, Dict, List, Optional, Protocol, Tuple, TypeVar

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

    return get_route(start, goal, node_parent)


def dijkstra_search(
    graph: WeightedGraph, start: Location, goal: Location
) -> Optional[List[Location]]:
    frontier = PriorityQueue()
    frontier.put(0, start)
    node_parent = {start: None}
    cost_so_far = collections.defaultdict(lambda: math.inf)
    cost_so_far[start] = 0

    while frontier:
        node = frontier.pop()
        if node == goal:
            break

        for child in graph.neighbors(node):
            new_cost = graph.cost(node, child) + cost_so_far[node]
            if new_cost < cost_so_far[child]:
                cost_so_far[child] = new_cost
                node_parent[child] = node
                priority = new_cost
                frontier.put(priority, child)

    return get_route(start, goal, node_parent)


def a_star_search(
    graph: WeightedGraph,
    start: Location,
    goal: Location,
    heuristic_fn: Callable[[Location, Location], float],
) -> Optional[List[Location]]:
    frontier = PriorityQueue()
    frontier.put(0, start)
    node_parent = {start: None}
    cost_so_far = collections.defaultdict(lambda: math.inf)
    cost_so_far[start] = 0

    while frontier:
        node = frontier.pop()
        if node == goal:
            break

        for child in graph.neighbors(node):
            new_cost = graph.cost(node, child) + cost_so_far[node]
            if new_cost < cost_so_far[child]:
                cost_so_far[child] = new_cost
                node_parent[child] = node
                priority = new_cost + heuristic_fn(child, goal)
                frontier.put(new_cost, child)

    return get_route(start, goal, node_parent)


def get_route(
    start: Location, goal: Location, node_parent: Dict[Location, Optional[Location]]
) -> Optional[List[Location]]:
    if goal not in node_parent:
        return

    path_to_child = []
    node = goal
    while node != start:
        path_to_child.append(node)
        node = node_parent[node]

    path_to_child.append(start)
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

    def test_dijkstra(self, edges):
        graph = SimpleWeightedGraph()
        graph.edges = edges
        assert dijkstra_search(graph, "A", "F") == ["A", "B", "C", "F"]
        graph.weights = {("C", "F"): 3}
        assert dijkstra_search(graph, "A", "F") == ["A", "B", "C", "F"]
        graph.weights = {("C", "F"): 4}
        assert dijkstra_search(graph, "A", "F") == ["A", "B", "C", "D", "E", "F"]

    def test_a_start(self, edges):
        graph = SimpleWeightedGraph()
        graph.edges = edges

        def heuristic_fn(node: Location, goal: Location):
            return abs(ord(node) - ord(goal)) / (ord("F") - ord("A"))

        assert a_star_search(graph, "A", "F", heuristic_fn) == ["A", "B", "C", "F"]
        graph.weights = {("C", "F"): 3}
        assert a_star_search(graph, "A", "F", heuristic_fn) == ["A", "B", "C", "F"]
        graph.weights = {("C", "F"): 4}
        assert a_star_search(graph, "A", "F", heuristic_fn) == [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]


if __name__ == "__main__":
    pytest.main(sys.argv)
