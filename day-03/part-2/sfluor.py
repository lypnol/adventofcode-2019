from tool.runners.python import SubmissionPy
from collections import namedtuple

Segment = namedtuple("Segment", "p q steps")
Point = namedtuple("Point", "x y")


class SfluorSubmission(SubmissionPy):
    def seg_dist(self, seg, point):
        if seg.p.x == seg.q.x:
            return abs(point.y - seg.p.y)

        return abs(point.x - seg.p.x)

    def segments(self, wire):
        curr = Point(0, 0)
        segms = []

        steps = 0

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

            segms.append(Segment(curr, new_point, steps))
            steps += value
            curr = new_point

        return segms

    def intersects(self, seg1, seg2):
        (p1, q1, _) = seg1

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

        steps = None

        for s1 in w1:
            for s2 in w2:
                p = self.intersects(s1, s2)
                if p is None or p == origin:
                    continue

                s = s1.steps + self.seg_dist(s1, p) + s2.steps + self.seg_dist(s2, p)

                if steps is None or s < steps:
                    steps = s

        return steps
