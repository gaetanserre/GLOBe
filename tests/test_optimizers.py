from globe.benchmarks import *
import globe.optimizers as go
import inspect


pygkls = PyGKLS(2, 15, [-100, 100], -100, smoothness="ND", gen=42)

f = Square()

bounds = f.visual_bounds

optimizers = inspect.getmembers(go, inspect.isclass)
for _, opt in optimizers:
    opt = opt(bounds=bounds)
    res = opt.minimize(f)
    print(f"Results for {opt} on {f}: {res[1]}")
