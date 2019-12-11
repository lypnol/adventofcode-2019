from tool.runners.python import SubmissionPy

def get_optcode_param(n):
    return (n%100, [(n//100)%10, (n//1000)%10, n//10000])

class IntCode(object):
    def __init__(self, l):
        self.l = l
        self.out = None

    def choose(self, v, m):
        if m == 0:
            return self.l[v]
        return v

    def add(self, args, i):
        self.l[args[2]] =  self.l[args[1]] + self.l[args[0]]
        return i+4

    def mul(self, args, i):
        self.l[args[2]] =  self.l[args[1]] * self.l[args[0]]
        return i+4
    
    def ins(self, args, i):
        self.l[args[0]] = 5
        return i+2

    def ret(self, args, i):
        self.out = self.l[args[0]]
        return i+2
    
    def jump_true(self, args, i):
        return self.l[args[1]] if self.l[args[0]] else i+3
    
    def jump_false(self, args, i):
        return self.l[args[1]] if not self.l[args[0]] else i+3

    def less_than(self, args, i):
        self.l[args[2]] = 1 if self.l[args[0]] < self.l[args[1]] else 0
        return i+4

    def equals(self, args, i):
        self.l[args[2]] = 1 if self.l[args[0]] == self.l[args[1]] else 0
        return i+4

    def run(self):
        i = 0
        opcodes = [0,(self.add, 3), (self.mul, 3), (self.ins,1), (self.ret, 1), (self.jump_true, 2), (self.jump_false, 2), (self.less_than, 3), (self.equals, 3)]
        while self.l[i] != 99:
            opcode, params = get_optcode_param(self.l[i])
            f,r = opcodes[opcode]
            l = [self.choose(i+k+1,params[k]) for k in range(r)]
            i = f(l, i)
            if self.out:
                return self.out


class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        ic = IntCode([int(i) for i in s.split(',')])
        return ic.run()
