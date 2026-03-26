#set page(width: 40cm, height: 50cm)

#set par(justify: true)

#set text(font: "New Computer Modern", size: 12pt)

#let opt = [MSGD]
#let smd_opt = [SMD-MSGD]
#let gcn_opt = [GCN-MSGD]

#let legend(it) = align(center, it) + v(-0.5em)

#v(-5em)

#grid(
  columns: 3,
  gutter: 0.5em,

  legend(opt) + image("exploration_opt.svg"),
  legend(smd_opt + [ Mean+Var]) + image("exploration_smd_opt.svg"),
  legend(gcn_opt) + image("exploration_gcn_opt.svg"),

  legend([#opt minimum value over iterations]) + image("exploration_opt_min.svg"),
  legend([#smd_opt minimum value over iterations]) + image("exploration_smd_opt_min.svg"),
  legend([#gcn_opt minimum value over iterations]) + image("exploration_gcn_opt_min.svg"),

  legend([Visited space by #opt]) + image("exploration_visited_opt.svg"),
  legend([Visited space by #smd_opt]) + image("exploration_visited_smd_opt.svg"),
  legend([Visited space by #gcn_opt]) + image("exploration_visited_gcn_opt.svg"),
)

#legend([Coverage of the search space over iterations (in %)])
#image("exploration_coverage.svg")

#v(1em)

#align(center, text(
  size: 15pt,
  align(
    left,
    [*Figure.* Visualization of the coverage of the search space for the #opt, #smd_opt and #gcn_opt algorithms on the Ackley function. The first row shows the repartition of particles at the last iteration (over $1000$ iterations) for each algorithm. The second row shows the evolution of the minimum value of the function over iterations for each algorithm. The last row shows the percentage of the search space that has been visited by the particles over iterations for each algorithm. The coverage is computed by discretizing the search space into a $epsilon$-covering of the space, and counting the number of cells that have been visited by at least one particle at each iteration. We set $epsilon = 0.1$ in our experiments.

      One can see that, not only the SMD and GCN variants of #opt explore more of the search space, but they also end up with a better concentration of particles around the global minimum, which is located at the center of the plots. This suggests that the SMD and GCN variants are able to escape local minima and explore more effectively the search space, leading to better optimization performance.],
  ),
))
