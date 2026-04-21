#
# Created in 2025 by Gaëtan Serré
#

from .SMD_optimizer import SMD_Optimizer
from ....cpp_optimizers import SMD_SBS as CSMD_SBS


class SMD_SBS(SMD_Optimizer):
    """
    Interface for the Stochastic Moment Dynamics SBS optimizer with optional particle filtering.

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
        iter=100,
        dt=0.1,
        sigma=0.1,
        filter_type=None,
        gamma=1,
        lambda_=1e-10,
        delta=2.1,
        moment="M1",
        verbose=False,
    ):
        super().__init__(
            "SBS", bounds, moment, filter_type=filter_type, verbose=verbose
        )

        self.c_opt = CSMD_SBS(
            bounds,
            n_particles,
            iter,
            dt,
            sigma,
            self.filter_type,
            gamma,
            lambda_,
            delta,
            self.moment,
        )
