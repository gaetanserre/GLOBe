#
# Created in 2024 by Gaëtan Serré
#

from .particles_optimizer import Particles_Optimizer
from ..cpp_optimizers import CBO as C_CBO


class CBO(Particles_Optimizer):
    """
    Interface for the CBO optimizer with optional particle filtering.

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
    batch_size : int
        The batch size for the mini-batch optimization. If 0, no mini-batch
        optimization is used.
    filter_type : str or None, optional
        The type of filter to apply to particles:
        - None: No filtering (default)
        - "quantile": Filters out particles judged as non-relevant based on quantile
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
        batch_size=0,
        filter_type=None,
        verbose=False,
    ):
        super().__init__("CBO", bounds, filter_type=filter_type, verbose=verbose)
        self.c_opt = C_CBO(
            bounds,
            n_particles,
            iter,
            dt,
            lam,
            epsilon,
            beta,
            sigma,
            alpha,
            batch_size,
            self.filter_type,
        )
