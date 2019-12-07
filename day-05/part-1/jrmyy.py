from typing import List, Tuple

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        ints = [int(x) for x in s.split(",")]
        c = 0
        opt = 0
        while ints[c] != 99:
            ints, next_cursor, opt = self.run_opcode(ints, c)
            c = next_cursor
        return opt

    def run_opcode(self, l: List[int], c: int) -> Tuple[List[int], int, int]:
        op_code = l[c] % 100
        opt = None

        if op_code == 1 or op_code == 2:
            first = l[l[c + 1]] if l[c] // 100 % 10 == 0 else l[c + 1]
            second = l[l[c + 2]] if l[c] // 1000 % 10 == 0 else l[c + 2]
            position = l[c + 3]
            if op_code == 1:
                res = first + second
            else:
                res = first * second

            l[position] = res
            next_cursor = c + 4

        elif op_code == 3:
            ipt = 1
            l[l[c + 1]] = ipt
            next_cursor = c + 2

        elif op_code == 4:
            is_immediate = l[c] // 100 % 10 == 1
            opt = l[c + 1] if is_immediate else l[l[c + 1]]
            if opt != 0 and l[c + 2] != 99:
                raise Exception(f"Error, output should be 0 but is {opt}")
            next_cursor = c + 2
        else:
            raise Exception(f"Opcode not found {l[c]}")

        return l, next_cursor, opt
