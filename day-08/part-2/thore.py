from textwrap import wrap

from tool.runners.python import SubmissionPy


def pprint(image):
    lines = ["".join(line) for line in image]
    image_str = "\n".join(lines).replace("0", u"\u2588").replace("1", " ")
    print(image_str)


def format_result(image):
    lines = ["".join(line) for line in image]
    return "".join(lines)


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        LAYER_WIDTH = 25
        LAYER_HEIGHT = 6

        layers = wrap(s, LAYER_WIDTH * LAYER_HEIGHT)

        image = [[2 for j in range(LAYER_WIDTH)] for i in range(LAYER_HEIGHT)]
        for i in range(LAYER_HEIGHT):
            for j in range(LAYER_WIDTH):
                idx = i * LAYER_WIDTH + j
                for k in range(len(layers)):
                    if layers[k][idx] != "2":
                        image[i][j] = layers[k][idx]
                        break

        # pprint(image)
        return format_result(image)
