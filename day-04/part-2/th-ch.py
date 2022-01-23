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
            streak_length = 1
            has_a_streak_of_2 = False
            is_increasing = True
            for i in range(1, len(password)):
                if password[i - 1] == password[i]:
                    streak_length += 1
                else:
                    if streak_length == 2:
                        has_a_streak_of_2 = True
                    streak_length = 1
                if int(password[i - 1]) > int(password[i]):
                    is_increasing = False
                    break

            if not has_a_streak_of_2 and streak_length == 2:
                has_a_streak_of_2 = True

            if has_a_streak_of_2 and is_increasing:
                nb_correct += 1

        return nb_correct
