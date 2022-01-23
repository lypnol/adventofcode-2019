from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        low, high = map(int, s.split("-"))
        nb_correct = 0
        for password in range(low, high + 1):
            password = str(password)
            has_double_digit = False
            is_increasing = True
            for i in range(1, len(password)):
                if password[i - 1] == password[i]:
                    has_double_digit = True
                if int(password[i - 1]) > int(password[i]):
                    is_increasing = False
                    break

            if has_double_digit and is_increasing:
                nb_correct += 1

        return nb_correct
