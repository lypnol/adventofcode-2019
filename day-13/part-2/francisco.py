from tool.runners.python import SubmissionPy

from collections import defaultdict


# XXX: this code should be refactored, but it works and it's not too fun to make
# it look better so I'm not gonna do it

# XXX: this is really ugly, the program should be a class with its own state
def execute(state, input_):
    program, i, j, relative_base = state
    output = []
    while program[i] != 99:
        opcode = program[i] % 100

        modes = {
            1: (program[i] // 100) % 10,
            2: (program[i] // 1000) % 10,
            3: (program[i] // 10000) % 10,
        }

        def param(n):
            if modes[n] == 0:
                return program[program[i + n]]
            elif modes[n] == 1:
                return program[i + n]
            elif modes[n] == 2:
                return program[program[i + n] + relative_base]
            else:
                raise f"Invalid param mode: {modes[n]}"

        def param_addr(n):
            if modes[n] == 0:
                return program[i + n]
            elif modes[n] == 2:
                return program[i + n] + relative_base
            else:
                raise f"Invalid param mode: {modes[n]}"

        if opcode == 1:  # plus
            program[param_addr(3)] = param(1) + param(2)
            i += 4
        elif opcode == 2:  # mul
            program[param_addr(3)] = param(1) * param(2)
            i += 4
        elif opcode == 3:  # input
            # no more inputs: exit at current state
            if j >= len(input_):
                return (program, i, 0, relative_base), output, False
            program[param_addr(1)] = input_[j]
            j += 1
            i += 2
        elif opcode == 4:  # output
            output.append(param(1))
            i += 2
        elif opcode == 5:  # jump if true
            if param(1) != 0:
                i = param(2)
            else:
                i += 3
        elif opcode == 6:  #  jump if false
            if param(1) == 0:
                i = param(2)
            else:
                i += 3
        elif opcode == 7:  # less than
            program[param_addr(3)] = 1 if param(1) < param(2) else 0
            i += 4
        elif opcode == 8:  # equals
            program[param_addr(3)] = 1 if param(1) == param(2) else 0
            i += 4
        elif opcode == 9:  # relative base update
            relative_base += param(1)
            i += 2
        else:
            raise f"Invalid opcode: {opcode}"

    return (program, i, 0, relative_base), output, True


def update_display(display, output, score=None, ball=None, paddle=None):
    for i in range(0, len(output), 3):
        (X, Y, Z) = output[i : i + 3]
        if X == -1 and Y == 0:
            score = Z
        else:
            display[(Y, X)] = Z
            if Z == 4:
                ball = X
            elif Z == 3:
                paddle = X
    return score, ball, paddle


def show_display(display):
    min_X, max_X = min(e[1] for e in display), max(e[1] for e in display)
    min_Y, max_Y = min(e[0] for e in display), max(e[0] for e in display)

    d = {0: " ", 1: "X", 2: "#", 3: "-", 4: "."}

    return "\n".join(
        "".join(d[display[(Y, X)]] for X in range(min_X, max_X + 1))
        for Y in range(min_Y, max_Y + 1)
    )


def count_blocks(display):
    return sum(1 for (Y, X) in display if display[(Y, X)] == 2)


def solve_part2(program, verbose=False):
    memory = defaultdict(lambda: 0, {i: e for i, e in enumerate(program)})
    memory[0] = 2

    state = memory, 0, 0, 0
    state, output, stop = execute(state, [])

    display = defaultdict(lambda: 0)
    score, ball, paddle = update_display(display, output)

    while stop != True:
        state, output, stop = execute(
            state, [1 if ball > paddle else -1 if ball < paddle else 0]
        )
        # XXX: ugly
        score, ball, paddle = update_display(display, output, score, ball, paddle)
        if verbose:
            print(score, ball, paddle, count_blocks(display))
            print(show_display(display))

    return score


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part2(program)
