from tool.runners.python import SubmissionPy
import numpy as np

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        return sum(i//3 - 2 for i in map(int, s.split("\n")))