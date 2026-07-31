/*
 * Created in 2025 by Gaëtan Serré
 */

#include "optimizers/particles/particles_optimizer.hh"
#include "optimizers/CMA_ES.hh"

void Particles_Optimizer::update_particles(Eigen::MatrixXd *particles, function<double(dyn_vector x)> f, vector<double> *all_evals, vector<dyn_vector> *samples, int &t)
{
  Eigen::MatrixXd *particles_old_ptr;
  if (this->filter != nullptr)
  {
    particles_old_ptr = new Eigen::MatrixXd(*particles);
  }

  vector<double> evals((*particles).rows());
  for (int i = 0; i < particles->rows(); i++)
  {
    samples->push_back((*particles).row(i));
  }

  dynamic dyn = this->compute_dynamics(*particles, f, &evals, t);

  // Drift update
  this->sched->step(particles, dyn.drift, t);
  double dt = this->sched->get_dt();

  // Noise update
  for (int j = 0; j < particles->rows(); j++)
  {
    all_evals->push_back(evals[j]);
    particles->row(j) += sqrt(dt) * dyn.noise.row(j);
    particles->row(j) = clip_vector(particles->row(j), this->bounds);
  }
  if (this->filter != nullptr)
  {
    this->filter->step(particles_old_ptr, particles);
  }
}

void init_particles(int n_particles, vec_bounds bounds, function<double(dyn_vector)> f,
                    Eigen::MatrixXd *particles)
{
  vector<double> m0(0);
  CMA_ES cma_es(bounds, 1000, m0, 1);
  pair<CMASolutions, GenoPheno<pwqBoundStrategy>> sols_gp = cma_es.get_sols(f);
  CMASolutions cmasols = sols_gp.first;
  GenoPheno<pwqBoundStrategy> gp = sols_gp.second;

  std::vector<Candidate> &cands = cmasols.candidates();

  for (int i = 0; i < cmasols.size(); i++)
  {
    Candidate &c = cands[i];

    Eigen::VectorXd x_pheno = gp.pheno(c.get_x_dvec());
    particles->row(i) = x_pheno.transpose();
  }
}

result_eigen Particles_Optimizer::minimize(function<double(dyn_vector)> f)
{
  vector<double> all_evals;
  vector<dyn_vector> samples;
  Eigen::MatrixXd particles(this->n_particles, this->bounds.size());

  if (this->warmup_type == WarmUpType::CMAES && this->warmup_iter > 0)
  {
    init_particles(this->warmup_iter, this->bounds, f, &particles);
  }
  else
  {
    for (int i = 0; i < this->n_particles; i++)
    {
      particles.row(i) = unif_random_vector(this->re, this->bounds);
    }
  }
  for (int i = 0; i < this->iter; i++)
  {
    if (this->batch_size > 0)
    {
      if (particles.rows() < this->batch_size)
      {
        string msg = "Batch size (" + to_string(this->batch_size) + ") cannot be larger than the number of particles (" + to_string(particles.rows()) + ").";
        throw runtime_error(msg);
      }
      if (particles.rows() % this->batch_size != 0)
      {
        string msg = "Number of particles (" + to_string(particles.rows()) + ") must be a multiple of the batch size (" + to_string(this->batch_size) + ").";
        throw runtime_error(msg);
      }

      vector<int> perm(particles.rows());
      for (size_t j = 0; j < perm.size(); ++j)
      {
        perm[j] = j;
      }
      std::shuffle(perm.begin(), perm.end(), this->re);

      Eigen::MatrixXd batch_particles(this->batch_size, particles.cols());
      for (int j = 0; j < this->batch_size; j++)
      {
        batch_particles.row(j) = particles.row(perm[j]);
      }
      this->update_particles(&batch_particles, f, &all_evals, &samples, i);
      for (int j = 0; j < this->batch_size; j++)
      {
        particles.row(perm[j]) = batch_particles.row(j);
      }
    }
    else

      this->update_particles(&particles, f, &all_evals, &samples, i);

    if (this->has_stop_criterion && min_vec(all_evals) <= this->stop_criterion)
      break;
  }
  int argmin = argmin_vec(all_evals);
  return {samples[argmin], all_evals[argmin]};
}