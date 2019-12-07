from tool.runners.python import SubmissionPy
from itertools import permutations

def get_optcode_param(n):
    L = list(str(n))
    c = (L[-1], L[:-2][::-1])
    while len(c[1]) < 3:
        c[1].append('0')
    return c

class Intcode(object):
    def __init__(self, phase,s):
        self.output = None
        self.input = [phase]
        self.l = list(map(int, s.split(',')))
        self.index = 0

    def choose(self, v, m):
        if m == '0':
            return self.l[v]
        return v

    def run_intcode(self):
        while self.l[self.index] != 99:
            c = get_optcode_param(self.l[self.index])
            if c[0] == '1':
                index1 = self.choose(self.index+1, c[1][0])
                index2 = self.choose(self.index+2, c[1][1])
                index3 = self.choose(self.index+3, c[1][2])
                self.l[index3] = self.l[index1] + self.l[index2]
                self.index+= 4
            elif c[0] == '2':
                index1 = self.choose(self.index+1, c[1][0])
                index2 = self.choose(self.index+2, c[1][1])
                index3 = self.choose(self.index+3, c[1][2])
                self.l[index3] = self.l[index1] * self.l[index2]
                self.index += 4
            elif c[0] == '3':
                index1 = self.l[self.index+1]
                if not self.input :
                    return self.output
                self.l[index1] = self.input.pop()
                self.index+= 2
            elif c[0] == '4':
                index1 = self.choose(self.index+1, c[1][0])
                self.output = self.l[index1]
                self.index += 2
            elif c[0] == '5':
                index1 = self.choose(self.index+1, c[1][0])
                index2 = self.choose(self.index+2, c[1][1])
                if self.l[index1]:
                    self.index = self.l[index2]
                else :
                    self.index += 3
            elif c[0] == '6':
                index1 = self.choose(self.index+1, c[1][0])
                index2 = self.choose(self.index+2, c[1][1])
                if not self.l[index1]:
                    self.index = self.l[index2]
                else :
                    self.index += 3
            elif c[0] == '7':
                index1 = self.choose(self.index+1, c[1][0])
                index2 = self.choose(self.index+2, c[1][1])
                index3 = self.choose(self.index+3, c[1][2])
                if self.l[index1] < self.l[index2]:
                    self.l[index3] = 1
                else :
                    self.l[index3] = 0
                self.index += 4
            elif c[0] == '8':
                index1 = self.choose(self.index+1, c[1][0])
                index2 = self.choose(self.index+2, c[1][1])
                index3 = self.choose(self.index+3, c[1][2])
                if self.l[index1] == self.l[index2]:
                    self.l[index3] = 1
                else :
                    self.l[index3] = 0
                self.index += 4
        return self.output

def compute(s, phases):
    objs = []
    for i in range(5):
        objs.append(Intcode(phases[i],s))
    i = 0
    objs[0].input.insert(0, 0)
    while True:
        v = objs[i%5].run_intcode()
        if v :
            objs[(i+1)%5].input.insert(0,v)
            objs[(i+1)%5].output = None
        else :
            return objs[-1].output
        i+= 1


class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        r = 0
        for phase in permutations(range(5,10)):
            res = compute(s, phase)
            if res and  res > r:
                r = res
        return r

        