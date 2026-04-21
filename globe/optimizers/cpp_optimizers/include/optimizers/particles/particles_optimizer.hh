/*
 * Created in 2025 by Gaëtan Serré
 */

#pragma once

#include "optimizers/optimizer.hh"
#include "optimizers/particles/schedulers.hh"
#include "optimizers/particles/filtering/filtering.hh"

enum FilterType
{
  NONE = 0,
  QUANTILE = 1
};

struct dynamic
{
  Eigen::MatrixXd drift;
  Eigen::MatrixXd noise;
};

class Particles_Optimizer : public Optimizer
{
public:
  Particles_Optimizer(
      vec_bounds bounds,
      int n_particles,
      int iter,
      int batch_size,
      Scheduler *sched,
      int filter_type = FilterType::NONE,
      std::string name = "Particles Optimizer") : Optimizer(bounds, name)
  {
    this->n_particles = n_particles;
    this->iter = iter;
    this->batch_size = batch_size;
    this->sched = sched;
    if (filter_type == FilterType::QUANTILE)
    {
      this->filter = new QuantileFilter();
    }
  }

  ~Particles_Optimizer()
  {
  }

  virtual result_eigen minimize(function<double(dyn_vector)> f);

  virtual dynamic compute_dynamics(const Eigen::MatrixXd &particles, const function<double(dyn_vector x)> &f, vector<double> *evals, const int &time) = 0;
  int n_particles;
  int iter;
  int batch_size;
  Scheduler *sched;
  Filter *filter = nullptr;

private:
  void update_particles(Eigen::MatrixXd *particles, function<double(dyn_vector x)> f, vector<double> *all_evals, vector<dyn_vector> *samples, int &t);
};