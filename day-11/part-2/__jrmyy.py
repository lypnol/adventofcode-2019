from typing import Tuple, Dict, List

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> None:
        # :param s: input in string format
        # :return: solution flag
        ints = [int(x) for x in s.split(",")] + [0] * 10000
        c = 0
        relative_base = 0
        ipt = 1
        current_position = (0, 0)
        painted_panels = {}
        current_direction = "up"
        color = None
        move = None
        while ints[c] != 99:
            ints, c, relative_base, opt = self._run_opcode(ints, ipt, c, relative_base)
            if opt is not None:
                if color is None:
                    color = opt
                else:
                    move = opt
            if color is not None and move is not None:
                current_position, current_direction, painted_panels = self._paint_panel(
                    current_position, current_direction, painted_panels, color, move
                )
                color = None
                move = None
            ipt = painted_panels.get(current_position, [0])[-1]
        recenter_x = max(abs(min([x[0] for x in painted_panels.keys()])), 0)
        recenter_y = max(abs(min([x[1] for x in painted_panels.keys()])), 0)
        normalized_painted_panels = {}
        for key in painted_panels:
            normalized_painted_panels[(key[0] + recenter_x, key[1] + recenter_y)] = painted_panels[key]

        max_x = max([x[0] for x in normalized_painted_panels])
        max_y = max([x[1] for x in normalized_painted_panels])

        out = ""

        for j in range(5, -1, -1):
            for i in range(40):
                if normalized_painted_panels.get((i, j), []) == [1]:
                    out += '1'
                else:
                    out += '0'

        print(out)
        return out

    def _paint_panel(self,
                     current_position: Tuple[int, int],
                     current_direction: str,
                     painted_panels: Dict[Tuple[int, int], List[int]],
                     color: int,
                     move: int) -> Tuple[Tuple[int, int], str, Dict[Tuple[int, int], List[int]]]:
        if current_position in painted_panels:
            painted_panels[current_position].append(color)
        else:
            painted_panels[current_position] = [color]
        if move == 0:
            if current_direction == "up":
                current_position = (current_position[0] - 1, current_position[1])
                current_direction = "left"
            elif current_direction == "left":
                current_position = (current_position[0], current_position[1] - 1)
                current_direction = "down"
            elif current_direction == "down":
                current_position = (current_position[0] + 1, current_position[1])
                current_direction = "right"
            elif current_direction == "right":
                current_position = (current_position[0], current_position[1] + 1)
                current_direction = "up"
        elif move == 1:
            if current_direction == "up":
                current_position = (current_position[0] + 1, current_position[1])
                current_direction = "right"
            elif current_direction == "right":
                current_position = (current_position[0], current_position[1] - 1)
                current_direction = "down"
            elif current_direction == "down":
                current_position = (current_position[0] - 1, current_position[1])
                current_direction = "left"
            elif current_direction == "left":
                current_position = (current_position[0], current_position[1] + 1)
                current_direction = "up"
        else:
            raise Exception(f"Wrong move : {move}")
        return current_position, current_direction, painted_panels

    def _run_opcode(self, l: List[int], ipt: int, c: int, relative_base: int) -> Tuple[List[int], int, int, int]:
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
