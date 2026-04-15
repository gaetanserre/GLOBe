#
# Created in 2024 by Gaëtan Serré
#

from .decision_optimizer import Decision_Optimizer
from ..cpp_optimizers import AdaRankOpt as C_AdaRankOpt


class AdaRankOpt(Decision_Optimizer):
    """
    Interface for the AdaRankOpt optimizer.

    Parameters
    ----------
    bounds : ndarray
        The bounds of the search space.
    n_eval : int
        The maximum number of function evaluations.
    max_trials : int
        The maximum number of potential candidates sampled at each iteration.
    max_degree : int
        The maximum degree of the polynomial kernel.
    it_lim : int
        The iteration limit for the simplex optimizer.
    trust_region_dict : dict, optional
        Dictionary with the following keys:

        radius : float
            The trust region radius.
        bobyqa_eval : int
            The number of evaluations for the BOBYQA optimizer.

        If None, the trust region is not used.
    verbose : bool
        Whether to print information about the optimization process.
    """

    def __init__(
        self,
        bounds,
        n_eval=1000,
        max_trials=50_000,
        max_degree=15,
        it_lim=100,
        trust_region_dict={"radius": 0.1, "bobyqa_eval": 20},
        verbose=False,
    ):
        super().__init__("AdaRankOpt", bounds, n_eval, trust_region_dict, verbose)

        self.c_opt = C_AdaRankOpt(
            bounds,
            self.n_eval,
            max_trials,
            max_degree,
            self.trust_region_radius,
            self.bobyqa_eval,
            it_lim,
        )
