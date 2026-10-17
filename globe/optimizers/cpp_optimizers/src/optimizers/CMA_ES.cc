/*
 * Created in 2024 by Gaëtan Serré
 */

#include "optimizers/CMA_ES.hh"

using namespace libcmaes;

void CMA_ES::transform_bounds(vec_bounds bounds)
{
  const int dim = this->bounds.size();
  this->lbounds = new double[dim];
  this->ubounds = new double[dim];
  for (int i = 0; i < dim; i++)
  {
    this->lbounds[i] = this->bounds[i][0];
    this->ubounds[i] = this->bounds[i][1];
  }
}

pair<CMASolutions, GenoPheno<pwqBoundStrategy>> CMA_ES::get_sols(function<double(dyn_vector)> f)
{
  // Without a user-given initial mean, a new one is drawn uniformly at each run
  vector<double> m0 = this->m0;
  if (m0.size() == 0)
  {
    int n = this->bounds.size();
    m0 = vector<double>(n);
    for (int i = 0; i < n; i++)
    {
      m0[i] = unif_random_double(re, bounds[i][0], bounds[i][1]);
    }
  }

  GenoPheno<pwqBoundStrategy> gp(this->lbounds, this->ubounds, m0.size());
  // libcmaes samples with its own generator, whose seed is drawn from ours (0 would mean a seed
  // from the clock)
  uint64_t cma_seed = this->re();
  CMAParameters<GenoPheno<pwqBoundStrategy>> cmaparams(m0, this->sigma, this->lambda, cma_seed == 0 ? 1 : cma_seed, gp);
  if (this->has_stop_criterion)
  {
    cmaparams.set_ftarget(this->stop_criterion);
  }
  cmaparams.set_max_fevals(this->n_eval);

  FitFunc f_ = [&f](const double *x, const int N)
  {
    dyn_vector xvec = dyn_vector::Map(x, N);
    return f(xvec);
  };
  CMASolutions cmasols = cmaes<GenoPheno<pwqBoundStrategy>>(f_, cmaparams);
  return {cmasols, gp};
}

result_eigen CMA_ES::minimize(function<double(dyn_vector)> f)
{
  pair<CMASolutions, GenoPheno<pwqBoundStrategy>> sols_gp = get_sols(f);
  CMASolutions cmasols = sols_gp.first;
  GenoPheno<pwqBoundStrategy> gp = sols_gp.second;
  dyn_vector best_x = gp.pheno(cmasols.get_best_seen_candidate().get_x_dvec());
  double best_f = cmasols.get_best_seen_candidate().get_fvalue();

  return {best_x, best_f};
}