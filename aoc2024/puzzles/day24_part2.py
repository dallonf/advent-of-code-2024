from dataclasses import dataclass
import aoc2024.common.input as aoc_input
from .day24 import Device, GateType


@dataclass(frozen=True)
class Anomaly:
    output_bit: int
    wires: tuple[str, ...]
    message: str


def validate_carry_bit(device: Device, wire: str, from_bit: int) -> list[Anomaly]:
    anomalies = list[Anomaly]()
    gate = device.gates[wire]
    if gate.gate_type != GateType.Or:
        anomalies.append(Anomaly(from_bit, (wire,), f"Expected OR gate (was {gate})"))
        return anomalies

    def is_first_gate(wire: str):
        test_gate = device.gates[wire]
        return test_gate.gate_type == GateType.And and sorted(
            [test_gate.a_input, test_gate.b_input]
        ) == [wire_name("x", from_bit), wire_name("y", from_bit)]

    second_gate = None
    if is_first_gate(gate.a_input):
        second_gate = device.gates[gate.b_input]
    elif is_first_gate(gate.b_input):
        second_gate = device.gates[gate.a_input]
    else:
        anomalies.append(
            Anomaly(
                from_bit,
                (gate.a_input, gate.b_input),
                f"Couldn't find a required gate in carry structure (expected AND({wire_name("x", from_bit)}, {wire_name("y", from_bit)}))",
            )
        )
        return anomalies

    if second_gate.gate_type != GateType.And:
        anomalies.append(
            Anomaly(
                from_bit,
                (second_gate.output,),
                f"Expected second gate in carry structure to be AND (was {second_gate})",
            )
        )
        return anomalies

    # prev_carry = None

    def is_third_gate(wire: str):
        test_gate = device.gates[wire]
        return test_gate.gate_type == GateType.Xor and sorted(
            [test_gate.a_input, test_gate.b_input]
        ) == [wire_name("x", from_bit), wire_name("y", from_bit)]

    if is_third_gate(second_gate.a_input):
        pass
        # prev_carry = device.gates[gate.b_input]
    elif is_third_gate(second_gate.b_input):
        pass
        # prev_carry = device.gates[gate.a_input]
    else:
        anomalies.append(
            Anomaly(
                from_bit,
                (gate.a_input, gate.b_input),
                f'Couldn\'t find a required gate ("third") in carry structure (expected XOR({wire_name("x", from_bit)}, {wire_name("y", from_bit)}))',
            )
        )
        return anomalies

    return anomalies  # + validate_carry_bit(device, prev_carry.output, from_bit - 1)


def validate_adder_bit(device: Device, bit: int):
    output_wire = wire_name("z", bit)
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
    if carry_bit is None:
        anomalies.append(Anomaly(bit, tuple(inputs), "Couldn't find a carry bit (OR)"))
    else:
        anomalies.extend(validate_carry_bit(device, carry_bit.output, bit - 1))

    if half_adder_bit is None:
        anomalies.append(
            Anomaly(bit, tuple(inputs), "Couldn't find a half-adder bit (XOR)")
        )
    else:
        half_adder_inputs = [half_adder_bit.a_input, half_adder_bit.b_input]
        half_adder_inputs.sort()
        expected_half_adder_inputs = [wire_name("x", bit), wire_name("y", bit)]
        if half_adder_inputs != expected_half_adder_inputs:
            anomalies.append(
                Anomaly(
                    bit,
                    tuple(
                        half_adder_inputs,
                    ),
                    f"Half-adder inputs should have been {expected_half_adder_inputs}",
                )
            )
    return anomalies


def wire_name(prefix: str, bit: int):
    return prefix + str(bit).rjust(2, "0")


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
