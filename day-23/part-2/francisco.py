from tool.runners.python import SubmissionPy


from copy import deepcopy
from collections import defaultdict, deque


class IntCodeVM:
    VAL, PTR = 0, 1  # arg modes: value / pointer

    INSTRS = {
        1: ("plus", (VAL, VAL, PTR)),
        2: ("mul", (VAL, VAL, PTR)),
        3: ("input", (PTR,)),
        4: ("output", (VAL,)),
        5: ("jump_if_true", (VAL, VAL)),
        6: ("jump_if_false", (VAL, VAL)),
        7: ("less_than", (VAL, VAL, PTR)),
        8: ("equals", (VAL, VAL, PTR)),
        9: ("relative_base_incr", (VAL,)),
    }

    def __init__(self, program):
        self.memory = defaultdict(int, {i: elem for i, elem in enumerate(program)})
        self.instr_ptr = 0
        self.relative_base = 0
        self.blocked_stdin = False
        self.stdin = deque()
        self.stdout = deque()

    def copy(self):
        return deepcopy(self)

    @property
    def stopped(self):
        return self.memory[self.instr_ptr] == 99

    def arg(self, n, arg_type, arg_mode):
        assert arg_type in [self.VAL, self.PTR]
        assert arg_mode in [0, 1, 2] if arg_type == self.VAL else [0, 2]

        if arg_mode == 0:
            ptr = self.memory[self.instr_ptr + 1 + n]
        elif arg_mode == 1:
            ptr = self.instr_ptr + 1 + n
        elif arg_mode == 2:
            ptr = self.memory[self.instr_ptr + 1 + n] + self.relative_base
        else:
            raise Exception(f"Unknown arg mode: {mode}")

        return ptr if arg_type == self.PTR else self.memory[ptr]

    @classmethod
    def parse_instr(cls, instr):
        opcode = instr % 100
        instr //= 100
        args_types = cls.INSTRS[opcode][1]
        modes = []

        for _ in range(len(args_types)):
            modes.append(instr % 10)
            instr //= 10

        return opcode, modes

    def run(self):
        while not self.stopped:
            opcode, modes = self.parse_instr(self.memory[self.instr_ptr])
            instr_name, arg_types = self.INSTRS[opcode]

            args = [
                self.arg(n, arg_type, arg_mode)
                for n, (arg_type, arg_mode) in enumerate(zip(arg_types, modes))
            ]

            getattr(self, f"op_{instr_name}")(args)  # self.op_XXX(args)

            if self.blocked_stdin:
                return

    def op_plus(self, args):
        self.memory[args[2]] = args[0] + args[1]
        self.instr_ptr += len(args) + 1

    def op_mul(self, args):
        self.memory[args[2]] = args[0] * args[1]
        self.instr_ptr += len(args) + 1

    def op_input(self, args):
        if self.stdin:
            self.memory[args[0]] = self.stdin.popleft()
            self.instr_ptr += len(args) + 1
            self.blocked_stdin = False
        else:
            self.blocked_stdin = True

    def op_output(self, args):
        self.stdout.append(args[0])
        self.instr_ptr += len(args) + 1

    def op_jump_if_true(self, args):
        if args[0] != 0:
            self.instr_ptr = args[1]
        else:
            self.instr_ptr += len(args) + 1

    def op_jump_if_false(self, args):
        if args[0] == 0:
            self.instr_ptr = args[1]
        else:
            self.instr_ptr += len(args) + 1

    def op_less_than(self, args):
        self.memory[args[2]] = 1 if args[0] < args[1] else 0
        self.instr_ptr += len(args) + 1

    def op_equals(self, args):
        self.memory[args[2]] = 1 if args[0] == args[1] else 0
        self.instr_ptr += len(args) + 1

    def op_relative_base_incr(self, args):
        self.relative_base += args[0]
        self.instr_ptr += len(args) + 1


def solve_part2(program):
    n = 50
    vms = [IntCodeVM(program) for _ in range(50)]

    for i, vm in enumerate(vms):
        vm.stdin.append(i)

    X_nat, Y_nat = None, None  # next values to be delivered by the NAT
    Y_delivered = None  # last Y value delivered by the NAT

    while True:
        idle = True

        for i, vm in enumerate(vms):
            assert vm.stopped == False

            if vm.blocked_stdin and not vm.stdin:
                vm.stdin.append(-1)
            else:
                idle = False

            vm.run()
            assert len(vm.stdout) % 3 == 0

            if vm.stdout:
                idle = False

            while vm.stdout:
                dest, X, Y = (vm.stdout.popleft() for _ in range(3))
                if dest == 255:
                    X_nat, Y_nat = X, Y
                else:
                    vms[dest].stdin.extend([X, Y])

        if idle:
            if Y_delivered is not None and Y_delivered == Y_nat:
                return Y_delivered
            Y_delivered = Y_nat
            vms[0].stdin.extend([X_nat, Y_nat])


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part2(program)
