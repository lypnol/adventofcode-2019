from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        fuels = s.splitlines()
        s_req = 0
        for f in fuels:
            current_fuel = int(f)
            while current_fuel > 8:
                current_fuel = current_fuel // 3 - 2
                s_req += current_fuel
        return s_req
