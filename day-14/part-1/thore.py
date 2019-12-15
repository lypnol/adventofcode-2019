from collections import defaultdict, OrderedDict
from math import ceil
import re

from tool.runners.python import SubmissionPy

BASE_REAGENT = "ORE"
TARGET = "FUEL"


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        recipes = parse_reactions(s)

        return solve_part1(recipes)


def parse_reactions(s):
    prog = re.compile("(\d+) ([A-Z]+),? ?")
    recipes = {}

    for line in s.splitlines():
        reagents_str, products_str = [g.strip() for g in line.split("=>")]
        match = prog.match(line)
        reagents = [(int(qty), name) for (qty, name) in prog.findall(reagents_str)]
        product_qty, product_name = (
            int(prog.findall(products_str)[0][0]),
            prog.findall(products_str)[0][1],
        )
        recipes[product_name] = {"qty": product_qty, "reagents": reagents}

    recipes[BASE_REAGENT] = {"qty": 1, "reagents": []}
    return recipes


def solve_part1(recipes):
    used_for_map = get_used_for_map(recipes)
    sorted_elements = topological_sort(used_for_map)

    quantities = defaultdict(int)
    quantities[TARGET] = 1
    for element in sorted_elements:
        for qty, reagent in recipes[element]["reagents"]:
            quantities[reagent] += (
                ceil(quantities[element] / recipes[element]["qty"]) * qty
            )

    return quantities[BASE_REAGENT]


def get_used_for_map(recipes):
    used_for_map = defaultdict(list)
    for product, recipe in recipes.items():
        for qty, reagent in recipe["reagents"]:
            used_for_map[reagent].append(product)
    return used_for_map


def topological_sort(used_for_map):
    visited = OrderedDict()

    def visit(node):
        if node in visited:
            return
        for reagent in used_for_map[node]:
            visit(reagent)
        visited[node] = True

    visit(BASE_REAGENT)
    return visited.keys()
