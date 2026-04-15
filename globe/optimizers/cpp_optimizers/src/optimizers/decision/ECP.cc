/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/decision/ECP.hh"
#include "optimizers/decision/decision.hh"

namespace ECP_decision
{
  bool decision(
      vector<result_eigen> samples,
      dyn_vector x, vector<void *> data,
      vector<void (*)(void)> functions)
  {
    if (samples.size() == 0)
      return true;

    double *epsilon = (double *)data[0];
    int *h1 = (int *)data[1];
    int *h2 = (int *)data[2];
    int *C = (int *)data[3];
    double *theta = (double *)data[4];

    *h2 = *h2 + 1;
    if (*h2 - *h1 > *C)
    {
      *epsilon = *epsilon * *theta;
      *h2 = 0;
    }
    double max_values = samples.back().second;
    vector<double> norms(samples.size());
    for (int i = 0; i < samples.size(); i++)
    {
      norms[i] = samples[i].second + *epsilon * (x - samples[i].first).norm();
    }
    bool res = max_values <= min_vec(norms);
    if (res)
    {
      *h1 = *h2;
      *epsilon = *epsilon * *theta;
      *h2 = 0;
    }
    return res;
  }
};

result_eigen ECP::minimize(function<double(dyn_vector)> f)
{
  int h1 = 1, h2 = 0;

  vector<void *> data(5);
  data[0] = (void *)&this->epsilon;
  data[1] = (void *)&h1;
  data[2] = (void *)&h2;
  data[3] = (void *)&this->C;
  data[4] = (void *)&this->theta;

  vector<void (*)(void)> functions(0);

  Decision dec = Decision(
      this->bounds,
      this->n_eval,
      this->max_trials,
      data,
      functions,
      &ECP_decision::decision,
      this->trust_region_radius,
      this->bobyqa_eval);

  if (this->has_stop_criterion)
    dec.set_stop_criterion(this->stop_criterion);

  return dec.minimize(f);
}