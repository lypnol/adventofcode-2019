from tool.runners.python import SubmissionPy

import json
import numpy as np


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        arr = np.array(list(map(int, list(s))))
        arr = arr.reshape((-1, 6, 25))

        img = 2 * np.ones((6, 25))
        for i in range(arr.shape[0]):
            img = np.where(img == 2, arr[i, :, :], img)

        with open("day-08/alphabet.json", "r") as fp:
            letters = json.load(fp)

        password = []
        for i in range(0, 25, 5):
            letter_to_identify = img[:, i:i + 5]
            identified = False
            for key, value in letters.items():
                if np.all(letter_to_identify == value):
                    password.append(key)
                    identified = True
                    break
            if not identified:
                print(letter_to_identify)
        return "".join(password)
