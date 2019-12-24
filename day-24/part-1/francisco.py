from tool.runners.python import SubmissionPy


import numpy as np


def parse_input(s):
    return np.array(
        [[0 if s == "." else 1 for s in line.strip()] for line in s.strip().split("\n")]
    )


def adjacent_bugs(state):
    bugs = np.zeros_like(state)
    bugs[1:, :] += state[:-1, :]
    bugs[:-1, :] += state[1:, :]
    bugs[:, 1:] += state[:, :-1]
    bugs[:, :-1] += state[:, 1:]
    return bugs


def biodiversity_rating(state):
    rating = 0
    incr = 1
    for i in state.flat:
        rating += i * incr
        incr <<= 1
    return rating


def solve_part1(state):
    history = set([biodiversity_rating(state)])
    while True:
        bugs = adjacent_bugs(state)
        to_zero = (state == 1) * (bugs != 1)
        to_one = (state == 0) * ((bugs == 1) + (bugs == 2))
        state[to_zero] = 0
        state[to_one] = 1
        rating = biodiversity_rating(state)
        if rating in history:
            return rating
        history.add(rating)


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        state = parse_input(s)
        return solve_part1(state)
