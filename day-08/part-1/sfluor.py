from collections import defaultdict
from tool.runners.python import SubmissionPy


def checksum(inp, width, height):
    layer_size = width * height
    n_layers = len(inp) // layer_size

    layers = [defaultdict(int) for i in range(n_layers)]

    # idx, value
    min_digits = (0, 1e10)

    for i, layer in enumerate(layers):

        start = i * layer_size

        for j in range(layer_size):
            digit = inp[start + j]

            if digit in "012":
                layer[digit] += 1

        if layer["0"] < min_digits[1]:
            min_digits = (i, layer["0"])

    idx, _ = min_digits
    l = layers[idx]

    return l["1"] * l["2"]


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        return checksum(s, 25, 6)
