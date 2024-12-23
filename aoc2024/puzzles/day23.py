from collections import deque
from typing import Optional
import aoc2024.common.input as aoc_input


class NetworkConnections:
    def __init__(self, connections: dict[str, set[str]]):
        self.connections = connections

    @staticmethod
    def parse(lines: list[str]) -> "NetworkConnections":
        connections = dict[str, set[str]]()

        def add_directional_connection(from_node: str, to_node: str):
            node_connections = connections.setdefault(from_node, set())
            node_connections.add(to_node)

        for line in lines:
            from_node, to_node = line.split("-")
            add_directional_connection(from_node, to_node)
            add_directional_connection(to_node, from_node)

        return NetworkConnections(connections)

    def find_all_historian_triads(self):
        return self.find_all_triads(prefix="t")

    def find_all_triads(self, prefix: Optional[str] = None) -> set[frozenset[str]]:
        result = set[frozenset[str]]()
        queue = deque[tuple[str, ...]](
            [
                (node,)
                for node in self.connections.keys()
                if prefix is None or node.startswith(prefix)
            ]
        )
        while len(queue) > 0:
            current = queue.popleft()
            if len(current) == 3:
                first = current[0]
                last = current[-1]
                if first in self.connections[last]:
                    result.add(frozenset(current))
                continue

            for n in self.connections[current[-1]]:
                if n not in current:
                    queue.append(current + (n,))

        return result

    def find_largest_cluster(self) -> frozenset[str]:
        current_best: frozenset[str] | None = None
        queue = deque[tuple[str, ...]]([(node,) for node in self.connections.keys()])
        explored = set[frozenset[str]]()
        while len(queue) > 0:
            current = queue.popleft()
            combination = frozenset(current)
            explored.add(frozenset(current))

            if current_best is None or len(current) > len(current_best):
                current_best = combination

            for n in self.connections[current[-1]]:
                if n in current:
                    # don't add a node already in the cluster
                    continue
                if frozenset(current + (n,)) in explored:
                    # we've already explored this cluster
                    continue
                if not all(n in self.connections[existing] for existing in current):
                    # the new node must be connected to all nodes already in the cluster
                    continue
                queue.appendleft(current + (n,))
        assert current_best is not None, "No cluster found"
        return current_best


def part_one_answer(lines: list[str]) -> int:
    connections = NetworkConnections.parse(lines)
    return len(connections.find_all_historian_triads())


def part_two_answer(lines: list[str]) -> str:
    connections = NetworkConnections.parse(lines)
    cluster = connections.find_largest_cluster()
    nodes = list(cluster)
    nodes.sort()
    return ",".join(nodes)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day23input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
