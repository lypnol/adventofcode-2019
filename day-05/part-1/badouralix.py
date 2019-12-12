from tool.runners.python import SubmissionPy
from typing import List


class BadouralixMachine:
    def __init__(self, intcode: List[int], inputs: List[int]):
        # Setup environment
        self.intcode = intcode
        self.inputs = inputs
        self.outputs: List[int] = []

        # Setup interpreter
        self.input_pointer = 0
        self.ip = 0
        self.opcodes = {
            "01": (4, self.opcode_01),
            "02": (4, self.opcode_02),
            "03": (2, self.opcode_03),
            "04": (2, self.opcode_04),
        }

    def run(self) -> List[int]:
        while self.run_cycle():
            pass

        return self.outputs

    def run_cycle(self) -> bool:
        # Read instruction as a string because it's easier to manipulate
        address = self.ip
        instruction = str(self.intcode[address])

        # Parse instruction
        # For instance, instruction = "1002" -> "02"
        if len(instruction) == 1:
            opcode = "0" + instruction
        else:
            opcode = instruction[-2:]

        # Exit on halt
        if opcode == "99":
            return False

        # Build call state
        argc, handler = self.opcodes[opcode]
        argv = self.intcode[address : address + argc]

        # Tweak modes
        # For instance, instruction = "1002" -> " " + "01" + "0"
        if len(instruction) == 1:
            modes = " " + "0" * (argc - 1)
        else:
            modes = " " + instruction[:-2][::-1] + "0" * (len(instruction) - 2)

        # Do stuff
        value = handler(argv, modes)
        # print(opcode, argv, modes, value, self.outputs)

        # Update state
        self.ip += argc

        # Return
        return True

    def opcode_01(self, argv: List[int], modes: str) -> int:
        if modes[1] == "0":
            address_1 = argv[1]
            value_1 = self.intcode[address_1]
        else:
            value_1 = argv[1]

        if modes[2] == "0":
            address_2 = argv[2]
            value_2 = self.intcode[address_2]
        else:
            value_2 = argv[2]

        value = value_1 + value_2

        # At this point, the parameter 3 is in position mode
        address = argv[3]
        self.intcode[address] = value

        # Return value
        return value

    def opcode_02(self, argv: List[int], modes: str) -> int:
        if modes[1] == "0":
            address_1 = argv[1]
            value_1 = self.intcode[address_1]
        else:
            value_1 = argv[1]

        if modes[2] == "0":
            address_2 = argv[2]
            value_2 = self.intcode[address_2]
        else:
            value_2 = argv[2]

        value = value_1 * value_2

        # At this point, the parameter 3 is in position mode
        address = argv[3]
        self.intcode[address] = value

        # Return value
        return value

    def opcode_03(self, argv: List[int], modes: str) -> int:
        value = self.inputs[self.input_pointer]
        self.input_pointer += 1

        # At this point, the parameter 0 is in position mode
        address = argv[1]
        self.intcode[address] = value

        # Return value
        return value

    def opcode_04(self, argv: List[int], modes: str) -> int:
        if modes[1] == "0":
            address = argv[1]
            value = self.intcode[address]
        else:
            value = argv[1]

        self.outputs.append(value)

        # Return value
        return value


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Read input
        intcode = list(map(int, s.strip().split(",")))
        inputs = [1]

        # Build machine
        machine = BadouralixMachine(intcode, inputs)

        # Run program
        output = machine.run()

        # Return result
        return output[-1]
