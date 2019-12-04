from tool.runners.python import SubmissionPy
from typing import List


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Read input
        intcode: List[int] = list(map(int, s.split(",")))

        # Patch program
        intcode[1] = 12
        intcode[2] = 2

        # Run program
        self.execute(intcode)

        # Return result
        return intcode[0]

    def execute(self, intcode: List[int]) -> None:
        # Setup environment
        current_index = 0

        # Do things
        while intcode[current_index] != 99:
            if (intcode[current_index] != 1) and (intcode[current_index] != 2):
                return

            index_one = intcode[current_index + 1]
            index_two = intcode[current_index + 2]
            index_three = intcode[current_index + 3]

            if intcode[current_index] == 1:
                new_value = intcode[index_one] + intcode[index_two]
            else:
                new_value = intcode[index_one] * intcode[index_two]

            intcode[index_three] = new_value

            current_index += 4
