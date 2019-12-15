import collections
from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        code = [int(i) for i in s.strip().split(",")]
        code[0] = 2

        instructions = self.compute_output(code)
    
        score = -1
        for i in range(0, len(instructions)-1, 3):
            if instructions[i] == -1 and instructions[i+1] == 0:
                score = instructions[i+2]
        
        return score


    def compute_output(self, code):
        p = collections.defaultdict(int, enumerate(code))
        pc = 0
        relative_base = 0

        outputs = []

        ball_x = None
        paddle_x = None

        def index(pos):
            mode = (p[pc] // 10 ** (pos-1+2)) % 10
            if mode == 0:
                return p[pc+pos]
            elif mode == 1:
                return pc+pos
            elif mode == 2:
                return p[pc+pos] + relative_base

        while True:
            opcode = p[pc] % 100

            if opcode == 1:
                p[index(3)] = p[index(1)] + p[index(2)]
                pc += 4
            elif opcode == 2:
                p[index(3)] = p[index(1)] * p[index(2)]
                pc += 4
            elif opcode == 3:
                p[index(1)] = -1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0
                pc += 2
            elif opcode == 4:
                outputs.append(p[index(1)])

                if len(outputs) % 3 == 0:
                    if outputs[-1] == 4:
                        ball_x = outputs[-3]
                    elif outputs[-1] == 3:
                        paddle_x = outputs[-3]

                pc += 2
            elif opcode == 5:
                pc = p[index(2)] if p[index(1)] != 0 else pc+3
            elif opcode == 6:
                pc = p[index(2)] if p[index(1)] == 0 else pc+3
            elif opcode == 7:
                p[index(3)] = int(p[index(1)] < p[index(2)])
                pc += 4
            elif opcode == 8:
                p[index(3)] = int(p[index(1)] == p[index(2)])
                pc += 4
            elif opcode == 9:
                relative_base += p[index(1)]
                pc += 2
            elif opcode == 99:
                return outputs