from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def run(self, s):
        base_data = list(map(int, s.split(",")))
        data = base_data[::]
        i = 0

        def get_param(offset):
            mode = (data[i] // 10 ** (1 + offset)) % 10
            return data[data[i + offset]] if mode == 0 else data[i + offset]

        input_value = 5
        outputs = []
        while True:
            opcode = data[i] % 100
            if opcode == 1:
                data[data[i + 3]] = get_param(1) + get_param(2)
                i += 4
            elif opcode == 2:
                data[data[i + 3]] = get_param(1) * get_param(2)
                i += 4
            elif opcode == 3:
                data[data[i + 1]] = input_value
                i += 2
            elif opcode == 4:
                outputs.append(get_param(1))
                i += 2
            elif opcode == 5:
                if get_param(1) != 0:
                    i = get_param(2)
                else:
                    i += 3
            elif opcode == 6:
                if get_param(1) == 0:
                    i = get_param(2)
                else:
                    i += 3
            elif opcode == 7:
                data[data[i + 3]] = 1 if get_param(1) < get_param(2) else 0
                i += 4
            elif opcode == 8:
                data[data[i + 3]] = 1 if get_param(1) == get_param(2) else 0
                i += 4
            elif opcode == 99:
                break
            else:
                raise Exception(f"Not a valid opcode: {opcode}")
        return outputs[-1]
