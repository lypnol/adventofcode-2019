from tool.runners.python import SubmissionPy

import math


class RemiSubmission(SubmissionPy):
    def run(self, s):

        ore = 1000000000000

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

        # heuristic of the quantity of ore needed for one fuel, it is a majorant
        quantity = self.one(elements)

        needed = []
        while elements["ORE"].quantity < ore:
            if len(needed) == 0:

                # estimate the quantity of FUEL we can still produce
                to_add = (ore - elements["ORE"].quantity) // quantity
                if to_add == 0:
                    # if we think we cannot produce anything anymore let's try one more, we should be near the end anyway
                    to_add = 1
                elements["FUEL"].quantity = to_add
            else:
                needed[0].process()

            needed = [
                element
                for element in elements.values()
                if element.quantity > 0 and element.name != "ORE"
            ]

        # we maybe overshot by one fuel
        if elements["ORE"].quantity > ore:
            elements["FUEL"].producted -= 1

        return elements["FUEL"].producted

    def one(self, elements):
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

        self.producted = 0

    def process(self):

        mult = math.ceil(self.quantity / self.coeff)
        self.quantity -= mult * self.coeff

        self.producted += mult * self.coeff

        for reactive, coeff in self.reactives.items():
            self.elements[reactive].quantity += coeff * mult
