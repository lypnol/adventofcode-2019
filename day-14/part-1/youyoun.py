from tool.runners.python import SubmissionPy

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
        total_cost = 0
        leftovers = {}
        reqs = {"FUEL": 1}
        while reqs:
            chem_needed, quant_needed = reqs.popitem() # resource needed
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
                quant_produced, _ = [e for e in reactions if e[1] == chem_needed][0] # Given formula
                if quant_needed <= quant_produced: # Quant desired
                    ratio = 1
                else:
                    ratio = quant_needed // quant_produced + (0 if quant_needed % quant_produced == 0 else 1)
                leftovers[chem_needed] = quant_produced * ratio - quant_needed
                for e in reactions[(quant_produced, chem_needed)]: # Get formula inputs
                    produced = e[0] * ratio
                    if e[1] in reqs:
                        reqs[e[1]] += produced
                    else:
                        reqs[e[1]] = produced
        return total_cost



