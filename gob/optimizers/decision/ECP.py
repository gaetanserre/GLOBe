#
# Created in 2024 by Gaëtan Serré
#

from .decision_optimizer import Decision_Optimizer
from ..cpp_optimizers import ECP as C_ECP


class ECP(Decision_Optimizer):
    """
    Interface for the ECP+TR optimizer.

    Parameters
    ----------
    bounds : ndarray
        The bounds of the search space.
    n_eval : int
        The maximum number of function evaluations.
    epsilon : float
        The initial Lipschitz constant estimate.
    theta_init : float
        The scaling factor for epsilon.
    C : float
        How many candidates to sample before increasing epsilon.
    max_trials : int
        The maximum number of potential candidates sampled at each iteration.
    trust_region_dict : dict, optional
        Dictionary with the following keys:

        radius : float
            The trust region radius.
        bobyqa_eval : int
            The number of evaluations for the BOBYQA optimizer.

        If None, the trust region is not used.
    verbose : bool
        Whether to print information about the optimization
    """

    def __init__(
        self,
        bounds,
        n_eval=50,
        epsilon=1e-2,
        theta_init=1.001,
        C=1000,
        max_trials=10_000_000,
        trust_region_dict={"radius": 0.1, "bobyqa_eval": 20},
        verbose=False,
    ):
        super().__init__("ECP", bounds, n_eval, trust_region_dict, verbose)

        self.c_opt = C_ECP(
            bounds,
            self.n_eval,
            epsilon,
            theta_init,
            C,
            max_trials,
            self.trust_region_radius,
            self.bobyqa_eval,
        )
