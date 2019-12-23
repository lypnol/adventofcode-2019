from tool.runners.python import SubmissionPy


import math
import re
import time

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


def operation_to_affine_transformation(operation, length):
    kind = operation[0]
    if kind == NEW_STACK:
        return (-1, length - 1)
    elif kind == CUT:
        cut = operation[1]
        return (1, -cut)
    elif kind == DEAL_INCR:
        incr = operation[1]
        return (incr, 0)
    else:
        assert False


def merge_affine_transformations(affine_transformations, length):
    a, b = 1, 0
    for (a1, b1) in affine_transformations:
        a = (a * a1) % length
        b = (a1 * b + b1) % length
    return a, b


def solve_part1_alt(operations, length=10007):
    a, b = merge_affine_transformations(
        [
            operation_to_affine_transformation(operation, length)
            for operation in operations
        ],
        length,
    )
    return (a * 2019 + b) % length


def inverse_modulo(i, p):
    x, y, gcd = euclid(i, p)
    assert gcd == 1, f"i and p not coprimes (i={i} p={p} gcd={gcd})"
    return x


def inverse_affine_transformation(a, b, length):
    a_ = inverse_modulo(a, length)
    return a_, (-a_ * b) % length


def solve_part2(operations, length=119_315_717_514_047, times=101_741_582_076_661):
    position = 2020
    a, b = merge_affine_transformations(
        [
            operation_to_affine_transformation(operation, length)
            for operation in operations
        ],
        length,
    )
    a, b = inverse_affine_transformation(a, b, length)

    a_total, b_total = 1, 0

    while times > 0:
        if times & 1 == 1:
            a_total, b_total = merge_affine_transformations(
                [(a, b), (a_total, b_total)], length
            )

        times >>= 1
        a, b = merge_affine_transformations([(a, b)] * 2, length)

    return (a_total * position + b_total) % length


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        operations = parse_input(s)
        return solve_part2(operations)
