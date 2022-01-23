from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        original_intcodes = [int(i) for i in s.split(",")]

        for noun in range(100):
            for verb in range(100):
                intcodes = original_intcodes[:]
                intcodes[1] = noun
                intcodes[2] = verb
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

                if intcodes[0] == 19690720:
                    return 100 * noun + verb
