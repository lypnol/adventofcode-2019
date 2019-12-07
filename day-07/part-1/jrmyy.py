import itertools
from typing import List

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        ints = [int(x) for x in s.split(",")]
        max_thruster = 0
        for a, b, c, d, e in list(itertools.permutations(list(range(5)))):
            opt_a = self.run_software(list(ints), a, 0)
            opt_b = self.run_software(list(ints), b, opt_a)
            opt_c = self.run_software(list(ints), c, opt_b)
            opt_d = self.run_software(list(ints), d, opt_c)
            final_opt = self.run_software(list(ints), e, opt_d)
            if final_opt > max_thruster:
                max_thruster = final_opt
        return max_thruster

    def run_software(self, l: List[int], phase_setting: int, ipt: int) -> int:
        c = 0
        opt = 0
        num_input_ops = 0
        while l[c] != 99:
            op_code = l[c] % 100

            if op_code == 1 or op_code == 2:
                first = l[l[c + 1]] if l[c] // 100 % 10 == 0 else l[c + 1]
                second = l[l[c + 2]] if l[c] // 1000 % 10 == 0 else l[c + 2]
                position = l[c + 3]
                if op_code == 1:
                    res = first + second
                else:
                    res = first * second

                l[position] = res
                c = c + 4

            elif op_code == 3:
                if num_input_ops == 0:
                    l[l[c + 1]] = phase_setting
                elif num_input_ops == 1:
                    l[l[c + 1]] = ipt
                else:
                    raise Exception("Too many inputs")
                num_input_ops += 1
                c = c + 2

            elif op_code == 4:
                is_immediate = l[c] // 100 % 10 == 1
                opt = l[c + 1] if is_immediate else l[l[c + 1]]
                c = c + 2

            elif op_code == 5 or op_code == 6:
                first = l[l[c + 1]] if l[c] // 100 % 10 == 0 else l[c + 1]
                second = l[l[c + 2]] if l[c] // 1000 % 10 == 0 else l[c + 2]
                if op_code == 5:
                    c = second if first != 0 else c + 3
                else:
                    c = second if first == 0 else c + 3

            elif op_code == 7 or op_code == 8:
                first = l[l[c + 1]] if l[c] // 100 % 10 == 0 else l[c + 1]
                second = l[l[c + 2]] if l[c] // 1000 % 10 == 0 else l[c + 2]
                position = l[c + 3]
                if op_code == 7:
                    res = int(first < second)
                else:
                    res = int(first == second)
                l[position] = res
                c = c + 4
            else:
                raise Exception(f"Opcode not found {l[c]}")
        return opt
