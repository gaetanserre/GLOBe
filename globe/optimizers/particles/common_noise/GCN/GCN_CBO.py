#
# Created in 2025 by Gaëtan Serré
#

from ...particles_optimizer import Particles_Optimizer
from ....cpp_optimizers import GCN_CBO as CGCN_CBO


class GCN_CBO(Particles_Optimizer):
    """
    Interface for the Geometric Common Noise CBO optimizer with optional particle filtering.

    Parameters
    ----------
    bounds : ndarray
        The bounds of the search space.
    n_particles : int
        The number of particles.
    iter : int
        The number of iterations.
    dt : float
        The time step.
    lam : float
        The attraction parameter.
    epsilon : float
        The smooth-heaviside parameter.
    beta : float
        The inverse temperature.
    sigma : float
        The standard deviation of the Gaussian noise.
    alpha : float
        The coefficient to decrease the step size.
    filter_type : str or None, optional
        The type of filter to apply to particles:
        - None: No filtering (default)
        - "quantile": Filters out particles judged as non-relevant based on quantile
    warmup_type : str or None, optional
        The type of warmup to apply to particles:
        - None: No warmup (default)
        - "CMA-ES": Uses CMA-ES to warm up the particles
    warmup_iter : int, optional
        The number of warmup iterations. Default is 0.
    sigma_noise : float
        The kernel bandwidth for the common noise.
    independent_noise : bool
        Whether to use independent noise for each particle.
    verbose : bool
        Whether to print information about the optimization process.
    """

    def __init__(
        self,
        bounds,
        n_particles=200,
        iter=1000,
        dt=0.1,
        lam=1,
        epsilon=1e-2,
        beta=1,
        sigma=5.1,
        alpha=1,
        filter_type=None,
        sigma_noise=1,
        independent_noise=True,
        verbose=False,
        warmup_type=None,
        warmup_iter=0,
    ):
        super().__init__(
            "GCN-CBO",
            bounds,
            filter_type=filter_type,
            warmup_type=warmup_type,
            verbose=verbose,
        )

        self.c_opt = CGCN_CBO(
            bounds,
            n_particles,
            iter,
            dt,
            lam,
            epsilon,
            beta,
            sigma,
            alpha,
            self.filter_type,
            self.warmup_type,
            warmup_iter,
            sigma_noise,
            independent_noise,
        )
