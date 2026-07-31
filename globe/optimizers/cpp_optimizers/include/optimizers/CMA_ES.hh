/*
 * Created in 2024 by Gaëtan Serré
 */

#include "optimizers/optimizer.hh"
#include "libcmaes/cmaes.h"

using namespace libcmaes;

class CMA_ES : public Optimizer
{
public:
  CMA_ES(
      vec_bounds bounds,
      int n_eval,
      std::vector<double> m0,
      double sigma) : Optimizer(bounds, "CMA-ES")
  {
    this->n_eval = n_eval;
    this->m0 = m0;
    this->sigma = sigma;

    this->transform_bounds(bounds);
  }

  ~CMA_ES()
  {
    delete[] lbounds;
    delete[] ubounds;
  }

  virtual pair<CMASolutions, GenoPheno<pwqBoundStrategy>> get_sols(function<double(dyn_vector)> f);
  virtual result_eigen minimize(function<double(dyn_vector)> f);

private:
  virtual void transform_bounds(vec_bounds bounds);
  int n_eval;
  double *lbounds;
  double *ubounds;
  std::vector<double> m0;
  double sigma;
};