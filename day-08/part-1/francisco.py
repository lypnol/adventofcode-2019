from tool.runners.python import SubmissionPy


def parse_image(string, rows, cols):
    digits = [int(i) for i in string]
    layers = len(digits) // (rows * cols)
    assert len(digits) % (rows * cols) == 0

    return [
        [
            [digits[(rows * cols) * l + cols * r + c] for c in range(cols)]
            for r in range(rows)
        ]
        for l in range(layers)
    ]


def solve_part1(image):
    count = lambda n, layer: sum(row.count(n) for row in layer)
    i = min(range(len(image)), key=lambda i: count(0, image[i]))
    return count(1, image[i]) * count(2, image[i])


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        image = parse_image(s, 6, 25)
        return solve_part1(image)
