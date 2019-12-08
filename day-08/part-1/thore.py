from collections import Counter
from textwrap import wrap

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        LAYER_WIDTH = 25
        LAYER_HEIGHT = 6

        layers = wrap(s, LAYER_WIDTH * LAYER_HEIGHT)

        def layer_map(layer):
            c = Counter(layer)
            return (c["0"], c["1"] * c["2"])

        layers_counts = [layer_map(layer) for layer in layers]

        return min(layers_counts)[1]
