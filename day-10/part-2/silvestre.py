import math
from functools import lru_cache
import itertools

from tool.runners.python import SubmissionPy

@lru_cache(maxsize=2**10)
def pgcd(a, b):
    if b == 0:
        return a
    r = a % b
    return pgcd(b, r)

def polar(x, y, x_0, y_0):
    x = x - x_0
    y = y - y_0
    r = x*x + y*y
    theta = math.atan2(y, x)
    if theta < - math.pi / 2:
        theta = theta + 2 * math.pi 
    return (theta, r)

class SilvestreSubmission(SubmissionPy):

    @staticmethod
    def parse_input(s):
        for j, line in enumerate(s.splitlines()):
            for i, char in enumerate(line):
                if char == "#":
                    yield (i,j)

    @staticmethod
    def count_in_sight(pt, all_pts):
        seen = set()
        u_x, u_y = pt
        for v_x, v_y in all_pts:
            if u_x == v_x and u_y == v_y :
                continue
            x = u_x - v_x
            y = u_y - v_y           
            norm = pgcd(abs(x), abs(y))
            seen.add((x//norm, y//norm))
        return len(seen)

    def run(self, s):
        all_pts = list(self.parse_input(s))
        station_x_y = max(all_pts, key=lambda pt: self.count_in_sight(pt, all_pts))
        
        polar_to_x_y = {polar(*pt, *station_x_y): pt for pt in all_pts if pt != station_x_y}
        unique_thetas = sorted(set(theta for theta, _ in polar_to_x_y))

        aligned = []
        for theta1 in unique_thetas:
            aligned.append(sorted(el for el in polar_to_x_y if math.isclose(theta1, el[0])))
        order = list(itertools.chain(*zip(*aligned)))

        x, y = polar_to_x_y[order[200-1]]
        return x * 100 + y



        

        