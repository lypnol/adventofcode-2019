import collections
from functools import lru_cache
from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    @staticmethod
    def parse_input(s):
        reactions = {}
        
        def parse_el(el):
            nb, name = el.split(" ")
            return name, int(nb)

        for l in s.splitlines():
            inputs, output = l.split(" => ")
            output_name, qty_produced = parse_el(output)
            reactions[output_name] = {
                "inputs": [parse_el(el) for el in inputs.split(", ")],
                "qty_produced": qty_produced,
            }

        return reactions

    @staticmethod
    def get_complexity(reactions):
        complexity = {}

        @lru_cache(maxsize=2**10)
        def _get_complexity(name):
            if name == "ORE":
                return 0
            else:
                inputs = reactions[name]["inputs"]
                return max(complexity.get(name, _get_complexity(name)) for name, _ in inputs) + 1

        for output_name, reaction in reactions.items():
            complexity[output_name] = _get_complexity(output_name)

        return complexity

    @staticmethod
    def compute_nb_of_ore_needed(nb_of_fuel, reactions, complexity):
        total = 0
        to_produce = collections.defaultdict(int, {"FUEL": nb_of_fuel})

        while to_produce:
            # find most complext element to produce
            most_complex_el = max(to_produce, key=lambda el: complexity[el])
            qty_to_produce = to_produce[most_complex_el]

            # find recipy
            reaction = reactions[most_complex_el]
            n_produced = reaction["qty_produced"]
            n_reaction = (qty_to_produce-1) // n_produced + 1 

            # update to produce
            del to_produce[most_complex_el]
            for (name, qty) in reaction["inputs"]:
                if name == "ORE":
                    total += qty * n_reaction
                else:
                    to_produce[name] += qty * n_reaction          

        return total

    def run(self, s):
        reactions = self.parse_input(s)
        complexity = self.get_complexity(reactions)

        too_low = 0
        too_high = 100000000 
        nb_of_fuel = 500000
        while True:
            nb_of_needed_ore = self.compute_nb_of_ore_needed(nb_of_fuel, reactions, complexity)

            if nb_of_needed_ore > 10 ** 12:
                too_high = nb_of_fuel
            else:
                if too_high == nb_of_fuel + 1:
                    return nb_of_fuel
                else:
                    too_low = nb_of_fuel
            nb_of_fuel = (too_high + too_low) // 2