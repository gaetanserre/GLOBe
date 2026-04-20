/*
 * Created in 2026 by Gaëtan Serré
 */

#include "optimizers/particles/filtering/filtering.hh"

void QuantileFilter::step(Eigen::MatrixXd *particles_old, Eigen::MatrixXd *particles_new)
{
  printf("QuantileFilter\n");
  if (particles_new->rows() <= 10)
    return;
  else
    return;
}