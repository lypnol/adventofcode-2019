from tool.runners.python import SubmissionPy

width = 25
height = 6
image_size = width * height


class RemiSubmission(SubmissionPy):
    def run(self, s):
        layers = []
        layer = ""
        for n in s:
            if len(layer) < image_size:
                layer += n
            else:
                layers.append(layer)
                layer = n
        layers.append(layer)

        image = ["2" for i in range(image_size)]
        for i in range(width * height):
            for layer in layers:
                if image[i] == "2":
                    image[i] = layer[i]

        return "".join(image)

    def print_image(self, image):
        for i in range(height):
            for j in range(width):
                if image[width * i + j] == "1":
                    print("#", end="")
                else:
                    print(" ", end="")

            print("")
