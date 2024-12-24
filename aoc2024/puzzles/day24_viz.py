import aoc2024.common.input as aoc_input
from .day24 import Device

if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day24input")
    device = Device.parse(puzzle_input)

    # mermaid diagrams
    print("flowchart TD")
    for i, gate in enumerate(device.gates):
        print(f'g{i}{'{'}"{gate.gate_type.name}"{'}'}')
        print(f"{gate.a_input} --> g{i}")
        print(f"{gate.b_input} --> g{i}")
        print(f"g{i} --> {gate.output}")
