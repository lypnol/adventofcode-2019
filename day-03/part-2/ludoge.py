from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def gen_path(self, moves):
        current_position = (0, 0)
        path = []
        for move in moves:
            direction, length = move[0], int(move[1:])
            if direction == "R":
                dx, dy = 1, 0
            if direction == "L":
                dx, dy = -1, 0
            if direction == "U":
                dx, dy = 0, 1
            if direction == "D":
                dx, dy = 0, -1
            path += [
                (current_position[0] + i * dx, current_position[1] + i * dy)
                for i in range(1, length + 1)
            ]
            current_position = path[-1]
        return path

    def run(self, s):
        move_lists = [x.split(",") for x in s.split()]
        paths = [self.gen_path(moves) for moves in move_lists]
        intersections = set(paths[0]).intersection(paths[1])
        return min(
            map(lambda x: paths[0].index(x) + paths[1].index(x) + 2, intersections)
        )
