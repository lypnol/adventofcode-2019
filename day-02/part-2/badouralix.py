from collections import defaultdict
from tool.runners.python import SubmissionPy
from typing import List


class BadouralixSubmission(SubmissionPy):
    def __init__(self):
        # Initialize counters
        # Uncomment a few lines in the code below to increment these counters and show stats
        self.index_errors = 0
        self.opcode_errors = 0
        self.opcodes = defaultdict(int)

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Read input
        intcode: List[int] = list(map(int, s.split(",")))

        # Do things
        for noun in range(100):
            for verb in range(100):
                # Patch program
                intcode_copy = intcode.copy()
                intcode_copy[1] = noun
                intcode_copy[2] = verb

                # Run program
                output = self.execute(intcode_copy)

                if output == 19690720:
                    # print(self.index_errors, self.opcode_errors)
                    # print(self.opcodes, self.opcodes[1] < self.opcodes[2])

                    # Return result
                    return 100 * noun + verb

        # Default result
        return -1

    def execute(self, intcode: List[int]) -> int:
        # Setup environment
        instruction_pointer = 0

        # Do things
        while intcode[instruction_pointer] != 99:
            try:
                parameter_one = intcode[instruction_pointer + 1]
                parameter_two = intcode[instruction_pointer + 2]
                parameter_three = intcode[instruction_pointer + 3]

                opcode = intcode[instruction_pointer]
                # self.opcodes[opcode] += 1

                if opcode == 1:
                    new_value = intcode[parameter_one] + intcode[parameter_two]
                elif opcode == 2:
                    new_value = intcode[parameter_one] * intcode[parameter_two]
                else:
                    # self.opcode_errors += 1
                    return -1

                intcode[parameter_three] = new_value

                instruction_pointer += 4
            except IndexError:
                # self.index_errors += 1
                return -1

        # Return result
        return intcode[0]
