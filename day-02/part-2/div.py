from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):

    def execute(self, intcode, noun, verb):
        # copy the list
        intcode = [x for x in intcode]

        intcode[1] = noun
        intcode[2] = verb

        pos = 0
        while True:
            # halt condition
            if intcode[pos] == 99:
                return intcode[0]

            if intcode[pos] == 1:
                intcode[intcode[pos+3]] = intcode[intcode[pos+1]] + intcode[intcode[pos+2]]
            elif intcode[pos] == 2:
                intcode[intcode[pos+3]] = intcode[intcode[pos+1]] * intcode[intcode[pos+2]]

            pos += 4


    def run(self, s):
        intcode = [int(x) for x in s.split(",")]

        for noun in range(100):
            for verb in range(100):
                if self.execute(intcode, noun, verb) == 19690720:
                    return noun * 100 + verb
