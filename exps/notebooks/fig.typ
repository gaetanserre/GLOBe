#set page(width: auto, height: auto)

#set text(font: "New Computer Modern")

#grid(
  columns: 3,
  image("exploration_cbo.svg"), image("exploration_smd_cbo.svg"), image("exploration_gcn_cbo.svg"),
  image("exploration_func.svg", width: 100%),
  align(horizon, image("exploration_mean.svg")) + align(center, [Mean distance between particles]),
  align(horizon, image("exploration_var.svg")) + align(center, [Particle variance]),
)
