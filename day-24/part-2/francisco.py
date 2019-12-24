from tool.runners.python import SubmissionPy


import numpy as np


def parse_input(s):
    return np.array(
        [[0 if s == "." else 1 for s in line.strip()] for line in s.strip().split("\n")]
    )


def adjacent_bugs_2(state):
    bugs = np.zeros_like(state)
    # almost a copy-paste from adjacent_bugs
    bugs[:, 1:, :] += state[:, :-1, :]
    bugs[:, :-1, :] += state[:, 1:, :]
    bugs[:, :, 1:] += state[:, :, :-1]
    bugs[:, :, :-1] += state[:, :, 1:]
    bugs[:, 2, 2] = 0  # center cannot become a bug

    # level recursion
    bugs[1:, :, 0] += state[:-1, 2, 1].reshape(-1, 1)
    bugs[1:, :, 4] += state[:-1, 2, 3].reshape(-1, 1)
    bugs[1:, 0, :] += state[:-1, 1, 2].reshape(-1, 1)
    bugs[1:, 4, :] += state[:-1, 3, 2].reshape(-1, 1)
    bugs[:-1, 2, 1] += state[1:, :, 0].sum(axis=1)
    bugs[:-1, 2, 3] += state[1:, :, 4].sum(axis=1)
    bugs[:-1, 1, 2] += state[1:, 0, :].sum(axis=1)
    bugs[:-1, 3, 2] += state[1:, 4, :].sum(axis=1)

    return bugs


def solve_part2(state, minutes=200):
    state = state.reshape(-1, 5, 5)
    state = np.vstack(
        [np.zeros_like(state) for _ in range(minutes // 2)]
        + [state]
        + [np.zeros_like(state) for _ in range(minutes // 2)]
    )

    for _ in range(minutes):
        bugs = adjacent_bugs_2(state)
        to_zero = (state == 1) * (bugs != 1)
        to_one = (state == 0) * ((bugs == 1) + (bugs == 2))
        state[to_zero] = 0
        state[to_one] = 1

    return state.sum()


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        state = parse_input(s)
        return solve_part2(state)
