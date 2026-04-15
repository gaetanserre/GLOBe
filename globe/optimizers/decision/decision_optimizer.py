#
# Created in 2025 by Gaëtan Serré
#

from ..cpp_optimizer import CPP_Optimizer


class Decision_Optimizer(CPP_Optimizer):
    """
    Interface for Stochastic Moment Dynamics optimizers.

    Parameters
    ----------
    name : str
        The name of the optimizer.
    bounds : ndarray
        The bounds of the search space.
    n_eval : int
        The maximum number of function evaluations.
    trust_region_dict : dict, optional
        Dictionary with the following keys:

        radius : float
            The trust region radius.
        bobyqa_eval : int
            The number of evaluations for the BOBYQA optimizer.

        If None, the trust region is not used.
    verbose : bool, optional
        Whether to print information about the optimization process.
    """

    def __init__(self, name, bounds, n_eval, trust_region_dict, verbose=False):
        if trust_region_dict is not None:
            try:
                self.trust_region_radius = trust_region_dict["radius"]
            except KeyError:
                raise ValueError(
                    "The trust region dictionary must contain the key 'radius'."
                )
            try:
                self.bobyqa_eval = trust_region_dict["bobyqa_eval"]
            except KeyError:
                raise ValueError(
                    "The trust region dictionary must contain the key 'bobyqa_eval'."
                )
        else:
            self.trust_region_radius = 0
            self.bobyqa_eval = 0

        if self.bobyqa_eval > 0:
            if n_eval < self.bobyqa_eval:
                self.bobyqa_eval = n_eval
                self.n_eval = 1
            else:
                self.n_eval = n_eval // self.bobyqa_eval
        else:
            self.n_eval = n_eval
        name = name + "+TR" if self.trust_region_radius > 0 else name
        super().__init__(name, bounds, verbose)
