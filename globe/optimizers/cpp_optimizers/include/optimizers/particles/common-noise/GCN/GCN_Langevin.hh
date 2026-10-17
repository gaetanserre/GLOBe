/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/particles/Langevin.hh"

class GCN_Langevin : public Optimizer
{
public:
  GCN_Langevin(
      vec_bounds bounds,
      int n_particles,
      int iter,
      double dt,
      double beta,
      int filter_type,
      int warmup_type,
      int warmup_iter,
      double sigma_cn,
      bool independent_noise = true) : Optimizer(bounds, "GCN-Langevin"),
                                       base_opt(bounds, n_particles, iter, dt, beta, 0, filter_type, warmup_type, warmup_iter)
  {
    // The base optimizer draws all the random numbers, with the seed of this one
    this->set_seed(this->seed);
    this->sigma = sigma_cn;
    this->independent_noise = independent_noise;
  }

  virtual void set_stop_criterion(double stop_criterion);
  virtual void set_seed(unsigned long long seed);
  virtual result_eigen minimize(function<double(dyn_vector)> f);

private:
  Langevin base_opt;
  double sigma;
  bool independent_noise = true;
};