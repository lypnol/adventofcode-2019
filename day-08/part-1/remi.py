from tool.runners.python import SubmissionPy

width = 25
height = 6


class RemiSubmission(SubmissionPy):
    def run(self, s):
        layers = []
        layer = []
        for n in [int(i) for i in list(s)]:
            if len(layer) < (width * height):
                layer.append(n)
            else:
                layers.append(layer)
                layer = [n]

        min_layer = min(layers, key=lambda layer: layer.count(0))

        return min_layer.count(1) * min_layer.count(2)
