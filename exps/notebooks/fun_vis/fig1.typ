#set page(width: auto, height: auto)

#set text(font: "New Computer Modern", size: 12pt)

#grid(
  columns: 3,
  image("Ackley.svg") + align(center, [Ackley]),
  image("Deb.svg") + align(center, [Deb N.1]),
  image("Griewank.svg") + align(center, [Griewank]),

  image("Levy.svg") + align(center, [Levy]),
  image("Rastrigin.svg") + align(center, [Rastrigin]),
  image("Schwefel.svg") + align(center, [Schwefel]),

  [], image("Styblinskitang.svg") + align(center, [Styblinski-Tang]), [],
)

#v(1em)

#align(center, text(
  size: 15pt,
  [*Figure.* Visualization of the 2D landscapes of the multimodal functions used in our experiments.],
))
