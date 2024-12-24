from dataclasses import dataclass
import aoc2024.common.input as aoc_input
from .day24 import Device, GateType


@dataclass(frozen=True)
class Anomaly:
    output_bit: int
    wires: tuple[str, ...]
    message: str


def validate_adder_bit(device: Device, bit: int):
    output_wire = "z" + str(bit).rjust(2, "0")
    output_gate = device.gates[output_wire]
    if output_gate.gate_type != GateType.Xor:
        return [
            Anomaly(
                bit,
                (output_wire,),
                f"Should have been an XOR gate, but was {output_gate}",
            )
        ]

    inputs = [output_gate.a_input, output_gate.b_input]
    input_gates = [device.gates[w] for w in inputs]
    half_adder_bit = next((i for i in input_gates if i.gate_type == GateType.Xor), None)
    carry_bit = next((i for i in input_gates if i.gate_type == GateType.Or), None)
    anomalies = list[Anomaly]()
    if half_adder_bit is None:
        anomalies.append(Anomaly(bit, tuple(inputs), "Couldn't find a carry bit (OR)"))
    if carry_bit is None:
        anomalies.append(
            Anomaly(bit, tuple(inputs), "Couldn't find a half-adder bit (XOR)")
        )
    return anomalies
    # TODO: verify the inputs of those gates


def main():
    puzzle_input = aoc_input.load_lines("day24input")
    device = Device.parse(puzzle_input)

    # mermaid diagrams
    with open("day24.mmd", "w", encoding="utf-8") as f:
        f.write("flowchart TD\n")
        for i, gate in enumerate(device.gates.values()):
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

    top_output_bit = max(z for z in device.gates if z.startswith("z"))
    print(f"{top_output_bit=}")
    top_output_bit = int(top_output_bit.removeprefix("z"))
    # ignore the first two bits and final one because they're a little different, mostly because of a lack of carrying
    anomalies = list[Anomaly]()
    for i in range(2, top_output_bit):
        anomalies.extend(validate_adder_bit(device, i))

    if len(anomalies) > 0:
        print("Anomalies found!")
        for a in anomalies:
            print(a)
    else:
        print("No anomalies found! Perfectly functional adder")


if __name__ == "__main__":
    main()
