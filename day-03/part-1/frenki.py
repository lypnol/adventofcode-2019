from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        l1,l2 = s.splitlines()
        l1 = l1.split(',')
        l2 = l2.split(',')
        v1 = self.create_v(l1)
        v2 = self.create_v(l2)
        res = -1
        for i in range(len(v1)-1):
            for j in range(len(v2)-1):
                if self.in_order(v1[i][0], v2[j][0]) != self.in_order(v1[i+1][0], v2[j+1][0]) and self.in_order(v1[i][1], v2[j][1]) != self.in_order(v1[i+1][1], v2[j+1][1]):
                    if v1[i][0] == v1[i+1][0]:
                        dist = abs(v1[i][0]) + abs(v2[j][1])
                    else :
                        dist = abs(v1[i][1]) + abs(v2[j][0])
                    if  dist < res :
                        res = dist
                    elif res == -1 :
                        res = dist
        return res


    
    def create_v(self, l):
        v = [(0,0)]
        for m in l:
            letter = m[0]
            if letter == 'U':
                v.append((v[-1][0], v[-1][1] - int(m[1:])))
            elif letter == 'D':
                v.append((v[-1][0], v[-1][1] + int(m[1:])))
            elif letter == 'L':
                v.append((v[-1][0] - int(m[1:]), v[-1][1]))
            else :
                v.append((v[-1][0] + int(m[1:]), v[-1][1]))
        return v
    
    def in_order(self, x, y):
        return x < y