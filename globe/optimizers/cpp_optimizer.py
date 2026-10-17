#
# Created in 2025 by Gaëtan Serré
#

from .optimizer import Optimizer


class CPP_Optimizer(Optimizer):
    """
    Interface for C++ based optimizers.

    Parameters
    ----------
    name : str
        The name of the optimizer.
    bounds : ndarray
        The bounds of the search space.
    verbose : bool
        Whether to print information about the optimization process.
    """

    def __init__(self, name, bounds, verbose=False):
        super().__init__(name, bounds)

        self.c_opt = None  # To be defined in subclasses
        self.verbose = verbose

    def minimize(self, f):
        if self.verbose:
            f = self.verbose_function(f)
        return self.c_opt.minimize(f)

    def set_stop_criterion(self, stop_criterion):
        self.c_opt.set_stop_criterion(stop_criterion)

    def set_seed(self, seed):
        """
        Set the seed of the random number generator. By default, it comes from the clock.

        Parameters
        ----------
        seed : int
            The seed, a non-negative integer.
        """
        self.c_opt.set_seed(seed)

    def get_seed(self):
        """
        Seed of the random number generator.

        Returns
        -------
        int
            The seed.
        """
        return self.c_opt.get_seed()

    def __del__(self):
        del self.c_opt
