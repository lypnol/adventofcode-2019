from tool.runners.python import SubmissionPy
import itertools


class RemiSubmission(SubmissionPy):
    def run(self, s):
        inp = [int(i) for i in list(s)]
        self.pattern = [0, 1, 0, -1]

        for _ in range(100):
            inp = [
                abs(
                    sum(
                        n * m
                        for n, m in zip(
                            inp,
                            itertools.islice(
                                itertools.cycle(
                                    itertools.chain(
                                        *(
                                            itertools.repeat(p, i + 1)
                                            for p in self.pattern
                                        )
                                    )
                                ),
                                1,
                                None,
                            ),
                        )
                    )
                )
                % 10
                for i in range(len(inp))
            ]

        return "".join([str(i) for i in inp[:8]])
