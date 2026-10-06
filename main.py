from src.fuzzy_mf import TriangularMF, TrapezoidalMF
from src.fuzzy_engine import SugenoEngine, MamdaniEngine
from src.fuzzy_set import LinguisticVariable
from src.fuzzy_rules import Rule, RuleBase, product
import pandas as pd
import time
import tracemalloc
import matplotlib.pyplot as plt


def measure(engine, cpu_mems, lat_mems):
    start = time.perf_counter()
    for _ in range(100):
        output, active = engine.infer(cpu_mems, lat_mems)
    elapsed_ms = (time.perf_counter() - start) * 1000 / 100
    
    tracemalloc.start()
    output, active = engine.infer(cpu_mems, lat_mems)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak / 1024
    
    return output, active, elapsed_ms, peak_kb
    
    
import yaml

MF_TYPES = {"triangular": TriangularMF, "trapezoidal": TrapezoidalMF}

def build_variable(name, spec):
    var = LinguisticVariable(name, *spec["range"])
    for term, t in spec["terms"].items():
        var.add_term(term, MF_TYPES[t["type"]](*t["params"]))
    return var

with open("config/rules_config.yaml") as f:
    config = yaml.safe_load(f)

cpu = build_variable("CPU", config["variables"]["cpu"])
latency = build_variable("Latency", config["variables"]["latency"])
replica = build_variable("ReplicaChange", config["variables"]["replica_change"])

rules = [Rule(r["cpu"], r["latency"], r["then"], r["sugeno"]) for r in config["rules"]]
rule_base = RuleBase(rules)


sugeno = SugenoEngine(rule_base)

mamdani = MamdaniEngine(rule_base, replica)


cpu_mems = cpu.fuzzify(70)
lat_mems = latency.fuzzify(600)

results = []
for name, engine in [("Mamdani", mamdani), ("Sugeno (TSK)", sugeno)]:
    output, active, ms, kb = measure(engine, cpu_mems, lat_mems)
    results.append({
        "Algorithm": name,
        "Output": round(float(output), 2),
        "Active rules": active,
        "Time (ms)": round(ms, 4),
        "Memory (KB)": round(kb, 2),
    })
    


print(pd.DataFrame(results).to_string(index=False))


sugeno_min   = SugenoEngine(rule_base)
sugeno_prod  = SugenoEngine(rule_base, product)
mamdani_min  = MamdaniEngine(rule_base, replica)
mamdani_prod = MamdaniEngine(rule_base, replica, product)

cpu_values = list(range(101))

def sweep(engine, latency_value=600):
    outs = [engine.infer(cpu.fuzzify(c), latency.fuzzify(latency_value))[0] for c in cpu_values]
    jumps = [abs(b - a) for a, b in zip(outs, outs[1:])]
    return outs, max(jumps), sum(jumps) / 100

s_min,  s_min_max,  s_min_avg  = sweep(sugeno_min)
m_min,  m_min_max,  m_min_avg  = sweep(mamdani_min)
s_prod, s_prod_max, s_prod_avg = sweep(sugeno_prod)
m_prod, m_prod_max, m_prod_avg = sweep(mamdani_prod)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

ax1.plot(cpu_values, s_min, label="Sugeno")
ax1.plot(cpu_values, m_min, label="Mamdani")
ax1.set_title("AND = min")

ax2.plot(cpu_values, s_prod, label="Sugeno")
ax2.plot(cpu_values, m_prod, label="Mamdani")
ax2.set_title("AND = product")

for ax in (ax1, ax2):
    ax.set_xlabel("CPU utilization (%)")
    ax.legend()
    ax.grid(True)
ax1.set_ylabel("ReplicaChange")

fig.suptitle("Controller output vs CPU (latency = 600 ms)")
plt.savefig("smoothness.png")
