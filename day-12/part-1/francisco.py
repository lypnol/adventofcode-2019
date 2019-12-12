from tool.runners.python import SubmissionPy


def parse_input(s):
    positions = []
    for line in s.splitlines():
        numbers = line.strip()[1:-1].split(",")
        positions.append(tuple(int(n.split("=")[1]) for n in numbers))
    return positions


def new_velocities(positions, velocities):
    for i in range(len(positions)):
        for j in range(len(positions)):
            velocities[i] = tuple(
                velocities[i][k]
                + (
                    1
                    if positions[i][k] < positions[j][k]
                    else -1
                    if positions[i][k] > positions[j][k]
                    else 0
                )
                for k in range(3)
            )
    return velocities


def new_positions(positions, velocities):
    return [
        (p[0] + v[0], p[1] + v[1], p[2] + v[2]) for p, v in zip(positions, velocities)
    ]


def energy(positions, velocities):
    return sum(
        sum(map(abs, p)) * sum(map(abs, v)) for p, v in zip(positions, velocities)
    )


def solve_part1(positions, steps=1000):
    velocities = [(0, 0, 0) for _ in range(len(positions))]
    for _ in range(steps):
        velocities = new_velocities(positions, velocities)
        positions = new_positions(positions, velocities)
    return energy(positions, velocities)


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part1(parse_input(s))
