from tool.runners.python import SubmissionPy
from itertools import permutations

def get_optcode_param(n):
    L = list(str(n))
    c = (L[-1], L[:-2][::-1])
    while len(c[1]) < 3:
        c[1].append('0')
    return c

class FrenkiSubmission(SubmissionPy):
    def __init__(self):
        self.l = []

    def choose(self, v, m):
        if m == '0':
            return self.l[v]
        return v

    def run(self, s):
        res = 0
        dic = {}
        for i in list(permutations([0,1,2,3,4])):
            input_value = 0
            for k in range(5):
                self.l = list(map(int, s.split(',')))
                if (i[k], input_value) in dic.keys():
                    input_value = dic[(i[k], input_value)]
                else :
                    v = input_value
                    input_value = self.run_intcode(i[k], input_value)
                    dic[(i[k], v)] = input_value
            if input_value > res:
                res = input_value
        return res


    def run_intcode(self, index, input_value):
        l = [input_value, index]
        i = 0
        while self.l[i] != 99:
            c = get_optcode_param(self.l[i])
            if c[0] == '1':
                index1 = self.choose(i+1, c[1][0])
                index2 = self.choose(i+2, c[1][1])
                index3 = self.choose(i+3, c[1][2])
                self.l[index3] = self.l[index1] + self.l[index2]
                i+= 4
            elif c[0] == '2':
                index1 = self.choose(i+1, c[1][0])
                index2 = self.choose(i+2, c[1][1])
                index3 = self.choose(i+3, c[1][2])
                self.l[index3] = self.l[index1] * self.l[index2]
                i += 4
            elif c[0] == '3':
                index1 = self.l[i+1]
                self.l[index1] = l.pop()
                i+= 2
            elif c[0] == '4':
                index1 = self.choose(i+1, c[1][0])
                return(self.l[index1])
            elif c[0] == '5':
                index1 = self.choose(i+1, c[1][0])
                index2 = self.choose(i+2, c[1][1])
                if self.l[index1]:
                    i = self.l[index2]
                else :
                    i += 3
            elif c[0] == '6':
                index1 = self.choose(i+1, c[1][0])
                index2 = self.choose(i+2, c[1][1])
                if not self.l[index1]:
                    i = self.l[index2]
                else :
                    i += 3
            elif c[0] == '7':
                index1 = self.choose(i+1, c[1][0])
                index2 = self.choose(i+2, c[1][1])
                index3 = self.choose(i+3, c[1][2])
                if self.l[index1] < self.l[index2]:
                    self.l[index3] = 1
                else :
                    self.l[index3] = 0
                i += 4
            elif c[0] == '8':
                index1 = self.choose(i+1, c[1][0])
                index2 = self.choose(i+2, c[1][1])
                index3 = self.choose(i+3, c[1][2])
                if self.l[index1] == self.l[index2]:
                    self.l[index3] = 1
                else :
                    self.l[index3] = 0
                i += 4