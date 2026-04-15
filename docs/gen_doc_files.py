import sys

sys.path.append("../")
import inspect
import globe.optimizers as go
import globe.metrics as gm
import globe.benchmarks as gb
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


matplotlib.rcParams.update({"font.size": 9})


# ============================================================================
# File I/O
# ============================================================================


def create_dir(path: Path) -> None:
    """Create directory and all parent directories if they don't exist."""
    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)


def create_file(path: Path, content: str) -> None:
    """Write content to file."""
    with open(path, "w") as f:
        f.write(content)


# ============================================================================
# RST Generation
# ============================================================================


def create_rst_header(title: str) -> str:
    """Generate RST header with title and underline."""
    underline = "=" * len(title)
    return f"{title}\n{underline}"


def create_rst_toctree(files: list[str], maxdepth: int = 1) -> str:
    """Generate RST toctree directive."""
    files_str = "\n   ".join(files)
    return ".. toctree::\n" f"   :maxdepth: {maxdepth}\n\n" f"   {files_str}"


def create_rst_automodule(module_path: str) -> str:
    """Generate RST automodule directive."""
    return (
        f".. automodule:: {module_path}\n"
        "   :members:\n"
        "   :show-inheritance:\n"
        "   :undoc-members:\n"
    )


def create_index_file(path: Path, title: str, files: list[str]) -> None:
    """Create an index.rst file with toctree."""
    content = f"{create_rst_header(title)}\n\n" f"{create_rst_toctree(files)}"
    create_file(path / "index.rst", content)


# ============================================================================
# Module Organization
# ============================================================================


def get_first_submodule(source_path: Path, package_name: str) -> str | None:
    """Extract the first-level submodule from a source file path.

    Args:
        source_path: Path to the source file
        package_name: Package name (e.g., 'optimizers', 'benchmarks')

    Returns:
        First-level submodule name or None if not found
    """
    parts = source_path.parts
    try:
        idx = parts.index(package_name)
        if idx + 1 < len(parts):
            return parts[idx + 1]
    except ValueError:
        pass
    return None


def get_full_module_path(source_path: Path, package_name: str) -> str:
    """Get the full module path excluding the filename.

    Args:
        source_path: Path to the source file
        package_name: Package name (e.g., 'optimizers', 'benchmarks')

    Returns:
        Module path as dot-separated string (e.g., 'decision.subdir')
    """
    parts = source_path.parts
    try:
        idx = parts.index(package_name)
        subpackages = list(parts[idx + 1 : -1])  # Exclude filename
        return ".".join(subpackages)
    except ValueError:
        return ""


def organize_by_submodule(items: list[tuple], package_name: str) -> dict:
    """Organize items by their first-level submodule.

    Args:
        items: List of (name, class) tuples
        package_name: Package name (e.g., 'optimizers', 'benchmarks')

    Returns:
        Dictionary mapping submodule names to lists of (name, class) tuples
    """
    result = {}
    for name, cls in items:
        source_path = Path(inspect.getsourcefile(cls))
        submodule = get_first_submodule(source_path, package_name)

        if submodule:
            if submodule not in result:
                result[submodule] = []
            result[submodule].append((name, cls))

    return result


# ============================================================================
# Benchmark-specific Functions
# ============================================================================


def generate_benchmark_graph(
    benchmark_instance, output_dir: Path, name: str, is_pygkls: bool = False
) -> None:
    """Generate and save a 3D surface plot of the benchmark function.

    Args:
        benchmark_instance: Instantiated benchmark
        output_dir: Directory to save the graph
        name: Benchmark name (used for filename)
        is_pygkls: Whether this is a PyGKLS benchmark
    """
    create_dir(output_dir)

    if is_pygkls:
        x = np.linspace(-10, 10, 500)
        y = np.linspace(-10, 10, 500)
    else:
        bounds = benchmark_instance.visual_bounds
        x = np.linspace(bounds[0][0], bounds[0][1], 500)
        y = np.linspace(bounds[1][0], bounds[1][1], 500)

    X, Y = np.meshgrid(x, y)
    Z = np.array(
        [
            benchmark_instance(np.array([xi, yi]))
            for xi, yi in zip(np.ravel(X), np.ravel(Y))
        ]
    ).reshape(X.shape)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z, linewidth=0.2, edgecolors="white", cmap="coolwarm")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_box_aspect(None, zoom=0.8)

    # Hide every other tick label for clarity
    xticks = ax.xaxis.get_major_ticks()
    yticks = ax.yaxis.get_major_ticks()
    for i in range(0, len(xticks), 2):
        xticks[i].label1.set_visible(False)
    for i in range(0, len(yticks), 2):
        yticks[i].label1.set_visible(False)

    plt.savefig(
        output_dir / f"{name}.png",
        dpi=400,
        bbox_inches="tight",
        transparent=True,
    )
    plt.close()


