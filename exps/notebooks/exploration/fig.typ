#set page(width: 40cm, height: 50cm)

#set par(justify: true)

#set text(font: "New Computer Modern", size: 12pt)

#let opt = [Langevin]
#let smd_opt = [SMD-#opt]
#let gcn_opt = [GCN-#opt]

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

#legend([Cumulative search space coverage (\%)])
#image("exploration_coverage.svg")

#v(1em)

#align(center, text(
  size: 15pt,
  align(
    left,
    [*Figure.* Visualization of the coverage of the search space for the #opt, #smd_opt and #gcn_opt algorithms on the Ackley function using $15$ particles and $1000$ iterations. The first row shows the estimated density (using Gaussian kernels) of particles at the last iteration for each algorithm. The second row shows the evolution of the minimum value of the function over iterations for each algorithm. The third row shows the space that has been visited by each algorithm after $1000$ iterations. The last row shows the percentage of the search space that has been visited by the particles over iterations for each algorithm. For the two last rows, the coverage of the search space is computed by discretizing the latter into a $epsilon$-cover. We then count the number of balls of radius $epsilon$ that have been visited by at least one particle during the optimization process. We set $epsilon = 0.1$ in our experiments.

      One can see that, not only the SMD and GCN variants of #opt end up with a better concentration of particles around the global minimum, but they also explore more of the search space, as shown by the last row. This suggests that the SMD and GCN variants are able to escape local minima and explore more effectively the search space, leading to better optimization performance.],
  ),
))
