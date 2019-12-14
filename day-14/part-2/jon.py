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
        def needed(elem, wanted):
            if elem == "FUEL":
                return wanted
            cache_key = (elem, wanted)
            if cache_key in cache:
                return cache[cache_key]

            needed_count = 0
            for relem in rev_deps.get(elem, []):
                needed_count += needed(relem, wanted) * deps[relem][elem]

            needed_reac = div_ceil(needed_count, qty[elem])
            cache[cache_key] = needed_reac
            return needed_reac

        budget = 1000000000000

        # binary search
        n = budget // needed("ORE", 1)
        step = n
        while True:
            while needed("ORE", n) <= budget:
                n += step
            n -= step
            if step == 1:
                return n
            step = max(step // 2, 1)


def div_ceil(a, b):
    if a % b == 0:
        return a // b
    return (a // b) + 1
