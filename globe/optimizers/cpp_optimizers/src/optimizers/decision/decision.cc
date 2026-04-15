/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/decision/decision.hh"
#include "optimizers/decision/bobyqa.hh"

bool check_in_ball(const CoverTree<Point> &cTree, const dyn_vector &x, const double &radius)
{
  Point px = Point(x);
  vector<Point> points = cTree.kNearestNeighbors(px, 1);
  if (points.size() == 0)
  {
    return false;
  }
  else
  {
    return points[0].distance(px) <= radius;
  }
}

result_eigen Decision::minimize(function<double(dyn_vector)> f)
{
  CoverTree<Point> cTree;
  vector<result_eigen> samples;

  auto compare_pair = [](result_eigen a, result_eigen b) -> bool
  {
    return a.second < b.second;
  };

  for (int i = 0; i < this->n_eval; i++)
  {
    int count = 0;
    while (true)
    {
      dyn_vector x = unif_random_vector(this->re, this->bounds);
      count++;
      if (this->use_trust_regions)
      {
        if (check_in_ball(cTree, x, this->trust_region_radius))
        {
          continue;
        }
      }

      if ((*this->decision)(samples, x, this->data, this->functions))
      {
        if (this->use_trust_regions)
        {
          Point px = Point(x);
          cTree.insert(px);
          result_eigen bobyqa_res = run_bobyqa(
              this->bounds,
              x,
              this->trust_region_radius,
              this->bobyqa_eval,
              f);
          samples.push_back({bobyqa_res.first, -bobyqa_res.second});
        }
        else
        {
          samples.push_back({x, -f(x)});
        }
        sort(samples.begin(), samples.end(), compare_pair);
        break;
      }

      if (count >= this->max_trials)
      {
        result_eigen best = samples.back();
        return {best.first, -best.second};
      }
    }

    result_eigen best = samples.back();
    if (this->has_stop_criterion && -best.second <= this->stop_criterion)
    {
      return {best.first, -best.second};
    }

    if (this->callback != nullptr)
    {
      (*this->callback)(samples, this->data, this->functions);
    }
  }

  result_eigen best = samples.back();
  return {best.first, -best.second};
}