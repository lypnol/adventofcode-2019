from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        width, height = 25, 6
        payload = [int(x) for x in list(s)]
        layers = [payload[i:i + width * height] for i in range(0, len(s), width * height)]
        min_n_zeros = float("inf")
        min_n_zeros_ind = 0
        for i in range(len(layers)):
            n_zeros = layers[i].count(0)
            if min_n_zeros > n_zeros:
                min_n_zeros = n_zeros
                min_n_zeros_ind = i
        return layers[min_n_zeros_ind].count(1) * layers[min_n_zeros_ind].count(2)
