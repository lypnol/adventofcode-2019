from collections import defaultdict
from tool.runners.python import SubmissionPy

WIDTH, HEIGHT = 25, 6
LETTER_WIDTH = 5
N_LETTERS = 5
TABLE = {"2": " ", "1": "#", "0": " "}


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
        pretty_print_img(img)

        # letters = ocr(img)
        # for letter in letters:
        #     pretty_print_letter(letter)
        #     print("------")


### DEBUG
def ocr(img):
    res = [[] for i in range(N_LETTERS)]

    for y in range(HEIGHT):
        s = y * WIDTH
        for i in range(N_LETTERS):
            res[i].extend(img[s + i * LETTER_WIDTH : s + (i + 1) * LETTER_WIDTH])

    return res


def pretty_print_img(img):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(TABLE[img[y * WIDTH + x]], end="")

        print()


def pretty_print_letter(letter):
    for y in range(HEIGHT):
        for char in letter[y * LETTER_WIDTH : (y + 1) * LETTER_WIDTH]:
            print(TABLE[char], end="")
        print()
