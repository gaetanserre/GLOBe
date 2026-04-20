#
# Created in 2026 by Gaëtan Serré
#

from ..cpp_optimizer import CPP_Optimizer


class Particles_Optimizer(CPP_Optimizer):
    """
    Base class for particle-based optimizers with filtering capabilities.

    This class handles the parsing of filter_type parameter which determines
    how particles are filtered during optimization.

    Parameters
    ----------
    name : str
        The name of the optimizer.
    bounds : ndarray
        The bounds of the search space.
    filter_type : str or None, optional
        The type of filter to apply to particles:
        - None: No filtering (default)
        - "quantile": Filters out particles judged as non-relevant based on quantile
    verbose : bool, optional
        Whether to print information about the optimization process.
    """

    def __init__(self, name, bounds, filter_type=None, verbose=False):
        # Parse filter_type to C++ compatible integer
        self.filter_type_str = filter_type
        self.filter_type = self._parse_filter_type(filter_type)

        super().__init__(name, bounds, verbose)

    def _parse_filter_type(self, filter_type):
        """
        Parse filter_type string to C++ compatible integer.

        Parameters
        ----------
        filter_type : str or None
            The filter type specification.

        Returns
        -------
        int
            - 0 if filter_type is None (no filtering)
            - 1 if filter_type is "quantile" (quantile-based filtering)

        Raises
        ------
        ValueError
            If filter_type is not None or "quantile".
        """
        if filter_type is None:
            return 0
        elif filter_type == "quantile":
            return 1
        else:
            raise ValueError(
                f'Invalid filter_type: {filter_type}. Choose from None or "quantile".'
            )
