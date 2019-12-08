from tool.runners.python import SubmissionPy

WIDTH = 25
HEIGHT = 6


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        payload = [int(x) for x in list(s)]
        layers = [payload[i:i + WIDTH * HEIGHT] for i in range(0, len(s), WIDTH * HEIGHT)]
        img = [0 for _ in range(WIDTH * HEIGHT)]
        for i in range(len(img)):
            for l in layers:
                if l[i] != 2:
                    img[i] = l[i]
                    break
        return "".join([str(x) for x in img])
