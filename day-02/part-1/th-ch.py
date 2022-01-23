from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        intcodes = [int(i) for i in s.split(",")]
        intcodes[1] = 12
        intcodes[2] = 2
        i = 0
        while intcodes[i] != 99:
            if intcodes[i] == 1:
                intcodes[intcodes[i + 3]] = (
                    intcodes[intcodes[i + 1]] + intcodes[intcodes[i + 2]]
                )
            elif intcodes[i] == 2:
                intcodes[intcodes[i + 3]] = (
                    intcodes[intcodes[i + 1]] * intcodes[intcodes[i + 2]]
                )
            i += 4

        return intcodes[0]
