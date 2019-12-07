import itertools
from typing import List, Tuple

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        ints = [int(x) for x in s.split(",")]
        max_thruster = 0
        for phases in list(itertools.permutations(list(range(5, 10)))):
            res = self.run_feedback_loop(list(ints), phases)
            if res > max_thruster:
                max_thruster = res
        return max_thruster

    def run_feedback_loop(self, l: List[int], phases: Tuple[int, ...]) -> int:
        amplifiers_inputs = [[phase] for phase in phases]
        amplifiers_inputs[0].append(0)
        amplifiers_softwares = [(list(l), 0, 0) for _ in phases]
        while True:
            for i in range(5):
                amplifiers_softwares[i], amplifier_outputs = self.run_software(
                    amplifiers_softwares[i], amplifiers_inputs[i]
                )
                amplifiers_inputs[(i + 1) % 5] += amplifier_outputs
                if not amplifier_outputs:
                    return amplifiers_inputs[0][-1]

    def run_software(self,
                     state: Tuple[List[int], int, int],
                     inputs: List[int]) -> Tuple[Tuple[List[int], int, int], List[int]]:
        opts = []
        l, c, ipt_c = state
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
                if ipt_c >= len(inputs):
                    return (l, c, ipt_c), opts
                l[l[c + 1]] = inputs[ipt_c]
                ipt_c += 1
                c = c + 2

            elif op_code == 4:
                is_immediate = l[c] // 100 % 10 == 1
                opts.append(l[c + 1] if is_immediate else l[l[c + 1]])
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
        return (l, c, ipt_c), opts
