

class LinguisticVariable:
    def __init__(self, name, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.terms = dict()
  
    def add_term(self, name, mf):
        self.terms[name] = mf
        
    def fuzzify(self, x):
        return {name: mf.evaluate(x) for name, mf in self.terms.items()}