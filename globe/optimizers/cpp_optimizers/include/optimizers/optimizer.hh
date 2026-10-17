/*
 * Created in 2024 by Gaëtan Serré
 */

#pragma once

#include <iostream>
#include "utils.hh"
using namespace std;

class Optimizer
{
public:
  Optimizer(vec_bounds bounds, string name)
  {
    // Py_Initialize();
    this->bounds = bounds;
    this->name = name;
    this->set_seed(chrono::system_clock::now().time_since_epoch().count());
  }

  ~Optimizer()
  {
    // Py_Finalize();
  }

  virtual result_eigen minimize(function<double(dyn_vector)> f) = 0;

  result py_minimize(PyObject *f);

  void set_stop_criterion(double stop_criterion)
  {
    this->stop_criterion = stop_criterion;
    this->has_stop_criterion = true;
  }

  // Seed of the random number generator. By default, it comes from the clock.
  virtual void set_seed(unsigned long long seed)
  {
    this->seed = seed;
    this->re.seed(seed);
  }

  unsigned long long get_seed()
  {
    return this->seed;
  }

  vec_bounds bounds;
  string name;
  mt19937_64 re;
  unsigned long long seed;

  bool has_stop_criterion = false;
  double stop_criterion;
};