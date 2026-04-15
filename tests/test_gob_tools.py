from gob.benchmarks import *
import gob.optimizers as go
import inspect


pygkls = PyGKLS(2, 15, [-100, 100], -100, smoothness="ND", gen=42)

f = Square()

bounds = augment_dimensions(f.visual_bounds, 2)  # f.visual_bounds

n_particles = 150
iter = 1000
sigma = 1 / n_particles**2
verbose = False

optimizers = inspect.getmembers(go, inspect.isclass)
for _, opt in optimizers:
    opt = opt(bounds=bounds)
    res = opt.minimize(f)
    print(f"Results for {opt} on {f}: {res[1]}")
