#
# Created in 2024 by Gaëtan Serré
#

from .particles_optimizer import Particles_Optimizer
from ..cpp_optimizers import Langevin as C_Langevin


class MSGD(Particles_Optimizer):
    """
    Interface for the Multi-Start Gradient Descent optimizer with optional particle filtering.

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
        iter=100,
        dt=0.1,
        batch_size=0,
        filter_type=None,
        verbose=False,
    ):
        super().__init__("MSGD", bounds, filter_type=filter_type, verbose=verbose)
        self.c_opt = C_Langevin(
            bounds, n_particles, iter, dt, 0, batch_size, self.filter_type
        )
