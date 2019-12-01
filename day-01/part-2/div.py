from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):

    def run(self, s):
        masses = [int(x) for x in s.splitlines()]

        # We cache the results returned by required_fuel using memoization
        # Note: This is totally over-engineered for this problem, the cache hit rate is around 9% on my input
        def memoize(f):
            cache = dict()
            def helper(x):
                if x in cache:
                    return cache[x]
                result = f(x)
                cache[x] = result
                return result
            return helper

        def required_fuel(mass):
            fuel = (mass//3)-2
            if fuel <= 0:
                # negative fuel is treated as if it requires zero fuel
                return 0

            return fuel + required_fuel(fuel)

        required_fuel = memoize(required_fuel)

        return sum(required_fuel(m) for m in masses)
