from tool.runners.python import SubmissionPy
from time import sleep
class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        l = ''
        for i in range(150):
            j = i
            while s[j] == '2':
                j += 150
            l += s[j]
        return l
