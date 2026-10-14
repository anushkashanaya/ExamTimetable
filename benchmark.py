
import time
import matplotlib.pyplot as plt

from graph_coloring import (
    generate_graph,
    dsatur,
    exact_solve,
    valid_assignment,
)


def benchmark():
    # Keep exact search sizes small initially.
    sizes = [5, 8, 10, 12, 15]
    density = 0.25
    capacity = 4

    greedy_times = []
    exact_times = []
    greedy_slots = []
    exact_slots = []
    exact_proven = []

    for n in sizes:
        graph = generate_graph(n, density, seed=42 + n)

        start = time.perf_counter()
        greedy = dsatur(graph, capacity)
        greedy_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        exact, proven = exact_solve(
            graph, capacity, time_limit=3
        )
        exact_times.append(time.perf_counter() - start)

        greedy_valid = (
            greedy is not None
            and valid_assignment(graph, greedy, capacity)
        )
        exact_valid = (
            exact is not None
            and valid_assignment(graph, exact, capacity)
        )

        greedy_slots.append(
            max(greedy.values()) if greedy_valid else None
        )
        exact_slots.append(
            max(exact.values()) if exact_valid else None
        )
        exact_proven.append(proven and exact_valid)

        print(
            f"N={n}: "
            f"Greedy slots={greedy_slots[-1]}, "
            f"Exact slots={exact_slots[-1]}, "
            f"Optimality proven={exact_proven[-1]}"
        )

    # Plot slot counts.
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, greedy_slots, marker="o", label="Greedy DSatur")
    plt.plot(sizes, exact_slots, marker="s", label="Exact Backtracking")
    plt.xlabel("Number of courses (N)")
    plt.ylabel("Time slots used")
    plt.title(f"Slot Count Comparison (density={density})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("slot_comparison.png", dpi=300)

    # Plot runtime.
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, greedy_times, marker="o", label="Greedy DSatur")
    plt.plot(sizes, exact_times, marker="s", label="Exact Backtracking")
    plt.xlabel("Number of courses (N)")
    plt.ylabel("Running time (seconds)")
    plt.title(f"Runtime Comparison (density={density})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("runtime_comparison.png", dpi=300)

    plt.show()


if __name__ == "__main__":
    benchmark()
