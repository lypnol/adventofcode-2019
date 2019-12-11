from tool.runners.python import SubmissionPy

def get_optcode_param(n):
    return (n%100, [(n//100)%10, (n//1000)%10, n//10000])

class IntCode(object):
    def __init__(self, l):
        self.l = l

    def choose(self, v, m):
        if m == 0:
            return self.l[v]
        return v

    def add(self, args):
        self.l[args[2]] =  self.l[args[1]] + self.l[args[0]]

    def mul(self, args):
        self.l[args[2]] =  self.l[args[1]] * self.l[args[0]]
    
    def ins(self, args):
        self.l[args[0]] = 1

    def ret(self, args):
        return self.l[args[0]]

    def run(self):
        i = 0
        opcodes = [0,(self.add, 3), (self.mul, 3), (self.ins,1), (self.ret, 1)]
        while self.l[i] != 99:
            opcode, params = get_optcode_param(self.l[i])
            f,r = opcodes[opcode]
            l = [self.choose(i+k+1,params[k]) for k in range(r)]
            res = f(l)
            i += r+1
            if res:
                return res


class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        ic = IntCode([int(i) for i in s.split(',')])
        return ic.run()
        