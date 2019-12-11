from tool.parser import Parser


letters = {
    "011001001010010111101001010010": "A",
    "111001001011100100101001011100": "B",
    "011001001010000100001001001100": "C",
    "111101000011100100001000011110": "E",
    "111101000011100100001000010000": "F",
    "011001001010000101101001001110": "G",
    "100101001011110100101001010010": "H",
    "001100001000010000101001001100": "J",
    "100101010011000101001010010010": "K",
    "100001000010000100001000011110": "L",
    "111001001010010111001000010000": "P",
    "111001001010010111001010010010": "R",
    "100101001010010100101001001100": "U",
    "100011000101010001000010000100": "Y",
    "111100001000100010001000011110": "Z",
}

LETTER_WIDTH = 5
N_LETTERS = 8
HEIGHT = 6
WIDTH = N_LETTERS * LETTER_WIDTH

class D11P2Parser(Parser):

    def __init__(self):
        self.unknown = set()

    def parse(self, s):
        ss = s.replace("\n", "").strip()
        if len(ss) != WIDTH * HEIGHT:
            return s
        if not all(c in ("0", "1") for c in ss):
            return s

        lines = [ss[WIDTH*i:WIDTH*(i+1)] for i in range(HEIGHT)]

        def letter(pos):
            return "".join(l[LETTER_WIDTH*pos:LETTER_WIDTH*(pos+1)] for l in lines)

        res = "".join(self.parse_letter(letter(pos)) for pos in range(N_LETTERS))
        return res

    def parse_letter(self, s):
        if s not in letters:
            self.unknown.add(s)
            return "?"
        return letters[s]

    def cleanup(self):
        if len(self.unknown) == 0:
            return
        print("Some letters are unknown to the parser, please add them.")
        print("Copy this code and replace the question marks with the letters below,")
        print("then add it to " + __file__)
        print()
        unknown = list(self.unknown)
        for s in unknown:
            print('"{}": "?",'.format(s))
        print()
        for s in unknown:
            pretty_print_letter(s)
            print()


def pretty_print_letter(s):
    ss = s.replace("0", " ").replace("1", u"\u2588")
    for l in range(HEIGHT):
        print(ss[LETTER_WIDTH*l:LETTER_WIDTH*(l+1)])
