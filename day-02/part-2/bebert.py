from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s: str):
        # s = "1,9,10,3,2,3,11,0,99,30,40,50"
        codes = [int(x) for x in s.split(",")]

        init_state = codes.copy()

        for noun in range(100):
            for verb in range(100):
                codes = init_state.copy()
                codes[1] = noun
                codes[2] = verb
                i = 0
                while codes[i] != 99:
                    if codes[i] == 1:
                        codes[codes[i+3]] = codes[codes[i+1]] + codes[codes[i+2]]
                    else:
                        codes[codes[i+3]] = codes[codes[i+1]] * codes[codes[i+2]]
                    i += 4
                if codes[0] == 19690720:
                    return 100 * noun + verb
        return -1
