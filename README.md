## Global Optimization Benchmark (GLOBe)

[![CI](https://github.com/gaetanserre/GLOBe/actions/workflows/build.yml/badge.svg)](https://github.com/gaetanserre/GLOBe/actions/workflows/build.yml)
[![CI](https://github.com/gaetanserre/GLOBe/actions/workflows/build_doc.yml/badge.svg)](https://github.com/gaetanserre/GLOBe/actions/workflows/build_doc.yml)
[![PyPI version](https://badge.fury.io/py/globe-opti.svg)](https://badge.fury.io/py/globe-opti)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

<p align="center">
  <img src="docs/_static/logo.png" alt="GLOBe Logo" width="250"/>
</p>


GLOBe is a collection of global optimization algorithms implemented in C++ and linked with Python. It also includes a set of analytical benchmark functions and a random function generator ([PyGKLS](https://github.com/gaetanserre/pyGKLS)) to test the performance of these algorithms.

### Algorithms

- [AdaLIPO+](https://dl.acm.org/doi/full/10.1145/3688671.3688763)
- [AdaRankOpt](https://arxiv.org/abs/1603.04381)
- [Bayesian Optimization](https://github.com/bayesian-optimization/BayesianOptimization)
- [CMA-ES](https://github.com/CMA-ES/libcmaes)
- [Controlled Random Search](http://dx.doi.org/10.1007/BF00933504)
- [DIRECT](http://dx.doi.org/10.1007/0-306-48332-7_93)
- [Every Call is Precious](https://arxiv.org/abs/2502.04290?)
- [Multi-Level Single-Linkage](https://ageconsearch.umn.edu/record/272327)
- [*Social Only* Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968)
- [Langevin dynamics](https://archive.org/details/rcin.org.pl.WA35_226705_8818_Art15_194893)
- [Stein Boltzmann Sampling](https://arxiv.org/abs/2402.04689)
- [Consensus Based Optimization](https://arxiv.org/abs/1909.09249)
- [Common noise variants of McKean-Vlasov dynamics](https://arxiv.org/abs/2601.22753)
- Gradient Descent
- Multi-start Gradient Descent
- Pure Random Search

### Documentation

The documentation is available at [gaetanserre.fr/GLOBe](https://gaetanserre.fr/GLOBe/).

### Installation (Python ≥ 3.10)

Install the package via pip from PyPI:
```bash
pip install globe-opti
```

Alternatively, download the corresponding wheel file from the [releases](https://github.com/gaetanserre/GLOBe/releases) and install it with pip:
```bash
pip install globe-opti-<version>-<architecture>.whl
```

### Build from source

Make sure you have CMake (≥ 3.28), a c++ compiler, and the eigen3 library installed. Then clone the repository and run:
```bash
pip install . -v
```
It should build the C++ extensions and install the package. You can also build the documentation with:
```bash
cd docs
pip install -r requirements.txt
make html
```

### Usage

This package can be used to design a complete benchmarking framework for global optimization algorithms, testing multiple algorithms on a set of benchmark functions. See [`test_globe.py`](tests/test_globe_tools.py) for an example of how to use it.

The global optimization algorithms can also be used independently. For example, to run the AdaLIPO+ algorithm on a benchmark function:

```python
from globe.optimizers import AdaLIPO_P
from globe import create_bounds

f = lambda x: return x.T @ x

opt = AdaLIPO_P(create_bounds(2, -5, 5), 300)
res = opt.minimize(f)
print(f"Optimal point: {res[0]}, Optimal value: {res[1]}")
```
See [`test_optimizers.py`](tests/test_optimizers.py) for more examples of how to use the algorithms.

### Contributing

Contributions are welcome! Please see the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines.

### References

- [BayesianOptimization](https://github.com/bayesian-optimization/BayesianOptimization)
- [libcames](https://github.com/CMA-ES/libcmaes)
- [nlopt-python](https://github.com/DanielBok/nlopt-python)

### License

This is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
