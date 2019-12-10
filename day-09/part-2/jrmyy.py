from typing import List, Tuple

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        ints = [int(x) for x in s.split(",")] + [0] * 10000
        c = 0
        opt = 0
        relative_base = 0
        while ints[c] != 99:
            ints, c, relative_base, opt = self._run_opcode(ints, c, relative_base)
        return opt

    def _run_opcode(self, l: List[int], c: int, relative_base: int) -> Tuple[List[int], int, int, int]:
        op_code = l[c] % 100
        opt = None

        if op_code == 1 or op_code == 2:
            first = self._get_first_element(l, c, relative_base)
            second = self._get_second_element(l, c, relative_base)
            position = self._get_position(l, c, relative_base)
            if op_code == 1:
                res = first + second
            else:
                res = first * second

            l[position] = res
            next_cursor = c + 4

        elif op_code == 3:
            ipt = 2
            position = self._get_ipt_position(l, c, relative_base)
            l[position] = ipt
            next_cursor = c + 2

        elif op_code == 4:
            position = self._get_opt_position(l, c, relative_base)
            opt = l[position]
            next_cursor = c + 2

        elif op_code == 5 or op_code == 6:
            first = self._get_first_element(l, c, relative_base)
            second = self._get_second_element(l, c, relative_base)
            if op_code == 5:
                next_cursor = second if first != 0 else c + 3
            else:
                next_cursor = second if first == 0 else c + 3
        elif op_code == 7 or op_code == 8:
            first = self._get_first_element(l, c, relative_base)
            second = self._get_second_element(l, c, relative_base)
            position = self._get_position(l, c, relative_base)
            if op_code == 7:
                res = int(first < second)
            else:
                res = int(first == second)
            l[position] = res
            next_cursor = c + 4
        elif op_code == 9:
            position = self._get_opt_position(l, c, relative_base)
            relative_base += l[position]
            next_cursor = c + 2
        else:
            raise Exception(f"Opcode not found {l[c]}")

        return l, next_cursor, relative_base, opt

    def _get_first_element(self, l: List[int], idx: int, relative_base: int) -> int:
        el_type = l[idx] // 100 % 10
        if el_type == 0:
            return l[l[idx + 1]]
        elif el_type == 1:
            return l[idx + 1]
        elif el_type == 2:
            return l[l[idx + 1] + relative_base]
        raise Exception(f"{el_type} not recognized")

    def _get_second_element(self, l: List[int], idx: int, relative_base: int) -> int:
        el_type = l[idx] // 1000 % 10
        if el_type == 0:
            return l[l[idx + 2]]
        elif el_type == 1:
            return l[idx + 2]
        elif el_type == 2:
            return l[l[idx + 2] + relative_base]
        raise Exception(f"{el_type} not recognized")

    def _get_position(self, l: List[int], idx: int, relative_base: int) -> int:
        el_type = l[idx] // 10000 % 10
        if el_type == 0:
            return l[idx + 3]
        elif el_type == 2:
            return l[idx + 3] + relative_base
        raise Exception(f"{el_type} not recognized")

    def _get_ipt_position(self, l: List[int], idx: int, relative_base: int) -> int:
        el_type = l[idx] // 100 % 10
        if el_type == 0:
            return l[idx + 1]
        elif el_type == 2:
            return l[idx + 1] + relative_base
        raise Exception(f"{el_type} not recognized")

    def _get_opt_position(self, l: List[int], idx: int, relative_base: int) -> int:
        el_type = l[idx] // 100 % 10
        if el_type == 0:
            return l[idx + 1]
        elif el_type == 1:
            return idx + 1
        elif el_type == 2:
            return l[idx + 1] + relative_base
        raise Exception(f"{el_type} not recognized")
