from tool.runners.python import SubmissionPy


def compute_wire(instructions):
    wire = set()
    x, y = (0, 0)
    for instr in instructions.split(","):
        val = int(instr[1:])
        if instr[0] == "R":
            for dx in range(1, val + 1):
                wire.add((x + dx, y))
            x += val
        elif instr[0] == "L":
            for dx in range(1, val + 1):
                wire.add((x - dx, y))
            x -= val
        elif instr[0] == "U":
            for dy in range(1, val + 1):
                wire.add((x, y + dy))
            y += val
        elif instr[0] == "D":
            for dy in range(1, val + 1):
                wire.add((x, y - dy))
            y -= val

    return wire


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # s = "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"
        # s = "R8,U5,L5,D3\nU7,R6,D4,L4"
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        instr1, instr2 = s.splitlines()
        wire1 = compute_wire(instr1)
        wire2 = compute_wire(instr2)
        common = wire1.intersection(wire2)
        return min(abs(x) + abs(y) for x, y in common)
