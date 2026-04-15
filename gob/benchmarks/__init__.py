#
# Created in 2024 by Gaëtan Serré
#

from .create_bounds import create_bounds, augment_dimensions
from .multimodal.ackley import Ackley
from .unimodal.bentcigar import Bentcigar
from .multimodal.deb import Deb
from .unimodal.dixonprice import Dixonprice
from .multimodal.griewank import Griewank
from .unimodal.hyperellipsoid import Hyperellipsoid
from .multimodal.langermann import Langermann
from .multimodal.levy import Levy
from .multimodal.michalewicz import Michalewicz
from .multimodal.rastrigin import Rastrigin
from .unimodal.rosenbrock import Rosenbrock
from .multimodal.schwefel import Schwefel
from .unimodal.square import Square
from .multimodal.styblinskitang import Styblinskitang
from .unimodal.sumpow import Sumpow
from .unimodal.trid import Trid
from .unimodal.zakharov import Zakharov
from .multimodal.pygkls import PyGKLS

__all__ = [
    "create_bounds",
    "augment_dimensions",
    "PyGKLS",
    "Ackley",
    "Bentcigar",
    "Deb",
    "Dixonprice",
    "Griewank",
    "Hyperellipsoid",
    "Langermann",
    "Levy",
    "Levy",
    "Michalewicz",
    "Rastrigin",
    "Rosenbrock",
    "Schwefel",
    "Square",
    "Styblinskitang",
    "Sumpow",
    "Trid",
    "Zakharov",
]
