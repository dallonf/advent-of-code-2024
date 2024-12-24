from dataclasses import dataclass
from enum import Enum, auto
import re
import aoc2024.common.input as aoc_input


class GateType(Enum):
    And = auto()
    Or = auto()
    Xor = auto()


@dataclass(frozen=True)
class Gate:
    a_input: str
    b_input: str
    output: str
    gate_type: GateType

    @staticmethod
    def parse(line: str) -> "Gate":
        match = re.match(
            r"([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})", line
        )
        assert match is not None

        match match.group(2):
            case "AND":
                gate_type = GateType.And
            case "OR":
                gate_type = GateType.Or
            case "XOR":
                gate_type = GateType.Xor
            case _:
                raise AssertionError()

        return Gate(
            a_input=match.group(1),
            gate_type=gate_type,
            b_input=match.group(3),
            output=match.group(4),
        )

    def compute(self, a: bool, b: bool) -> bool:
        match self.gate_type:
            case GateType.And:
                return a and b
            case GateType.Or:
                return a or b
            case GateType.Xor:
                return a ^ b


class Device:
    def __init__(self, wires: dict[str, bool], gates: dict[str, Gate]):
        self.wires = wires
        self.gates = gates

    @staticmethod
    def parse(lines: list[str]) -> "Device":
        split = lines.index("")

        wires = dict[str, bool]()
        for initial_line in lines[:split]:
            label, value = initial_line.split(": ")
            value = value == "1"
            wires[label] = value

        gates = (Gate.parse(l) for l in lines[split + 1 :])
        gates = {g.output: g for g in gates}

        return Device(wires, gates)

    def simulate(self):
        while True:
            updated_any = False
            for g in self.gates.values():
                if (
                    not g.output in self.wires
                    and g.a_input in self.wires
                    and g.b_input in self.wires
                ):
                    updated_any = True
                    self.wires[g.output] = g.compute(
                        self.wires[g.a_input], self.wires[g.b_input]
                    )

            if not updated_any:
                break

    def extract_output(self):
        output_keys = [k for k in self.wires.keys() if k.startswith("z")]
        output_keys.sort()

        place = 1
        output = 0
        for i, k in enumerate(output_keys):
            # make sure the outputs are numbered
            assert int(k.removeprefix("z")) == i
            if self.wires[k]:
                output += place
            place *= 2

        return output

    def copy(self) -> "Device":
        return Device(self.wires.copy(), self.gates.copy())

    def fill_x(self, x_value: int):
        self.fill_input("x", x_value)

    def fill_y(self, y_value: int):
        self.fill_input("y", y_value)

    def fill_input(self, input_prefix: str, value: int):
        keys = [k for k in self.wires.keys() if k.startswith(input_prefix)]
        keys.sort()
        max_value = pow(2, len(keys)) - 1
        assert value <= max_value

        place = 1
        for i, k in enumerate(keys):
            # make sure the outputs are numbered
            assert int(k.removeprefix(input_prefix)) == i
            is_bit_active = value >> i & 1 == 1
            self.wires[k] = is_bit_active
            place *= 2


def part_one_answer(lines: list[str]) -> int:
    device = Device.parse(lines)
    device.simulate()
    return device.extract_output()


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day24input")
    print("Part One:", part_one_answer(puzzle_input))
