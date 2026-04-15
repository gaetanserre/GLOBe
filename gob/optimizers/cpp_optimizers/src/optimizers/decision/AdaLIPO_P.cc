/*
 * Created in 2024 by Gaëtan Serré
 */

#include "optimizers/decision/AdaLIPO_P.hh"
#include "optimizers/decision/decision.hh"

namespace AdaLIPO_P_decision
{
  bool decision(
      vector<result_eigen> samples,
      dyn_vector x, vector<void *> data,
      vector<void (*)(void)> functions)
  {
    if (samples.size() == 0)
      return true;
    double *k_hat = (double *)data[0];
    vector<double> norms(samples.size());
    for (int i = 0; i < samples.size(); i++)
    {
      norms[i] = samples[i].second + *k_hat * (x - samples[i].first).norm();
    }
    double max_values = samples.back().second;
    return max_values <= min_vec(norms);
  }

  void callback(
      vector<result_eigen> samples,
      vector<void *> data,
      vector<void (*)(void)> functions)
  {
    if (samples.size() >= 2)
    {
      double *k_hat = (double *)data[0];
      vector<double> *ratios = (vector<double> *)data[1];
      double alpha = 1e-2;
      dyn_vector x = samples.back().first;
      double value = samples.back().second;
      for (int i = 0; i < samples.size() - 1; i++)
      {
        (*ratios).push_back(abs(value - samples[i].second) / (x - samples[i].first).norm());
      }
      int i = ceil(log(max_vec(*ratios)) / log(1 + alpha));
      *k_hat = pow(1 + alpha, i);
    }
  }
}

result_eigen AdaLIPO_P::minimize(function<double(dyn_vector)> f)
{
  double k_hat = 0;
  vector<double> ratios;

  vector<void *> data(2);
  data[0] = (void *)&k_hat;
  data[1] = (void *)&ratios;

  vector<void (*)(void)> functions(0);

  Decision dec = Decision(
      this->bounds,
      this->n_eval,
      this->max_trials,
      data,
      functions,
      &AdaLIPO_P_decision::decision,
      this->trust_region_radius,
      this->bobyqa_eval,
      &AdaLIPO_P_decision::callback);

  if (this->has_stop_criterion)
    dec.set_stop_criterion(this->stop_criterion);

  return dec.minimize(f);
}