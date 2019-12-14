from tool.runners.python import SubmissionPy
import re


class Axis:
    def __init__(self):
        self.pos = [0, 0, 0, 0]
        self.vel = [0, 0, 0, 0]

    def update_velocity(self):
        for i in range(4):
            for j in range(i, 4):
                if self.pos[i] != self.pos[j]:
                    sup = 2 * (int(self.pos[i] < self.pos[j]) - 1 / 2)
                    self.vel[j] += -sup
                    self.vel[i] += sup

    def update_positions(self):
        for i in range(4):
            self.pos[i] += self.vel[i]
        return

    @property
    def state(self):
        return (*self.pos, *self.vel)


def ppcm(*n):
    """Calcul du 'Plus Petit Commun Multiple' de n (>=2) valeurs entières (Euclide)"""

    def _pgcd(a, b):
        while b: a, b = b, a % b
        return a

    p = abs(n[0] * n[1]) // _pgcd(n[0], n[1])
    for x in n[2:]:
        p = abs(p * x) // _pgcd(p, x)
    return p


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        ax = [Axis(), Axis(), Axis()]
        for i, pos in enumerate(re.findall(r"<\w=(-?\d+),\s\w=(-?\d+),\s\w=(-?\d+)>", s)):
            for j in range(3):
                ax[j].pos[i] = int(pos[j])
        cycles = [0, 0, 0]
        for i in range(3):
            history = ax[i].state
            while True:
                ax[i].update_velocity()
                ax[i].update_positions()
                cycles[i] += 1
                if history == ax[i].state:
                    break
        return ppcm(*cycles)
