from tool.runners.python import SubmissionPy
from collections import namedtuple

Segment = namedtuple("Segment", "p q")
Point = namedtuple("Point", "x y")


class SfluorSubmission(SubmissionPy):
    def dist(self, point):
        return abs(point.x) + abs(point.y)

    def segments(self, wire):
        curr = Point(0, 0)
        segms = []

        for p in wire.split(","):
            direction = p[0]
            value = int(p[1:])

            new_point = None

            if direction == "R":
                new_point = Point(curr.x + value, curr.y)
            if direction == "L":
                new_point = Point(curr.x - value, curr.y)
            if direction == "U":
                new_point = Point(curr.x, curr.y + value)
            if direction == "D":
                new_point = Point(curr.x, curr.y - value)

            segms.append(Segment(curr, new_point))
            curr = new_point

        return segms

    def intersects(self, seg1, seg2):
        (p1, q1) = seg1

        # XXX: Ignore the case where we have two // segments
        v, h = None, None
        if p1.x == q1.x:
            v = seg1
            h = seg2
        else:
            v = seg2
            h = seg1

        if v.p.x > h.p.x and v.p.x > h.q.x:
            return None

        if v.p.x < h.p.x and v.p.x < h.q.x:
            return None

        if h.p.y > v.p.y and h.p.y > v.q.y:
            return None

        if h.p.y < v.p.y and h.p.y < v.q.y:
            return None

        return Point(v.p.x, h.p.y)

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here

        origin = Point(0, 0)
        w1, w2 = [self.segments(w) for w in s.splitlines()]

        min_dist = None

        for s1 in w1:
            for s2 in w2:
                p = self.intersects(s1, s2)
                if p is None or p == origin:
                    continue

                d = self.dist(p)

                if min_dist is None or d < min_dist:
                    min_dist = d

        return min_dist
