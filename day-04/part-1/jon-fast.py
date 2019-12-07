from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s_start, s_end = s.strip().split("-")

        end = [int(k) for k in s_end]
        normalize(end)

        curr = [int(k) for k in s_start]
        normalize(curr)

        count = 0
        while curr != end:
            if has_dup(curr):
                count += 1
            next_value(curr)

        return count


def normalize(l):
    for i in range(5):
        if l[i+1] < l[i]:
            for j in range(i+1, 6):
                l[j] = l[i]
            return


def next_value(l):
    for i in range(5, -1, -1):
        if l[i] < 9:
            l[i] += 1
            for j in range(i + 1, 6):
                l[j] = l[i]
            return
    raise Exception("reached the end")


def has_dup(l):
    for i in range(5):
        if l[i] == l[i + 1]:
            return True
    return False
