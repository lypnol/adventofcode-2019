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
            "05": (3, self.opcode_05),
            "06": (3, self.opcode_06),
            "07": (4, self.opcode_07),
            "08": (4, self.opcode_08),
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

        # Tweak modes
        # For instance, instruction = "1002" -> " " + "01" + "0"
        if len(instruction) == 1:
            modes = " " + "0" * (argc - 1)
        else:
            modes = " " + instruction[:-2][::-1] + "0" * (len(instruction) - 2)

        # Do stuff
        # print(self.ip, instruction, opcode, modes)
        value = handler(modes)
        # print(value, self.outputs, self.ip, self.intcode)

        # Return
        return True

    def get_value(self, address: int, mode: str) -> int:
        if mode == "0":
            address = self.intcode[address]

        return self.intcode[address]

    def opcode_01(self, modes: str) -> int:
        # Read parameters
        value_1 = self.get_value(self.ip + 1, modes[1])
        value_2 = self.get_value(self.ip + 2, modes[2])

        value = value_1 + value_2

        # At this point, the parameter 3 is in position mode
        address = self.intcode[self.ip + 3]
        self.intcode[address] = value

        # Update instruction pointer
        self.ip += 4

        # Return value
        return value

    def opcode_02(self, modes: str) -> int:
        # Read parameters
        value_1 = self.get_value(self.ip + 1, modes[1])
        value_2 = self.get_value(self.ip + 2, modes[2])

        value = value_1 * value_2

        # At this point, the parameter 3 is in position mode
        address = self.intcode[self.ip + 3]
        self.intcode[address] = value

        # Update instruction pointer
        self.ip += 4

        # Return value
        return value

    def opcode_03(self, modes: str) -> int:
        value = self.inputs[self.input_pointer]
        self.input_pointer += 1

        # At this point, the parameter 0 is in position mode
        address = self.intcode[self.ip + 1]
        self.intcode[address] = value

        # Update instruction pointer
        self.ip += 2

        # Return value
        return value

    def opcode_04(self, modes: str) -> int:
        # Read parameters
        value = self.get_value(self.ip + 1, modes[1])

        self.outputs.append(value)

        # Update instruction pointer
        self.ip += 2

        # Return value
        return value

    def opcode_05(self, modes: str) -> None:
        # Read parameters
        value_1 = self.get_value(self.ip + 1, modes[1])
        value_2 = self.get_value(self.ip + 2, modes[2])

        if value_1 != 0:
            self.ip = value_2
            return

        # Update instruction pointer
        self.ip += 3

    def opcode_06(self, modes: str) -> None:
        # Read parameters
        value_1 = self.get_value(self.ip + 1, modes[1])
        value_2 = self.get_value(self.ip + 2, modes[2])

        if value_1 == 0:
            self.ip = value_2
            return

        # Update instruction pointer
        self.ip += 3

    def opcode_07(self, modes: str) -> int:
        # Read parameters
        value_1 = self.get_value(self.ip + 1, modes[1])
        value_2 = self.get_value(self.ip + 2, modes[2])

        if value_1 < value_2:
            value = 1
        else:
            value = 0

        # At this point, the parameter 3 is in position mode
        address = self.intcode[self.ip + 3]
        self.intcode[address] = value

        # Update instruction pointer
        self.ip += 4

        # Return value
        return value

    def opcode_08(self, modes: str) -> int:
        # Read parameters
        value_1 = self.get_value(self.ip + 1, modes[1])
        value_2 = self.get_value(self.ip + 2, modes[2])

        if value_1 == value_2:
            value = 1
        else:
            value = 0

        # At this point, the parameter 3 is in position mode
        address = self.intcode[self.ip + 3]
        self.intcode[address] = value

        # Update instruction pointer
        self.ip += 4

        # Return value
        return value


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Read input
        intcode = list(map(int, s.strip().split(",")))
        inputs = [5]

        # Build machine
        machine = BadouralixMachine(intcode, inputs)

        # Run program
        output = machine.run()

        # Return result
        return output[-1]
