/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/optimizer.hh"
#include "Cover_Tree.hh"

class Point
{
public:
  Point(dyn_vector x)
  {
    this->x = x;
  }

  double distance(const Point &p) const
  {
    return (this->x - p.x).norm();
  }

  double operator==(const Point &p) const
  {
    return this->x == p.x;
  }

  void print()
  {
    print_vector(this->x);
  }

  dyn_vector x;
};

typedef bool (*decision_f)(
    vector<result_eigen>,
    dyn_vector, vector<void *>,
    vector<void (*)(void)>);

typedef void (*callback_f)(
    vector<result_eigen>,
    vector<void *>,
    vector<void (*)(void)>);

class Decision : public Optimizer
{
public:
  Decision(
      vec_bounds bounds,
      int n_eval,
      int max_trials,
      vector<void *> data,
      vector<void (*)(void)> functions,
      decision_f decision,
      double trust_region_radius,
      int bobyqa_eval,
      callback_f callback = nullptr)
      : Optimizer(bounds, "Decision Optimizer")
  {
    this->n_eval = n_eval;
    this->max_trials = max_trials;
    this->data = data;
    this->functions = functions;
    this->decision = decision;
    this->callback = callback;
    this->trust_region_radius = trust_region_radius;
    this->bobyqa_eval = bobyqa_eval;
    if (trust_region_radius > 0)
    {
      this->use_trust_regions = true;
    }
  }

  virtual result_eigen minimize(function<double(dyn_vector)> f);

private:
  int n_eval;
  int max_trials;
  vector<void *> data;
  vector<void (*)(void)> functions;
  decision_f decision;
  callback_f callback;
  double trust_region_radius;
  int bobyqa_eval;
  bool use_trust_regions = false;
};