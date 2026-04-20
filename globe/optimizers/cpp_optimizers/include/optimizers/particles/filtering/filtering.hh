/*
 * Created in 2026 by Gaëtan Serré
 */

#pragma once

#include "utils.hh"

class Filter
{
public:
  Filter() = default;

  virtual ~Filter() = default;

  virtual void step(Eigen::MatrixXd *particles_old, Eigen::MatrixXd *particles_new) = 0;
};

class QuantileFilter : public Filter
{
public:
  QuantileFilter() = default;
  ~QuantileFilter() = default;

  void step(Eigen::MatrixXd *particles_old, Eigen::MatrixXd *particles_new);
};
