from tool.runners.python import SubmissionPy
import re


class Universe:
    def __init__(self):
        self.positions = [0 for _ in range(12)]
        self.velocities = [0 for _ in range(12)]

    def get_state(self):
        return (*self.positions, *self.velocities)

    def update_velocity(self):
        for i in range(0, 12, 3):
            for j in range(i + 3, 12, 3):
                for k in range(3):
                    if self.positions[i + k] < self.positions[j + k]:
                        self.velocities[i + k] = self.velocities[i + k] + 1
                        self.velocities[j + k] = self.velocities[j + k] - 1
                    elif self.positions[i + k] > self.positions[j + k]:
                        self.velocities[i + k] = self.velocities[i + k] - 1
                        self.velocities[j + k] = self.velocities[j + k] + 1
        return

    def update_position(self):
        for i in range(12):
            self.positions[i] += self.velocities[i]
        return


def total_energy(univ):
    en = 0
    for i in range(0, 12, 3):
        en += sum((abs(univ.positions[i + k]) for k in range(3))) * sum((abs(univ.velocities[i + k]) for k in range(3)))
    return en


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        history = set()
        i = 0
        univ = Universe()
        for pos in re.findall(r"<\w=(-?\d+),\s\w=(-?\d+),\s\w=(-?\d+)>", s):
            j = 0
            while j < len(pos):
                univ.positions[i + j] = int(pos[j])
                j += 1
            i += 3
        for i in range(1000):
            univ.update_velocity()
            univ.update_position()
        return total_energy(univ)
