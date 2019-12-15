import collections
from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        code = [int(i) for i in s.strip().split(",")]

        instructions = self.compute_output(code)
    
        counter = 0
        for i in range(0, len(instructions)-1, 3):
            if instructions[i+2] == 2:
                counter += 1
        
        return counter


    def compute_output(self, code):
        p = collections.defaultdict(int, enumerate(code))
        inputs = []
        pc = 0
        relative_base = 0
        outputs = []

        def index(pos):
            mode = (p[pc] // 10 ** (pos-1+2)) % 10
            if mode == 0:
                return p[pc+pos]
            elif mode == 1:
                return pc+pos
            elif mode == 2:
                return p[pc+pos] + relative_base

        input_index = 0

        while True:
            opcode = p[pc] % 100

            if opcode == 1:
                p[index(3)] = p[index(1)] + p[index(2)]
                pc += 4
            elif opcode == 2:
                p[index(3)] = p[index(1)] * p[index(2)]
                pc += 4
            elif opcode == 3:
                p[index(1)] = inputs[input_index]
                pc += 2
            elif opcode == 4:
                outputs.append(p[index(1)])
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