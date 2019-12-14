from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        deps = {}
        rev_deps = {}
        qty = {"ORE": 1}

        for line in s.strip().split("\n"):
            pins, pout = line.split(" => ")
            qout, eout = pout.split(" ")
            qout = int(qout)

            qty[eout] = qout
            deps[eout] = {}

            for pin in pins.split(", "):
                qin, ein = pin.split(" ")
                qin = int(qin)

                deps[eout][ein] = qin
                if ein not in rev_deps:
                    rev_deps[ein] = []
                rev_deps[ein].append(eout)

        cache = {}

        # Needed REACTIONS!
        def needed(elem):
            if elem == "FUEL":
                return 1
            if elem in cache:
                return cache[elem]

            needed_count = 0
            for relem in rev_deps.get(elem, []):
                needed_count += needed(relem) * deps[relem][elem]

            needed_reac = div_ceil(needed_count, qty[elem])
            cache[elem] = needed_reac
            return needed_reac

        return needed("ORE")


def div_ceil(a, b):
    if a % b == 0:
        return a // b
    return (a // b) + 1
