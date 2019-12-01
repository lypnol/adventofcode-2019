from tool.runners.python import SubmissionPy
from typing import Dict, List, Tuple


class BadouralixSubmission(SubmissionPy):

    def __init__(self):
        # Handmade memoization
        self.fuel_requirement_cache: Dict[int, int] = dict()

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        modules: List[str] = s.split("\n")

        total_fuel = 0
        total_function_calls = 0
        total_cache_hits = 0

        for module in modules:
            fuel, function_calls, cache_hits = self.fuel_requirement(mass=int(module))
            total_fuel += fuel
            total_function_calls += function_calls
            total_cache_hits += cache_hits

        # print(total_function_calls, total_cache_hits)

        return total_fuel

    def fuel_requirement(self, mass: int) -> Tuple[int, int, int]:
        if mass in self.fuel_requirement_cache:
            return self.fuel_requirement_cache[mass], 1, 1

        if mass < 9:
            self.fuel_requirement_cache[mass] = 0
            return self.fuel_requirement_cache[mass], 1, 0

        fuel = mass // 3 - 2
        fuel_for_fuel, function_calls, cache_hits = self.fuel_requirement(mass=fuel)

        self.fuel_requirement_cache[mass] = fuel + fuel_for_fuel

        return self.fuel_requirement_cache[mass], function_calls + 1, cache_hits
