#
# Created in 2025 by Gaëtan Serré
#

from .SMD_optimizer import SMD_Optimizer
from ....cpp_optimizers import SMD_CBO as CSMD_CBO


class SMD_CBO(SMD_Optimizer):
    """
    Interface for the Stochastic Moment Dynamics CBO optimizer with optional particle filtering.

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
    gamma : float
        The coefficient for the common noise.
    ``lambda_`` : float
        The regularization parameter for the common noise.
    delta : float
        The parameter for the Bessel process.
    moment : str
        The type of moment used for the common noise ("M1" | "M2" | "VAR" | "MVAR").
    independent_noise : bool
        Whether to use independent noise or not.
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
        gamma=1,
        lambda_=1e-10,
        delta=2.1,
        moment="M1",
        independent_noise=True,
        verbose=False,
    ):
        super().__init__(
            "CBO", bounds, moment, filter_type=filter_type, verbose=verbose
        )

        self.c_opt = CSMD_CBO(
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
            gamma,
            lambda_,
            delta,
            self.moment,
            independent_noise,
        )
