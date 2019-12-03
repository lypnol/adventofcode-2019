from tool.runners.python import SubmissionPy

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        path1, path2 = (line.split(",") for line in s.splitlines())

        ridges1 = self.get_ridges(path1)
        ridges2 = self.get_ridges(path2)

        intersections = self.get_intersections(ridges1, ridges2)
        
        return min(abs(x)+abs(y) for x,y in intersections)

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
            ridges.append((previous, current))
            previous = current.copy()
        return ridges

    @staticmethod
    def get_intersections(ridges1, ridges2):
        intersections = []
        for pt_a, pt_b in ridges1:
            for pt_c, pt_d in ridges2:
                cond_x = (pt_a[0] - pt_c[0] > 0) != (pt_b[0] - pt_d[0] > 0)
                cond_y = (pt_a[1] - pt_c[1] > 0) != (pt_b[1] - pt_d[1] > 0)
                if cond_x and cond_y:
                    x = pt_a[0] if pt_a[0] == pt_b[0] else pt_c[0]
                    y = pt_a[1] if pt_a[1] == pt_b[1] else pt_c[1]
                    intersections.append((x, y))
        return intersections