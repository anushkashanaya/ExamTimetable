
import random
import time
import csv


def build_graph(n, edges):
    graph = {i: set() for i in range(1, n + 1)}

    for u, v in edges:
        if u < 1 or u > n or v < 1 or v > n:
            raise ValueError("Invalid course number.")
        if u == v:
            raise ValueError("A course cannot conflict with itself.")

        graph[u].add(v)
        graph[v].add(u)

    return graph


def generate_graph(n, density, seed=None):
    if not 0 <= density <= 1:
        raise ValueError("Density must be between 0 and 1.")

    rng = random.Random(seed)
    edges = []

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if rng.random() < density:
                edges.append((u, v))

    return build_graph(n, edges)


def valid_assignment(graph, coloring, capacity):
    if set(coloring) != set(graph):
        return False

    counts = {}

    for course, slot in coloring.items():
        if not isinstance(slot, int) or slot < 1:
            return False

        counts[slot] = counts.get(slot, 0) + 1

        if counts[slot] > capacity:
            return False

        for neighbor in graph[course]:
            if coloring.get(neighbor) == slot:
                return False

    return True


def dsatur(graph, capacity):
    """Greedy DSatur with a maximum number of courses per slot."""
    coloring = {}
    counts = {}

    while len(coloring) < len(graph):
        uncolored = [v for v in graph if v not in coloring]

        def priority(v):
            saturation = len({
                coloring[u] for u in graph[v] if u in coloring
            })
            return saturation, len(graph[v]), -v

        course = max(uncolored, key=priority)
        forbidden = {
            coloring[u] for u in graph[course] if u in coloring
        }

        slot = next(
            (
                s for s in range(1, len(graph) + 1)
                if s not in forbidden and counts.get(s, 0) < capacity
            ),
            None,
        )

        if slot is None:
            return None

        coloring[course] = slot
        counts[slot] = counts.get(slot, 0) + 1

    return coloring


def exact_solve(graph, capacity, time_limit=10):
    """
    Find a minimum-slot timetable using exact backtracking.
    If the time limit expires, return the best known result
    without claiming optimality.
    """
    n = len(graph)

    if n == 0:
        return {}, True

    if capacity < 1:
        raise ValueError("R must be at least 1.")

    if n > 0 and capacity * n < n:
        return None, True

    greedy = dsatur(graph, capacity)
    if greedy is None:
        upper = n
    else:
        upper = max(greedy.values())

    lower = max(1, (n + capacity - 1) // capacity)
    deadline = time.perf_counter() + time_limit

    def search(limit):
        colors = {}
        counts = [0] * (limit + 1)

        def visit():
            if time.perf_counter() > deadline:
                raise TimeoutError

            if len(colors) == n:
                return True

            uncolored = [v for v in graph if v not in colors]

            def priority(v):
                saturation = len({
                    colors[u] for u in graph[v] if u in colors
                })
                return saturation, len(graph[v]), -v

            v = max(uncolored, key=priority)
            forbidden = {
                colors[u] for u in graph[v] if u in colors
            }

            max_color = min(limit, max(colors.values(), default=0) + 1)

            for color in range(1, max_color + 1):
                if color in forbidden or counts[color] >= capacity:
                    continue

                colors[v] = color
                counts[color] += 1

                if visit():
                    return True

                counts[color] -= 1
                del colors[v]

            return False

        return dict(colors) if visit() else None

    for limit in range(lower, upper + 1):
        try:
            result = search(limit)
        except TimeoutError:
            return greedy, False

        if result is not None:
            return result, True

    return greedy, False


def save_csv(
    coloring,
    filename="timetable.csv",
    capacity=None,
    course_names=None,
):
    import csv

    course_names = course_names or {}

    if not coloring:
        raise ValueError("No valid timetable to save.")

    slots = {}

    for course, slot in coloring.items():
        slots.setdefault(slot, []).append(
            course_names.get(course, f"Course {course}")
        )

    max_courses = max(len(courses) for courses in slots.values())

    if capacity is not None:
        max_courses = capacity

    headers = ["Time Slot"] + [
        f"Hall {i}" for i in range(1, max_courses + 1)
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for slot in sorted(slots):
            courses = sorted(slots[slot])
            row = [f"Slot {slot}"] + courses
            row += [""] * (max_courses - len(courses))
            writer.writerow(row)

    print(f"Named timetable saved to {filename}")



def report(name, coloring, graph, capacity, elapsed, optimal=None):
    print(f"\n--- {name} ---")
    print(f"Running time: {elapsed:.6f} seconds")

    if coloring is None:
        print("No timetable returned.")
        return

    print("Valid:", valid_assignment(graph, coloring, capacity))
    print("Slots used:", max(coloring.values(), default=0))

    if optimal is not None:
        print("Optimality proven:", optimal)

    for slot in sorted(set(coloring.values())):
        courses = sorted(
            course for course, assigned in coloring.items()
            if assigned == slot
        )
        print(f"Slot {slot}: {courses}")
