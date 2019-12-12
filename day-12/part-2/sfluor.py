import itertools
from tool.runners.python import SubmissionPy

class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __repr__(self):
        return f"Moon(x={self.x}, y={self.y}, z={self.z}, vx={self.vx}, vy={self.vy}, vz={self.vz})"

def parse_moons(s):
    for line in s.splitlines():
        x, y, z = [int(el.strip(">")[3:]) for el in line.split(",")]
        yield Moon(x=x, y=y, z=z)

def cmp(a, b):
    if a < b: return -1
    if a > b: return 1
    return 0

def apply_gravity(moons):
    for m, m2 in itertools.product(moons, repeat=2):
        m.vx += cmp(m2.x, m.x)
        m.vy += cmp(m2.y, m.y)
        m.vz += cmp(m2.z, m.z)

def move(moons):
    for m in moons:
        m.x += m.vx
        m.y += m.vy
        m.z += m.vz

def step(moons):
    apply_gravity(moons)
    move(moons)

class SfluorSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        moons = list(parse_moons(s))
        for _ in range(2772):
            step(moons)

        print(moons)
        return None
