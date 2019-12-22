from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        N_CARDS = 10_007
        INTERESTING_CARD = 2019

        return solve_part1(N_CARDS, s.splitlines(), INTERESTING_CARD)


def solve_part1(n_cards, actions, card):
    a, b = shuffle(n_cards, actions)
    return (a * card + b) % n_cards


def shuffle(n_cards, actions):
    """ Return (a, b) such that for any card,
    shuffled_position  = (a * initial_position + b) % n_cards """
    a, b = 1, 0
    for action in actions:
        if action.startswith("deal with increment"):
            n = int(action.split()[-1])
            a *= n
            b *= n
        elif action == "deal into new stack":
            a *= -1
            b = -b - 1
        elif action.startswith("cut"):
            n = int(action.split()[-1])
            b -= n
        else:
            raise ValueError("Unknown action:", action)

    # Simplify a and b
    a %= n_cards
    b %= n_cards

    return a, b
