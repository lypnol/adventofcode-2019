from collections import defaultdict
from tool.runners.python import SubmissionPy

WIDTH, HEIGHT = 25, 6


def image(inp):
    layer_size = WIDTH * HEIGHT
    n_layers = len(inp) // layer_size

    layers = [defaultdict(int) for i in range(n_layers)]

    # Start with a transparent image
    image = ["2" for _ in range(layer_size)]

    for i, layer in enumerate(layers):

        start = i * layer_size

        for j in range(layer_size):
            if image[j] == "2":
                image[j] = inp[start + j]

    return image


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        img = image(s)

        table = {"2": " ", "1": "#", "0": "."}

        for y in range(HEIGHT):
            for x in range(WIDTH):
                print(table[img[y * WIDTH + x]], end="")

            print()
