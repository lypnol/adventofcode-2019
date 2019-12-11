from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        code = [int(i) for i in s.strip().split(",")]
        return self.compute_output(code, [1])

    def compute_output(self, code, inputs):
        mem = {}
        pc = 0
        relative_base = 0

        def p(i): # add support for larger memory than code size
            return mem[i] if i in mem else code[i]

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
        output_value = None

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
                input_index += 1
                pc += 2
            elif opcode == 4:
                output_value = param(1)
                pc += 2
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
                return output_value