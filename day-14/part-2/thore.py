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

        return solve_part2(recipes, ore_qty=1_000_000_000_000)


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


def solve_part2(recipes, ore_qty):
    used_for_map = get_used_for_map(recipes)
    sorted_elements = topological_sort(used_for_map)

    ore_per_fuel = get_ore_needed(recipes, sorted_elements)
    fuel = ore_qty // ore_per_fuel

    ore_needed = get_ore_needed(recipes, sorted_elements, target_qty=fuel)
    prev_fuel = None
    while fuel != prev_fuel:
        prev_fuel = fuel
        fuel += (ore_qty - ore_needed) // ore_per_fuel
        ore_needed = get_ore_needed(recipes, sorted_elements, target_qty=fuel)

    # here fuel should be a lower bound close to the true value

    while ore_needed < ore_qty:
        fuel += 1
        ore_needed = get_ore_needed(recipes, sorted_elements, target_qty=fuel)

    return fuel - 1


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


def get_ore_needed(recipes, sorted_elements, target_qty=1):
    quantities = defaultdict(int)
    quantities[TARGET] = target_qty
    for element in sorted_elements:
        for qty, reagent in recipes[element]["reagents"]:
            quantities[reagent] += (
                ceil(quantities[element] / recipes[element]["qty"]) * qty
            )

    return quantities[BASE_REAGENT]
