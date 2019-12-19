from tool.runners.python import SubmissionPy

def ore_cost(reactions, n_fuel_produced):
    total_cost = 0
    leftovers = {}
    reqs = {"FUEL": n_fuel_produced}
    while reqs:
        chem_needed, quant_needed = reqs.popitem()  # resource needed
        if chem_needed in leftovers:
            if leftovers[chem_needed] >= quant_needed:
                leftovers[chem_needed] -= quant_needed
                continue
            else:
                quant_needed -= leftovers[chem_needed]
                leftovers[chem_needed] = 0
        if chem_needed == "ORE":
            total_cost += quant_needed
        else:
            quant_produced, _ = [e for e in reactions if e[1] == chem_needed][0]  # Given formula
            if quant_needed <= quant_produced:  # Quant desired
                ratio = 1
            else:
                ratio = quant_needed // quant_produced + (0 if quant_needed % quant_produced == 0 else 1)
            leftovers[chem_needed] = quant_produced * ratio - quant_needed
            for e in reactions[(quant_produced, chem_needed)]:  # Get formula inputs
                produced = e[0] * ratio
                if e[1] in reqs:
                    reqs[e[1]] += produced
                else:
                    reqs[e[1]] = produced
    return total_cost

class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        reactions = {}
        for reac in s.splitlines():
            input_, output_ = reac.split("=>")
            input_ = input_.replace(",","").split()
            quant, out = output_.split()
            reactions[(int(quant), out)] = set()
            for i in range(0, len(input_), 2):
                reactions[(int(quant), out)].add((int(input_[i]), input_[i+1]))
        total_ore = 1000000000000
        cost_per_fuel = ore_cost(reactions, 1)
        estimated_fuel = total_ore // cost_per_fuel

        lower = estimated_fuel
        upper = 2 * estimated_fuel
        while True:
            total_cost = ore_cost(reactions, (lower + upper) // 2)
            if total_cost < total_ore:
                lower = (lower + upper) // 2
            elif total_cost == total_ore:
                break
            else:
                upper = (lower + upper) // 2
            if upper - lower == 1:
                break
        return lower



