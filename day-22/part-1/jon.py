from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        lines = s.strip().split("\n")

        n = 10007
        cards = list(range(n))

        for l in lines:

            if l.startswith("deal i"):  # deal into new stack
                cards.reverse()
            elif l.startswith("c"):  # cut X
                v = int(l[4:])
                cards = cards[v:] + cards[:v]
            elif l.startswith("deal w"):  # deal with increment X
                v = int(l[20:])
                result = [0]*n
                for i in range(n):
                    result[i*v % n] = cards[i]
                cards = result
            else:
                raise Exception("unknown instruction")

        return cards.index(2019)
