def product(a, b):
    return a * b

class Rule:
    def __init__(self, cpu_term, lat_term, out_term, sugeno_value):
        self.cpu_term = cpu_term
        self.lat_term = lat_term
        self.out_term = out_term
        self.sugeno_value = sugeno_value

    def strength(self, cpu_mems, lat_mems, and_op=min):
        return and_op(cpu_mems[self.cpu_term], lat_mems[self.lat_term])
        
class RuleBase:
    def __init__(self, rules):
        self.rules = rules