from tool.runners.python import SubmissionPy
from functools import lru_cache

@lru_cache(maxsize=2**10)
def pgcd(a, b):
    if b == 0:
        return a
    r = a % b
    return pgcd(b, r)

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
        return max(self.count_in_sight(pt, all_pts) for pt in all_pts)
        




        

        