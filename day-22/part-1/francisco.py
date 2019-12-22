from tool.runners.python import SubmissionPy


import math
import re

DEAL_INCR, NEW_STACK, CUT = 0, 1, 2
RE = {
    DEAL_INCR: re.compile(r"deal with increment (\d+)"),
    NEW_STACK: re.compile(r"deal into new stack"),
    CUT: re.compile(r"cut (-?\d+)"),
}
ARGS = {DEAL_INCR: 1, NEW_STACK: 0, CUT: 1}


def parse_input(s):
    operations = []
    lines = s.strip().split("\n")
    for line in lines:
        for kind, regex in RE.items():
            m = regex.match(line)
            if m:
                operations.append(
                    (kind,) + tuple(int(m.group(i + 1)) for i in range(0, ARGS[kind]))
                )
                break
    return operations


def apply_operations(deck, operations):
    for operation in operations:
        if operation[0] == NEW_STACK:
            deck = list(reversed(deck))
        elif operation[0] == CUT:
            cut = operation[1]
            deck = deck[cut:] + deck[:cut]
        elif operation[0] == DEAL_INCR:
            incr = operation[1]
            deck_ = [None] * len(deck)
            i = 0
            for card in deck:
                deck_[i] = card
                i = (i + incr) % len(deck)
            deck = deck_
        else:
            assert False
    return deck


def solve_part1(operations, l=10007):
    deck = list(range(l))
    deck = apply_operations(deck, operations)
    return deck.index(2019)


def euclid(a, b):
    if b == 0:
        return (1, 0, a)

    q = a // b
    r = a % b

    x, y, gcd = euclid(b, r)
    return y, x - q * y, gcd


def inverse_modulo(i, p):
    x, y, gcd = euclid(i, p)
    assert gcd == 1, f"i and p not coprimes (i={i} p={p} gcd={gcd})"
    return x


def prev_position(position, length, operation):
    kind = operation[0]
    if kind == NEW_STACK:
        return length - 1 - position
    elif kind == CUT:
        cut = operation[1]
        return (position + cut) % length
    elif kind == DEAL_INCR:
        incr = operation[1]
        return (position * inverse_modulo(incr, length)) % length
    else:
        assert False


def apply_operations_alt(position, length, operations):
    for operation in reversed(operations):
        position = prev_position(position, length, operation)
    return position


def solve_part1_alt(operations, l=10007):
    # This method is slower, but it allowed me to check that my prev_position function
    # was correct.
    deck = list(range(l))
    deck = [apply_operations_alt(position, l, operations) for position in deck]
    return deck.index(2019)


def convert_operation(operation, length):
    kind = operation[0]
    if kind == NEW_STACK:
        return (-1, length - 1)
    elif kind == CUT:
        cut = operation[1]
        return (1, cut)
    elif kind == DEAL_INCR:
        incr = operation[1]
        return (inverse_modulo(incr, length), 0)
    else:
        assert False


def stack_operations(converted_operations, length):
    a, b = 1, 0
    for (a1, b1) in reversed(converted_operations):
        a = (a * a1) % length
        b = (a1 * b + b1) % length
    return a, b


def solve_part1_alt_alt(operations, length=10007):
    # This method is faster than the naive one ! and it allowed me to check that my
    # stack_operations and convert_operation functions were working.
    a, b = stack_operations(
        [convert_operation(operation, length) for operation in operations], length
    )
    deck = list(range(length))
    deck = [(a * p + b) % length for p in deck]
    return deck.index(2019)


def solve_part2(operations, length=119_315_717_514_047, times=101_741_582_076_661):
    position = 2020
    a, b = stack_operations(
        [convert_operation(operation, length) for operation in operations], length
    )

    while times > 0:
        if times & 1 == 1:
            position = (a * position + b) % length
        times >>= 1
        a, b = stack_operations([(a, b)] * 2, length)
    return position


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        operations = parse_input(s)
        return solve_part1_alt_alt(operations)
