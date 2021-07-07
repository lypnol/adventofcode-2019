from tool.runners.python import SubmissionPy
import numpy as np

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        arr = np.array(list(map(int, list(s))))
        arr = arr.reshape((-1, 6, 25))
        best_index = np.argmin(np.sum(arr == 0, axis=(1, 2)))
        return np.sum(arr[best_index, :, :] == 1) * np.sum(arr[best_index, :, :] == 2)

