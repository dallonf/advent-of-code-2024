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


def part_one_answer(lines: list[str]) -> int:
    connections = NetworkConnections.parse(lines)
    return len(connections.find_all_historian_triads())


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day23input")
    print("Part One:", part_one_answer(puzzle_input))
