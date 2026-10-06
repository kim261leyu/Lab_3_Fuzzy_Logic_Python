class TriangularMF:
    def __init__(self, a, b, c):  
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, x):
        if x <= self.a or x >= self.c: #not in a range
            return 0.0                              
        if x == self.b:                 # at a peak
            return 1.0                           
        if x < self.b:                  # before peak
            return (x - self.a) / (self.b - self.a)
        return (self.c - x) / (self.c - self.b)   #after peak
        
        
class TrapezoidalMF:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def evaluate(self, x):
        if self.b <= x <= self.c:
            return 1.0
        if x <= self.a or x >= self.d:
            return 0.0
        if x < self.b:
            return (x - self.a) / (self.b - self.a)
        return (self.d - x) / (self.d - self.c)