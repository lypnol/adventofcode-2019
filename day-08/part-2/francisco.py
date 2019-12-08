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


def decode_image(image):
    layers, rows, cols = len(image), len(image[0]), len(image[0][0])
    decoded_image = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            for l in range(layers):
                if image[l][r][c] != 2:
                    decoded_image[r][c] = image[l][r][c]
                    break
    return decoded_image


def solve_part2(image):
    decoded_image = decode_image(image)
    cast_int = lambda i: "#" if i == 1 else " "
    cast_row = lambda row: "".join(map(cast_int, row))
    cast_image = lambda image: "\n".join(map(cast_row, image))
    return cast_image(decoded_image)


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        image = parse_image(s, 6, 25)
        return solve_part2(image).replace("\n", "").replace("#", "1").replace(" ", "0")
