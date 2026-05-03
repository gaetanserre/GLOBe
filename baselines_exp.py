#
# Created in 2025 by Gaëtan Serré
#

from utils import (
    print_avg_rank,
    print_competitive_ratios,
    noisy_functions,
    noisy_functions_bounds,
)

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gob import GOB

n_particles = 150
iter = 300
sigma = 1 / n_particles**2
n_runs = 50

if __name__ == "__main__":
    algorithms = [
        (
            "CMA-ES",
            {
                "n_eval": n_particles * iter,
            },
        ),
        (
            "SMD-CBO",
            {
                "n_particles": n_particles,
                "iter": iter,
                "moment": "MVAR",
            },
        ),
        (
            "GCN-CBO",
            {
                "n_particles": n_particles,
                "iter": iter,
            },
        ),
        (
            "SMD-SBS",
            {
                "n_particles": n_particles,
                "iter": iter,
                "sigma": sigma,
                "moment": "MVAR",
            },
        ),
        (
            "GCN-SBS",
            {
                "n_particles": n_particles,
                "iter": iter,
                "sigma": sigma,
            },
        ),
        (
            "SMD-Langevin",
            {
                "n_particles": n_particles,
                "iter": iter,
                "moment": "MVAR",
            },
        ),
        (
            "GCN-Langevin",
            {
                "n_particles": n_particles,
                "iter": iter,
            },
        ),
        (
            "SMD-MSGD",
            {
                "n_particles": n_particles,
                "iter": iter,
                "moment": "MVAR",
            },
        ),
        (
            "GCN-MSGD",
            {
                "n_particles": n_particles,
                "iter": iter,
            },
        ),
    ]

    # noisy
    gob = GOB(
        algorithms,
        noisy_functions,
        [],
        bounds=noisy_functions_bounds,
    )
    print("Running noisy functions experiments...")
    res_dict, ratios = gob.run(
        n_runs=n_runs, verbose=1, latex_table=True, reference_optimizer="CMA-ES"
    )
    print_avg_rank(res_dict)
    print_competitive_ratios(ratios)
