from tool.runners.python import SubmissionPy

import math


class RemiSubmission(SubmissionPy):
    def run(self, s):

        elements = dict()

        for reaction in s.split("\n"):
            reactives, product = reaction.split("=>")

            product = product.strip()
            coeff, product = product.split(" ")
            coeff = int(coeff)

            product = elements.setdefault(product, Element(product, elements, coeff))
            product.coeff = coeff

            for reactive in reactives.split(","):
                reactive = reactive.strip()
                coeff, reactive = reactive.split(" ")
                coeff = int(coeff)

                elements.setdefault(reactive, Element(reactive, elements))
                product.reactives[reactive] = coeff

        elements["FUEL"].quantity = 1

        needed = [
            element
            for element in elements.values()
            if element.quantity > 0 and element.name != "ORE"
        ]
        while len(needed) > 0:
            needed[0].process()

            needed = [
                element
                for element in elements.values()
                if element.quantity > 0 and element.name != "ORE"
            ]

        return elements["ORE"].quantity


class Element:
    def __init__(self, name, elements, coeff=0):
        self.name = name
        self.coeff = coeff
        self.elements = elements

        self.reactives = dict()

        self.quantity = 0

    def process(self):

        mult = math.ceil(self.quantity / self.coeff)
        self.quantity -= mult * self.coeff

        for reactive, coeff in self.reactives.items():
            self.elements[reactive].quantity += coeff * mult
