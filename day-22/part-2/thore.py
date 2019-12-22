from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        N_CARDS = 119315717514047
        N_REPEATS = 101741582076661
        INTERESTING_CARD = 2020

        return solve_part2(N_CARDS, s.splitlines(), INTERESTING_CARD, N_REPEATS)


def solve_part2(n_cards, actions, position, n_repeats):
    a, b = shuffle(n_cards, actions)

    # shuffled_position  = (a * initial_position + b) % n_cards
    # initial_position = (a^{-1} * shuffled_position - a^{-1} * b) % n_cards
    #                   = a' * shuffled_position + b'
    a_inv = modular_inverse(a, n_cards)
    a, b = a_inv, -a_inv * b

    # u_n = initial position of card at position 'position' after n shufflings
    # u_{n+1} = (a * u_n + b) % n_cards
    # u_n = (a^n * u_0 + b * (1 + a^1 + ... + a^{n-1})) % n_cards
    #     = ((a^n % n_cards) * u_0 + b * modular_geometric_sum(a, n, n_cards)) % n_cards
    res = (
        pow(a, n_repeats, n_cards) * position
        + b * modular_geometric_sum(a, n_repeats, n_cards)
    ) % n_cards
    return res


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


def modular_inverse(a, mod):
    """ Compute modular inverse using Extended Euclidean algorithm """
    r_prev, u_prev, v_prev, r, u, v = a, 1, 0, mod, 0, 1
    while r != 0:
        q = r_prev // r
        r_prev, u_prev, v_prev, r, u, v = (
            r,
            u,
            v,
            r_prev - q * r,
            u_prev - q * u,
            v_prev - q * v,
        )
    return u_prev


def modular_geometric_sum(x, n, mod):
    """ Compute a_n = (1 + a^1 + ... + a^{n-1}) % mod 
    using that 
        a_{2n} = ((x_n + 1) * a_n) % mod
        a_{2n+1} = (x^{2n} + a_{2n}) % mod
    """
    if n == 1:
        return 1 % mod
    elif n % 2 == 0:
        return ((pow(x, n // 2, mod) + 1) * modular_geometric_sum(x, n // 2, mod)) % mod
    else:
        return (pow(x, n - 1, mod) + modular_geometric_sum(x, n - 1, mod)) % mod
