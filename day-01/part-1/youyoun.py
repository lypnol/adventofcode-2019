from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        fuels = s.splitlines()
        s_reqs = 0
        for f in fuels:
            s_reqs += int(f) // 3 - 2
        return s_reqs
