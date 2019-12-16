from tool.runners.python import SubmissionPy

BASE_PATTERN = [0, 1, 0, -1]
N_PHASES = 100


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        signal = [int(d) for d in s]
        for _ in range(N_PHASES):
            signal = fft(signal)
        return "".join([str(signal[i]) for i in range(8)])


def fft(input_signal):
    n = len(input_signal)
    output = [0] * n

    for i in range(n):
        res = 0
        for j in range(n):
            pattern_idx = ((j + 1) // (i + 1)) % len(BASE_PATTERN)
            res += input_signal[j] * BASE_PATTERN[pattern_idx]
        output[i] = abs(res) % 10
    return output

