from sys import maxsize
from tool.runners.python import SubmissionPy
from typing import Dict, Set, Tuple


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Parse input
        split_one, split_two = s.splitlines()
        path_one = split_one.split(",")
        path_two = split_two.split(",")

        # Walk path one and record steps
        locations_one: Dict[Tuple[int, int], int] = dict()
        current_location = (0, 0)
        current_distance = 0
        for branch in path_one:
            direction = branch[0]
            length = int(branch[1:])

            if direction == "R":
                for step in range(length):
                    current_location = (current_location[0] + 1, current_location[1])
                    current_distance += 1
                    if current_location not in locations_one:
                        locations_one[current_location] = current_distance
            elif direction == "L":
                for step in range(length):
                    current_location = (current_location[0] - 1, current_location[1])
                    current_distance += 1
                    if current_location not in locations_one:
                        locations_one[current_location] = current_distance
            elif direction == "U":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] + 1)
                    current_distance += 1
                    if current_location not in locations_one:
                        locations_one[current_location] = current_distance
            elif direction == "D":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] - 1)
                    current_distance += 1
                    if current_location not in locations_one:
                        locations_one[current_location] = current_distance

        # Walk path two and find intersection
        closest_distance = maxsize
        current_location = (0, 0)
        current_distance = 0
        for branch in path_two:
            direction = branch[0]
            length = int(branch[1:])

            if direction == "R":
                for step in range(length):
                    current_location = (current_location[0] + 1, current_location[1])
                    current_distance += 1
                    if current_location in locations_one:
                        distance = locations_one[current_location] + current_distance
                        closest_distance = min(closest_distance, distance)
            elif direction == "L":
                for step in range(length):
                    current_location = (current_location[0] - 1, current_location[1])
                    current_distance += 1
                    if current_location in locations_one:
                        distance = locations_one[current_location] + current_distance
                        closest_distance = min(closest_distance, distance)
            elif direction == "U":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] + 1)
                    current_distance += 1
                    if current_location in locations_one:
                        distance = locations_one[current_location] + current_distance
                        closest_distance = min(closest_distance, distance)
            elif direction == "D":
                for step in range(length):
                    current_location = (current_location[0], current_location[1] - 1)
                    current_distance += 1
                    if current_location in locations_one:
                        distance = locations_one[current_location] + current_distance
                        closest_distance = min(closest_distance, distance)

        # Return result
        return closest_distance
