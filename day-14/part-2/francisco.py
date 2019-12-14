from tool.runners.python import SubmissionPy


from collections import defaultdict
import math
import re


ORE = "ORE"
FUEL = "FUEL"

line_regexp = re.compile(r"(\d+) (\w+)")


def parse_line(line):
    left_right = line.strip().split("=>")
    left_right_matches = [line_regexp.findall(part) for part in left_right]
    return tuple(
        {name: int(number) for number, name in matches}
        for matches in left_right_matches
    )


def parse_file(s):
    transformations = {}

    for line in s.splitlines():
        left, right = parse_line(line)
        assert len(right) == 1
        chemical, number = next(iter(right.items()))

        # A given chemical can only be produced by a single transformation
        assert chemical not in transformations

        transformations[chemical] = (number, left)

    return transformations


def transform(resources, resource, transformation):
    n = math.ceil(resources[resource] / transformation[0])

    resources[resource] -= n * transformation[0]

    for chemical, quantity in transformation[1].items():
        resources[chemical] += n * quantity


def solve_part1(transformations, fuel=1):
    resources = defaultdict(int, {FUEL: fuel})

    while True:
        try:
            # pick any chemical whose value is stricly positive
            resource, quantity = next(
                (resource, quantity)
                for resource, quantity in resources.items()
                if quantity > 0 and resource != ORE
            )
            # transform it into more primitive chemicals
            transform(resources, resource, transformations[resource])
        except StopIteration:
            # no more chemicals to transform
            return resources[ORE]


def solve_part2(transformations):
    # binary search

    max_ore = 1000000000000
    min_fuel = 1
    max_fuel = 2

    while solve_part1(transformations, max_fuel) < max_ore:
        min_fuel *= 2
        max_fuel *= 2

    # At that point, we have:
    # solve_part1(min_fuel) < max_ore <= solve_part2(max_fuel)

    # This invariant remains valid during the next loop.
    # (which is the actual binary search)

    while max_fuel - min_fuel > 1:
        middle_fuel = min_fuel + (max_fuel - min_fuel) // 2
        middle_ore = solve_part1(transformations, middle_fuel)
        if middle_ore > max_ore:
            max_fuel = middle_fuel
        else:
            min_fuel = middle_fuel

    if solve_part1(transformations, max_fuel) < max_ore:
        return max_fuel

    return min_fuel


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part2(parse_file(s))
