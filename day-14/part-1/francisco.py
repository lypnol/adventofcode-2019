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


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part1(parse_file(s))
