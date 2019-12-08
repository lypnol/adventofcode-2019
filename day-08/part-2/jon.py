from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s = s.strip()

        w = 25
        h = 6
        a = w * h
        n = len(s) // a

        def pixel(k):
            for i in range(n):
                v = s[k + i*a]
                if v != "2":
                    return v
            return "2"

        return "\n".join("".join(pixel(w*x+y) for y in range(w)) for x in range(h))
