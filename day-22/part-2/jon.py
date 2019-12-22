from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        lines = list(s.strip().split("\n"))
        lines.reverse()

        n = 119315717514047

        mult, add = 1, 0

        for l in lines:

            if l.startswith("deal i"):  # deal into new stack
                mult, add = -mult, -1-add
            elif l.startswith("c"):  # cut X
                v = int(l[4:])
                v = -v  # inverse op
                add = add-v
            elif l.startswith("deal w"):  # deal with increment X
                v = int(l[20:])
                v = invert(v, n)  # inverse op
                mult, add = mult*v, add*v
            else:
                raise Exception("unknown instruction")

            mult = mult % n
            add = add % n

        r = 101741582076661
        idx = 2020

        mr = pow(mult, r, n)

        geo_sum = (mr-1) * invert(mult-1, n)

        return (mr*idx + add * geo_sum) % n


def invert(x, n):
    a = n
    b = x % n
    s = 1
    t = 0

    while b != 0:
        q = a // b
        a, b = b, a - q*b
        t, s = s, t - q*s

    if a != 1:
        raise Exception("not invertible")
    return t