def create_benchmark_rst(
    benchmark_instance,
    title: str,
    module_path: str,
    graph_path: str | None = None,
    is_pygkls: bool = False,
) -> str:
    """Generate RST content for a benchmark.

    Args:
        benchmark_instance: Instantiated benchmark
        title: Benchmark title
        module_path: Full module path
        graph_path: Relative path to graph file (if any)
        is_pygkls: Whether this is a PyGKLS benchmark

    Returns:
        RST content as string
    """
    content = f"{create_rst_header(title)}\n\n"

    if graph_path:
        content += (
            f".. image:: {graph_path}\n"
            "   :width: 550px\n"
            "   :height: 550px\n"
            "   :align: center\n\n"
        )

    if is_pygkls:
        content += (
            "Uses the `pyGKLS <https://pypi.org/project/gkls/>`_ package to generate "
            "random test functions, with control over their geometry.\n\n"
        )

    content += create_rst_automodule(f"globe.benchmarks.{module_path}")

    return content


# ============================================================================
# Documentation Generation
# ============================================================================


def generate_optimizers_documentation(output_dir: Path) -> None:
    """Generate documentation for optimizers."""
    create_dir(output_dir / "optimizers")
    optimizers = inspect.getmembers(go, inspect.isclass)
    optimizers_by_submodule = organize_by_submodule(optimizers, "optimizers")

    submodule_indices = []
    for submodule in sorted(optimizers_by_submodule.keys()):
        submodule_dir = output_dir / "optimizers" / submodule
        create_dir(submodule_dir)
        files_list = []

        for name, opt_class in optimizers_by_submodule[submodule]:
            source_path = Path(inspect.getsourcefile(opt_class))
            module_path = get_full_module_path(source_path, "optimizers")
            opt_instance = opt_class([])

            content = (
                f"{create_rst_header(str(opt_instance))}\n\n"
                f"{create_rst_automodule(f'globe.optimizers.{module_path}.{name}')}"
            )

            file_path = submodule_dir / f"globe.{name}.rst"
            create_file(file_path, content)
            files_list.append(file_path.stem)

        create_index_file(submodule_dir, submodule.capitalize(), files_list)
        submodule_indices.append(f"{submodule}/index")

    create_index_file(
        output_dir / "optimizers",
        "Optimizers",
        submodule_indices,
    )


def generate_metrics_documentation(output_dir: Path) -> None:
    """Generate documentation for metrics."""
    create_dir(output_dir / "metrics")
    metrics = inspect.getmembers(gm, inspect.isclass)
    files_list = []

    for name, metric_class in metrics:
        metric_instance = metric_class(None, None)

        content = (
            f"{create_rst_header(str(metric_instance))}\n\n"
            f"{create_rst_automodule(f'globe.metrics.{name.lower()}')}"
        )

        file_path = output_dir / "metrics" / f"globe.{name}.rst"
        create_file(file_path, content)
        files_list.append(file_path.stem)

    create_index_file(output_dir / "metrics", "Metrics", files_list)


def generate_benchmarks_documentation(output_dir: Path) -> None:
    """Generate documentation for benchmarks."""
    create_dir(output_dir / "benchmarks")
    benchmarks = inspect.getmembers(gb, inspect.isclass)
    benchmarks_by_submodule = organize_by_submodule(benchmarks, "benchmarks")

    submodule_indices = []
    for submodule in sorted(benchmarks_by_submodule.keys()):
        submodule_dir = output_dir / "benchmarks" / submodule
        create_dir(submodule_dir)
        files_list = []

        for name, benchmark_class in benchmarks_by_submodule[submodule]:
            source_path = Path(inspect.getsourcefile(benchmark_class))
            module_path = get_full_module_path(source_path, "benchmarks")

            # Instantiate benchmark
            if name == "PyGKLS":
                benchmark_instance = benchmark_class(2, 30, [-10, 10], -10, gen=125794)
                is_pygkls = True
            else:
                benchmark_instance = benchmark_class()
                is_pygkls = False

            # Generate graph
            graphs_dir = submodule_dir / "graphs"
            generate_benchmark_graph(
                benchmark_instance, graphs_dir, name, is_pygkls=is_pygkls
            )

            # Generate RST file
            content = create_benchmark_rst(
                benchmark_instance,
                str(benchmark_instance),
                f"{submodule.lower()}.{name.lower()}",
                graph_path=f"graphs/{name}.png",
                is_pygkls=is_pygkls,
            )

            file_path = submodule_dir / f"globe.{name}.rst"
            create_file(file_path, content)
            files_list.append(file_path.stem)

        create_index_file(submodule_dir, submodule.capitalize(), files_list)
        submodule_indices.append(f"{submodule}/index")

    create_index_file(
        output_dir / "benchmarks",
        "Benchmarks",
        submodule_indices,
    )


# ============================================================================
# Main
# ============================================================================


if __name__ == "__main__":
    output_dir = Path("./source")

    generate_optimizers_documentation(output_dir)
    generate_metrics_documentation(output_dir)
    generate_benchmarks_documentation(output_dir)
