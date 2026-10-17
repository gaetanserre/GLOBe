/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/particles/common-noise/GCN/GCN.hh"
#include "optimizers/particles/common-noise/GCN/GCN_CBO.hh"

void GCN_CBO::set_stop_criterion(double stop_criterion)
{
  this->stop_criterion = stop_criterion;
  this->has_stop_criterion = true;
  this->base_opt.set_stop_criterion(stop_criterion);
}

void GCN_CBO::set_seed(unsigned long long seed)
{
  Optimizer::set_seed(seed);
  this->base_opt.set_seed(seed);
}

result_eigen GCN_CBO::minimize(function<double(dyn_vector)> f)
{
  GCN gcn(&this->base_opt, this->sigma, this->name, this->independent_noise);
  return gcn.minimize(f);
}