/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/particles/common-noise/SMD/SMD.hh"
#include "optimizers/particles/common-noise/SMD/SMD_SBS.hh"

void SMD_SBS::set_stop_criterion(double stop_criterion)
{
  this->stop_criterion = stop_criterion;
  this->has_stop_criterion = true;
  this->base_opt.set_stop_criterion(stop_criterion);
}

void SMD_SBS::set_seed(unsigned long long seed)
{
  Optimizer::set_seed(seed);
  this->base_opt.set_seed(seed);
}

result_eigen SMD_SBS::minimize(function<double(dyn_vector)> f)
{
  SMD smd(&this->base_opt, this->gamma, this->lambda, this->delta, static_cast<NoiseType>(this->moment), this->name, false);
  return smd.minimize(f);
}