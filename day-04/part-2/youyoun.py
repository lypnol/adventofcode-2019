from tool.runners.python import SubmissionPy
from collections import Counter

def is_password(pwd):
    return is_sorted(pwd) and exists_pair_only(pwd)

def is_sorted(pwd):
    return pwd[1] >= pwd[0] and pwd[2] >= pwd[1] and pwd[3] >= pwd[2] and pwd[4] >= pwd[3] and pwd[5] >= pwd[4]

def exists_pair_only(pwd):
    counts = Counter(pwd)
    for e in counts:
        if counts[e] == 2:
            return True
    return False

class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        start, end = s.split("-")
        count = 0
        for i in range(int(start), int(end) + 1):
            count += is_password(str(i))
        return count
