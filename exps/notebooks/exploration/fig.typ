#set page(width: auto, height: auto)

#set text(font: "New Computer Modern", size: 12pt)

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
