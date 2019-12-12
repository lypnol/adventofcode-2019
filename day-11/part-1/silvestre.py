from collections import defaultdict
from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    @staticmethod
    def move(current_pos, direction):
        x, y = current_pos
        if direction == "up":
            return x,y+1
        elif direction == "right":
            return x+1,y
        elif direction == "down":
            return x,y-1
        elif direction == "left":
            return x-1,y

    def run(self, s):
        code = [int(i) for i in s.strip().split(",")]
        
        is_finished = False
        mem = defaultdict(int)
        pc = 0
        relative_base = 0
        
        grid = {}
        current_pos = (0,0)
        directions = ["up", "right", "down", "left"]
        current_dir_idx = 0
    
        while True:
            color = grid[current_pos] if current_pos in grid else 0
            color, pc, relative_base, is_finished = self.compute_output(code, [color], mem, pc, relative_base)
            if is_finished:
                break
            grid[current_pos] = color
            instr, pc, relative_base, is_finished = self.compute_output(code, [color], mem, pc, relative_base)
            if is_finished:
                break
            current_dir_idx = (current_dir_idx + 1) % 4 if instr else (current_dir_idx - 1) % 4
            current_pos = self.move(current_pos, directions[current_dir_idx])
        
        return len(grid)


    def compute_output(self, code, inputs, mem, pc, relative_base):

        def p(i):
            return mem[i] if (i in mem) or (i >= len(code)) else code[i]

        def index(pos):
            mode = (p(pc) // 10 ** (pos-1+2)) % 10
            if mode == 0:
                return p(pc+pos)
            elif mode == 1:
                return pc+pos
            elif mode == 2:
                return p(pc+pos) + relative_base

        def param(pos):
            return p(index(pos))

        input_index = 0

        while True:
            opcode = p(pc) % 100

            if opcode == 1:
                mem[index(3)] = param(1) + param(2)
                pc += 4
            elif opcode == 2:
                mem[index(3)] = param(1) * param(2)
                pc += 4
            elif opcode == 3:
                mem[index(1)] = inputs[input_index]
                pc += 2
            elif opcode == 4:
                return param(1), pc+2, relative_base, False
            elif opcode == 5:
                pc = param(2) if param(1) != 0 else pc+3
            elif opcode == 6:
                pc = param(2) if param(1) == 0 else pc+3
            elif opcode == 7:
                mem[index(3)] = int(param(1) < param(2))
                pc += 4
            elif opcode == 8:
                mem[index(3)] = int(param(1) == param(2))
                pc += 4
            elif opcode == 9:
                relative_base += param(1)
                pc += 2
            elif opcode == 99:
                return None, None, None, True