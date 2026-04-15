/*
 * Created in 2024 by Gaëtan Serré
 */

#include "optimizers/decision/AdaRankOpt.hh"
#include "optimizers/decision/PolynomialFeatures.hh"
#include "optimizers/decision/Simplex.hh"
#include "optimizers/decision/decision.hh"

Eigen::MatrixXd AdaRankOpt::polynomial_matrix(vector<result_eigen> &samples, int degree)
{
  int n = samples.size() - 1;
  int d = samples[0].first.size();
  int n_out = comp(d + degree, d) - 1;
  Eigen::MatrixXd M = Eigen::MatrixXd::Zero(n_out, n);
  for (int i = 0; i < n; i++)
  {
    dyn_vector poly = polynomial_features(samples[i + 1].first, degree) - polynomial_features(samples[i].first, degree);
    for (int j = 0; j < n_out; j++)
    {
      M(j, i) = poly(j);
    }
  }
  return M;
}

namespace AdaRankOpt_decision
{
  bool decision(
      vector<result_eigen> samples,
      dyn_vector x, vector<void *> data,
      vector<void (*)(void)> functions)
  {
    if (samples.size() == 0)
      return true;
    int *degree = (int *)data[0];
    glp_smcp *param = (glp_smcp *)data[1];
    Eigen::MatrixXd (*polynomial_matrix)(vector<result_eigen>, int) =
        (Eigen::MatrixXd (*)(vector<result_eigen>, int))functions[0];
    double f_x_tmp = samples.back().second + 1;
    samples.push_back({x, f_x_tmp});
    Eigen::MatrixXd M = polynomial_matrix(samples, *degree);
    samples.pop_back();
    return simplex(M, param) == GLP_NOFEAS;
  }

  void callback(
      vector<result_eigen> samples,
      vector<void *> data,
      vector<void (*)(void)> functions)
  {
    if (samples.size() >= 2)
    {
      int *degree = (int *)data[0];
      glp_smcp *param = (glp_smcp *)data[1];
      int *max_degree = (int *)data[2];
      Eigen::MatrixXd (*polynomial_matrix)(vector<result_eigen>, int) =
          (Eigen::MatrixXd (*)(vector<result_eigen>, int))functions[0];
      while (*degree < *max_degree)
      {
        Eigen::MatrixXd M = polynomial_matrix(samples, *degree);
        if (simplex(M, param) == GLP_NOFEAS)
          break;
        *degree = *degree + 1;
      }
    }
  }
}

result_eigen AdaRankOpt::minimize(function<double(dyn_vector)> f)
{
  int degree = 1;

  vector<void *> data(3);
  data[0] = (void *)&degree;
  data[1] = (void *)this->param;
  data[2] = (void *)&this->max_degree;
  vector<void (*)(void)> functions(1);
  functions[0] = (void (*)(void))&AdaRankOpt::polynomial_matrix;

  Decision dec = Decision(
      this->bounds,
      this->n_eval,
      this->max_trials,
      data,
      functions,
      &AdaRankOpt_decision::decision,
      this->trust_region_radius,
      this->bobyqa_eval,
      &AdaRankOpt_decision::callback);

  if (this->has_stop_criterion)
    dec.set_stop_criterion(this->stop_criterion);

  return dec.minimize(f);
}
