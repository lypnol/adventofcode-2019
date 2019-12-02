from typing import List

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        ints = [int(x) for x in s.split(",")]
        ints[1] = 12
        ints[2] = 2
        c = 0
        while ints[c] != 99:
            ints = self.run_opcode(ints, c)
            c = c + 4
        return ints[0]

    def run_opcode(self, l: List[int], c: int) -> List[int]:
        first = l[l[c + 1]]
        second = l[l[c + 2]]
        position = l[c + 3]

        if l[c] == 1:
            res = first + second
        elif l[c] == 2:
            res = first * second
        else:
            raise Exception(f"Opcode not found {l[c]}")

        l[position] = res
        return l
