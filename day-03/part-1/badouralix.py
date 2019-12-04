from sys import maxsize
from tool.runners.python import SubmissionPy
from typing import Set, Tuple


class BadouralixSubmission(SubmissionPy):
    """
    So this deserves some comments because I tried a few alternatives that were
    overall slower than this dirty yolo copy-pasta.

    alt-1 : use a function to compute the set of locations of both wires and
            then compute the intersection of the two sets

    alt-2 : compute locations_two in the walk over path two and then compute the
            the closest intersection

    alt-3 : same as alt-2 with a small refactoring to avoid the many
            for step in range(length)

            if direction == "R":
                horizontal_move = 1
                vertical_move = 0
            ...
            for step in range(length):
            ...

    alt-4 : alternate refactoring of the many for step in range(length)

            if direction == "R":
                horizontal_move, vertical_move = (1, 0)
            ...
            for step in range(length):
            ...

    alt-5 : build a list locations_one before turning it into a set
    """

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Parse input
        split_one, split_two = s.splitlines()
        path_one = split_one.split(",")
        path_two = split_two.split(",")

        # Walk path one and record steps
        locations_one: Set[Tuple[int, int]] = set()
        current_location = (0, 0)
        for branch in path_one:
            direction = branch[0]
            length = int(branch[1:])

            if direction == "R":
                for step in range(length):
                    current_location = (current_location[0] + 1, current_location[1])
                    locations_one.add(current_location)
            elif direction == "L":
                for step in range(length):
                    current_location = (current_location[0] - 1, current_location[1])
                    locations_one.add(current_location)
            elif direction == "U":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] + 1)
                    locations_one.add(current_location)
            elif direction == "D":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] - 1)
                    locations_one.add(current_location)

        # Walk path two and find intersection
        closest_distance = maxsize
        current_location = (0, 0)
        for branch in path_two:
            direction = branch[0]
            length = int(branch[1:])

            if direction == "R":
                for step in range(length):
                    current_location = (current_location[0] + 1, current_location[1])
                    if current_location in locations_one:
                        distance = abs(current_location[0]) + abs(current_location[1])
                        closest_distance = min(closest_distance, distance)
            elif direction == "L":
                for step in range(length):
                    current_location = (current_location[0] - 1, current_location[1])
                    if current_location in locations_one:
                        distance = abs(current_location[0]) + abs(current_location[1])
                        closest_distance = min(closest_distance, distance)
            elif direction == "U":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] + 1)
                    if current_location in locations_one:
                        distance = abs(current_location[0]) + abs(current_location[1])
                        closest_distance = min(closest_distance, distance)
            elif direction == "D":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] - 1)
                    if current_location in locations_one:
                        distance = abs(current_location[0]) + abs(current_location[1])
                        closest_distance = min(closest_distance, distance)

        # Return result
        return closest_distance
