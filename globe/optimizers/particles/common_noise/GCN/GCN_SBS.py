#
# Created in 2025 by Gaëtan Serré
#

from ...particles_optimizer import Particles_Optimizer
from ....cpp_optimizers import GCN_SBS as CGCN_SBS


class GCN_SBS(Particles_Optimizer):
    """
    Interface for the Geometric Common Noise SBS optimizer with optional particle filtering.

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
    sigma : float
        The kernel bandwidth.
    filter_type : str or None, optional
        The type of filter to apply to particles:
        - None: No filtering (default)
        - "quantile": Filters out particles judged as non-relevant based on quantile
    sigma_noise : float
        The kernel bandwidth for the common noise.
    verbose : bool
        Whether to print information about the optimization process.
    """

    def __init__(
        self,
        bounds,
        n_particles=200,
        iter=100,
        dt=0.1,
        sigma=0.1,
        filter_type=None,
        sigma_noise=1,
        verbose=False,
    ):
        super().__init__("GCN-SBS", bounds, filter_type=filter_type, verbose=verbose)

        self.c_opt = CGCN_SBS(
            bounds,
            n_particles,
            iter,
            dt,
            sigma,
            self.filter_type,
            sigma_noise,
        )
