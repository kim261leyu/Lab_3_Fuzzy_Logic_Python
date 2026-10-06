import numpy as np

class SugenoEngine:
    def __init__(self, rule_base, and_op=min):
        self.rule_base = rule_base
        self.and_op = and_op

    def infer(self, cpu_mems, lat_mems):
        numerator = 0
        denominator = 0
        active = 0
        for rule in self.rule_base.rules:
           w = rule.strength(cpu_mems, lat_mems, self.and_op)
           if w > 0:
               active += 1
               numerator += w * rule.sugeno_value
               denominator += w
               
        if denominator == 0:
            return 0, 0
            
        return numerator / denominator, active


import numpy as np

class MamdaniEngine:
    def __init__(self, rule_base, out_var, and_op=min):
        self.rule_base = rule_base
        self.out_var = out_var
        self.y = np.linspace(-3, 5, 801)
        self.and_op = and_op
        
    def infer(self, cpu_mems, lat_mems):
        active_rules = []                      
        for rule in self.rule_base.rules:
            w = rule.strength(cpu_mems, lat_mems, self.and_op)
            if w > 0:
                shape = self.out_var.terms[rule.out_term]
                active_rules.append((w, shape))

        active = len(active_rules)    
        
        heights = []
        for y in self.y:
            height = 0.0
            for w, shape in active_rules:
                height = max(height, min(w, shape.evaluate(y)))
            heights.append(height)
         
        total = sum(heights)
        if total == 0:
            return 0, 0
        result = sum(y * h for y, h in zip(self.y, heights)) / total
        return float(result), active