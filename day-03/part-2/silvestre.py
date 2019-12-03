from tool.runners.python import SubmissionPy

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        path1, path2 = (line.split(",") for line in s.splitlines())

        ridges1 = self.get_ridges(path1)
        ridges2 = self.get_ridges(path2)

        _, steps = self.get_intersections_w_steps(ridges1, ridges2)

        return min(steps)

    @staticmethod
    def get_ridges(path):
        ridges = []
        previous = [0,0]
        for el in path:
            current = previous.copy()
            if el[0] == "U":
                current[1] += int(el[1:])
            elif el[0] == "D":
                current[1] -= int(el[1:])
            elif el[0] == "R":
                current[0] += int(el[1:])
            elif el[0] == "L":
                current[0] -= int(el[1:])
            ridges.append((tuple(previous), tuple(current)))
            previous = current.copy()
        return ridges

    @staticmethod
    def get_intersections_w_steps(ridges1, ridges2):
        intersections = []
        steps = []

        steps_to_intersections_wire1 = {}
        steps_to_intersections_wire2 = {}
        steps_count1 = 0
        for pt_a, pt_b in ridges1:
            steps_count1 += manhattan_distances(pt_b, pt_a)
            steps_count2 = 0
            for pt_c, pt_d in ridges2:
                steps_count2 += manhattan_distances(pt_d, pt_c)

                cond_x = (pt_a[0] - pt_c[0] > 0) != (pt_b[0] - pt_d[0] > 0)
                cond_y = (pt_a[1] - pt_c[1] > 0) != (pt_b[1] - pt_d[1] > 0)
                if cond_x and cond_y:
                    # intersection !
                    x = pt_a[0] if pt_a[0] == pt_b[0] else pt_c[0]
                    y = pt_a[1] if pt_a[1] == pt_b[1] else pt_c[1]

                    if not (x,y) in steps_to_intersections_wire1:
                        steps_to_intersections_wire1[(x, y)] = steps_count1 - manhattan_distances(pt_b, (x,y))
                    if not (x,y) in steps_to_intersections_wire2:
                        steps_to_intersections_wire2[(x, y)] = steps_count2 - manhattan_distances(pt_d, (x,y))
                    
                    steps1 = steps_to_intersections_wire1[(x, y)]
                    steps2 = steps_to_intersections_wire2[(x, y)]
                    
                    intersections.append((x, y))
                    steps.append(steps1+steps2)
        return intersections, steps

def manhattan_distances(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])