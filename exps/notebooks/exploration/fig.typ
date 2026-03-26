#set page(width: 40cm, height: 39cm)

#set par(justify: true)

#set text(font: "New Computer Modern", size: 12pt)

#v(-5em)

#grid(
  columns: 3,
  align(center, [CBO]) + image("exploration_cbo.svg"),
  align(center, [SMD-CBO Mean+Var]) + image("exploration_smd_cbo.svg"),
  align(center, [GCN-CBO]) + image("exploration_gcn_cbo.svg"),

  image("exploration_cbo_min.svg", width: 100%) + align(center, [CBO minimum value over iterations]),
  image("exploration_smd_cbo_min.svg", width: 100%) + align(center, [SMD-CBO minimum value over iterations]),
  image("exploration_gcn_cbo_min.svg", width: 100%) + align(center, [GCN-CBO minimum value over iterations]),

  image("exploration_func.svg", width: 100%) + align(center, [The Holder Table function]),
  align(horizon, image("exploration_mean.svg")) + align(center, [Mean distance between particles over iterations]),
  align(horizon, image("exploration_var.svg")) + align(center, [Particle variance over iterations]),
)

#v(1em)

#align(center, text(
  size: 15pt,
  align(
    left,
    [*Figure 1.* Visualization of the repartition of particles in the search space for the CBO, SMD-CBO and GCN-CBO algorithms on the Holder Table function. The first row shows the repartition of particles at the last iteration (over $1000$ iterations) for each algorithm. The second row shows the evolution of the minimum value of the function over iterations for each algorithm. The third row shows the Holder Table function and the evolution of the mean distance between particles and the particle variance over iterations for each algorithm.],
  ),
))
