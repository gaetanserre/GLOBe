from gob.benchmarks import *
from gob.optimizers import *


pygkls = PyGKLS(2, 15, [-100, 100], -100, smoothness="ND", gen=42)

f = Square()

bounds = augment_dimensions(f.visual_bounds, 2)  # f.visual_bounds

n_particles = 150
iter = 1000
sigma = 1 / n_particles**2
verbose = False

opt = AdaLIPO_P(bounds=bounds, n_eval=100, verbose=verbose)
res = opt.minimize(f)
print(f"Results for {opt} on {f}: {res[1]}")

opt = AdaRankOpt(bounds=bounds, n_eval=100, verbose=verbose)
res = opt.minimize(f)
print(f"Results for {opt} on {f}: {res[1]}")

opt = ECP(bounds=bounds, n_eval=100, verbose=verbose)
res = opt.minimize(f)
print(f"Results for {opt} on {f}: {res[1]}")
