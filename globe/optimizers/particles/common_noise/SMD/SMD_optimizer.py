#
# Created in 2025 by Gaëtan Serré
#

from ...particles_optimizer import Particles_Optimizer


class SMD_Optimizer(Particles_Optimizer):
    """
    Interface for Stochastic Moment Dynamics optimizers with particle filtering.

    This class extends Particles_Optimizer and handles the parsing of both
    filter_type and moment parameters specific to SMD algorithms.

    Parameters
    ----------
    name : str
        The name of the optimizer.
    bounds : ndarray
        The bounds of the search space.
    moment : str, optional
        The moment to use for the common noise. Can be "M1", "M2", "VAR", "MVAR".
    filter_type : str or None, optional
        The type of filter to apply to particles:
        - None: No filtering (default)
        - "quantile": Filters out particles judged as non-relevant based on quantile
    verbose : bool, optional
        Whether to print information about the optimization process.
    """

    def __init__(self, name, bounds, moment, filter_type=None, verbose=False):

        match moment:
            case "M1":
                self.moment = 0
            case "M2":
                self.moment = 1
            case "VAR":
                self.moment = 2
            case "MVAR":
                self.moment = 3
            case _:
                raise ValueError(
                    'Invalid moment type. Choose from "M1", "M2", "VAR", or "MVAR".'
                )

        super().__init__(
            "SMD-" + name, bounds, filter_type=filter_type, verbose=verbose
        )
