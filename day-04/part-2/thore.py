from tool.runners.python import SubmissionPy


def is_valid(password):
    if password > 999_999 or password < 100_000:
        return False

    password = str(password)
    has_double = False
    for i in range(len(password) - 1):
        if password[i + 1] < password[i]:
            return False
        if (
            password[i + 1] == password[i]
            and (i - 1 < 0 or password[i - 1] != password[i])
            and (i + 2 >= len(password) or password[i + 2] != password[i])
        ):
            has_double = True
    return has_double


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        mini, maxi = [int(n) for n in s.split("-")]
        return sum([is_valid(number) for number in range(mini, maxi + 1)])
