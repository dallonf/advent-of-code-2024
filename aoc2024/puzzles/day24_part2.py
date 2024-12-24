import aoc2024.common.input as aoc_input
from .day24 import Device

if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day24input")
    device = Device.parse(puzzle_input)

    # mermaid diagrams
    with open("day24.mmd", "w", encoding="utf-8") as f:
        f.write("flowchart TD\n")
        for i, gate in enumerate(device.gates):
            f.write(f'  g{i}{'{'}"{gate.gate_type.name}"{'}'}')
            f.write("\n")
            f.write(f"  {gate.a_input} --> g{i}")
            f.write("\n")
            f.write(f"  {gate.b_input} --> g{i}")
            f.write("\n")
            f.write(f"  g{i} --> {gate.output}")
            f.write("\n")

    # check adder works with small values
    for x in range(7):
        for y in range(7):
            test_device = device.copy()
            test_device.fill_x(x)
            test_device.fill_y(y)
            test_device.simulate()
            output = test_device.extract_output()
            output = output & 0b1111
            assert (
                output == x + y
            ), f"Expected {x} + {y} to equal {x + y}, but got {output}"
    print("Confirmed working with inputs of 0-7")

    