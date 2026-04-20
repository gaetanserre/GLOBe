#
# Created in 2025 by Gaëtan Serré
#

from .SMD_optimizer import SMD_Optimizer
from ....cpp_optimizers import SMD_PSO as CSMD_PSO


class SMD_PSO(SMD_Optimizer):
    """
    Interface for the Stochastic Moment Dynamics PSO optimizer with optional particle filtering.

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
    beta : float
        The inverse temperature.
    alpha : float
        The coefficient to decrease the step size.
    filter_type : str or None, optional
        The type of filter to apply to particles:
        - None: No filtering (default)
        - "quantile": Filters out particles judged as non-relevant based on quantile
    gamma : float
        The coefficient for the common noise.
    ``lambda_`` : float
        The regularization parameter for the common noise.
    delta : float
        The parameter for the Bessel process.
    moment : str
        The type of moment used for the common noise ("M1" | "M2" | "VAR" | "MVAR").
    verbose : bool
        Whether to print information about the optimization process.
    """

    def __init__(
        self,
        bounds,
        n_particles=200,
        iter=1000,
        dt=0.1,
        beta=1e5,
        alpha=1,
        gamma=1,
        lambda_=1e-10,
        delta=2.1,
        moment="M1",
        filter_type=None,
        verbose=False,
    ):
        super().__init__(
            "PSO", bounds, moment, filter_type=filter_type, verbose=verbose
        )

        self.c_opt = CSMD_PSO(
            bounds,
            n_particles,
            iter,
            dt,
            beta,
            alpha,
            self.filter_type,
            gamma,
            lambda_,
            delta,
            self.moment,
        )
