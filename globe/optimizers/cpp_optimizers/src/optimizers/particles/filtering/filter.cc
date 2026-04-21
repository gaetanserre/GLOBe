/*
 * Created in 2026 by Gaëtan Serré
 */

#include "optimizers/particles/filtering/filtering.hh"

void QuantileFilter::step(Eigen::MatrixXd *particles_old, Eigen::MatrixXd *particles_new)
{
  // Only filter if we have enough particles
  if (particles_new->rows() <= 10)
    return;

  int n_particles = particles_new->rows();
  int n_dims = particles_new->cols();

  // Calculate distances: L2 norm between each particle_old and particle_new
  Eigen::VectorXd distance(n_particles);
  for (int i = 0; i < n_particles; ++i)
  {
    distance(i) = (particles_old->row(i) - particles_new->row(i)).norm();
  }

  // Calculate x_values: L2 norm of each particle_new
  Eigen::VectorXd x_values(n_particles);
  for (int i = 0; i < n_particles; ++i)
  {
    x_values(i) = particles_new->row(i).norm();
  }

  // Calculate quantiles
  std::vector<double> dist_vec(distance.data(), distance.data() + n_particles);
  std::sort(dist_vec.begin(), dist_vec.end());
  double dist_quantile = dist_vec[static_cast<int>(n_particles * 0.5)]; // Default to 0.5

  std::vector<double> val_vec(x_values.data(), x_values.data() + n_particles);
  std::sort(val_vec.begin(), val_vec.end());
  double value_quantile = val_vec[static_cast<int>(n_particles * 0.3)]; // Default to 0.3

  // Create masks and combined filter mask
  Eigen::VectorXi valid(n_particles);
  int n_valid = 0;

  for (int i = 0; i < n_particles; ++i)
  {
    bool dist_mask = distance(i) < dist_quantile;
    bool value_mask = x_values(i) > value_quantile;
    bool keep = !(dist_mask && value_mask); // Keep if NOT (both conditions)

    if (keep)

    {
      valid(n_valid) = i;
      n_valid++;
    }
  }

  // Modify particles_new in place: keep only valid particles
  for (int i = 0; i < n_valid; ++i)
  {
    particles_new->row(i) = particles_new->row(valid(i));
  }

  // Resize the matrix to contain only valid particles
  particles_new->conservativeResize(n_valid, n_dims);
}