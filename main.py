
from visualization import visualize_timetable

from graph_coloring import (
    build_graph,
    generate_graph,
    dsatur,
    exact_solve,
    save_csv,
    report,
    valid_assignment,
)
import time

def load_conflicts(filename):
    with open(filename, "r") as file:
        lines = [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]

    if not lines:
        raise ValueError("Input file is empty.")

    n, m, capacity = map(int, lines[0].split())

    if n < 1 or m < 0 or capacity < 1:
        raise ValueError("Invalid N, M, or R.")

    if len(lines) != m + 1:
        raise ValueError(
            f"Expected {m} conflict edges, but found {len(lines) - 1}."
        )

    edges = [
        tuple(map(int, line.split()))
        for line in lines[1:]
    ]

    if any(len(edge) != 2 for edge in edges):
        raise ValueError("Each conflict edge must contain two course numbers.")

    return n, capacity, edges


def main():
    print("=== EXAM TIMETABLE SCHEDULER ===")
    print("1. Enter conflict graph")
    print("2. Generate random conflict graph")
    print("3. Load conflicts from file")

    choice = input("Choose option (1, 2 or 3): ").strip()

    try:
        if choice == "1":
            n, m, capacity = map(
                int, input("Enter N M R: ").split()
            )

            if n < 1 or m < 0 or capacity < 1:
                raise ValueError("N and R must be positive; M cannot be negative.")

            edges = []
            for i in range(m):
                u, v = map(
                    int, input(f"Edge {i + 1} (u v): ").split()
                )
                edges.append((u, v))

            graph = build_graph(n, edges)

        elif choice == "2":
            n, capacity = map(
                int, input("Enter N R: ").split()
            )
            density = float(input("Enter edge density (0 to 1): "))

            if n < 1 or capacity < 1:
                raise ValueError("N and R must be positive.")

            graph = generate_graph(n, density)

            edge_count = sum(map(len, graph.values())) // 2
            print(f"Generated {edge_count} conflict edges.")
        elif choice == "3":
            n, capacity, edges = load_conflicts("conflicts.txt")
            graph = build_graph(n, edges)
            print("Conflict graph loaded successfully.")

        else:
            print("Invalid option.")
            return

        course_names = {}

        print("\n=== ENTER COURSE NAMES ===")
        for course_id in graph:
            name = input(
                f"Enter name for Course {course_id}: "
            ).strip()

            if not name:
                name = f"Course {course_id}"

            course_names[course_id] = name

        start = time.perf_counter()
        greedy = dsatur(graph, capacity)
        greedy_time = time.perf_counter() - start

        report(
            "Greedy DSatur", greedy, graph, capacity, greedy_time
        )

        start = time.perf_counter()
        exact, optimal = exact_solve(graph, capacity, time_limit=10)
        exact_time = time.perf_counter() - start

        report(
            "Exact Backtracking",
            exact,
            graph,
            capacity,
            exact_time,
            optimal,
        )

        if exact is not None and valid_assignment(
            graph, exact, capacity
        ):
            selected = exact
            method = "Exact Backtracking"
        elif greedy is not None and valid_assignment(
            graph, greedy, capacity
        ):
            selected = greedy
            method = "Greedy DSatur"
        else:
            selected = None

        if selected is not None:
            slots_used = len(set(selected.values()))

            print("\n=== TIMETABLE SUMMARY ===")
            print(f"Courses scheduled: {len(selected)}")
            print(f"Time slots required: {slots_used}")
            print(f"Hall capacity per slot: {capacity}")
            print(f"Scheduling method: {method}")
            print(f"Optimality proven: {method == 'Exact Backtracking' and optimal}")
        else:
            print("\nNo valid timetable was found.")


        if exact is not None and valid_assignment(graph, exact, capacity):
            save_csv(exact,capacity=capacity,course_names=course_names,)
            print("\nTimetable saved to timetable.csv")
        
        elif greedy is not None and valid_assignment(graph, greedy, capacity):
            save_csv(
                greedy,
                capacity=capacity,
                course_names=course_names,
            )
            print("\nExact solution unavailable; saved greedy timetable.")

        
        
        if exact is not None and valid_assignment(
            graph, exact, capacity
        ):
            visualize_timetable(
                graph, exact, capacity, course_names
            )
        elif greedy is not None and valid_assignment(
            graph, greedy, capacity
        ):
            visualize_timetable(
                graph, greedy, capacity, course_names
            )



    except ValueError as error:
        print("Invalid input:", error)


if __name__ == "__main__":
    main()
