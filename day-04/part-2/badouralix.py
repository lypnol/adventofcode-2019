from tool.runners.python import SubmissionPy

import re


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        nmin, nmax = map(int, s.split("-"))

        decrease_somewhere = re.compile(
            r"(1[0-0]|2[0-1]|3[0-2]|4[0-3]|5[0-4]|6[0-5]|7[0-6]|8[0-7]|9[0-8])"
        )
        with_double = re.compile(
            r"((?<!0)00(?!0)|(?<!1)11(?!1)|(?<!2)22(?!2)|(?<!3)33(?!3)|(?<!4)44(?!4)|(?<!5)55(?!5)|(?<!6)66(?!6)|(?<!7)77(?!7)|(?<!8)88(?!8)|(?<!9)99(?!9))"
        )

        result = 0
        i = nmin

        while i <= nmax:
            str_i = str(i)

            # Try to find adjacent digits in i that are in decreasing order
            decrease_group = re.search(decrease_somewhere, str_i)
            if decrease_group is not None:
                # Skip numbers that are not valid because the current i is not valid
                # Example : i = 123432, error_index = 3, next i = 123440
                error_index = decrease_group.start()
                i = int(
                    str_i[: error_index + 1]
                    + str_i[error_index]
                    + "0" * (4 - error_index)
                )
                # Note that the 4 here is a direct consequence of nmin, nmax being 6-digit long
                continue

            # Try to find adjacent digits in i that are the same
            if re.search(with_double, str_i) is not None:
                result += 1

            i += 1

        return result
