
import matplotlib.pyplot as plt
import networkx as nx



def visualize_timetable(
    graph, coloring, capacity, course_names=None
):
    course_names = course_names or {}

    if coloring is None:

        print("No timetable available to visualize.")
        return

    # Use the same color for a course and its assigned slot.
    slot_colors = {}
    palette = plt.get_cmap("tab10")

    for slot in sorted(set(coloring.values())):
        slot_colors[slot] = palette((slot - 1) % 10)

    node_colors = [
        slot_colors[coloring[course]]
        for course in graph
    ]

    # Create a graph from the conflict adjacency list.
    G = nx.Graph()
    G.add_nodes_from(graph.keys())

    for course, neighbors in graph.items():
        for neighbor in neighbors:
            if course < neighbor:
                G.add_edge(course, neighbor)

    positions = nx.spring_layout(G, seed=42)

    fig, (ax_graph, ax_table) = plt.subplots(
        1, 2, figsize=(15, 7),
        gridspec_kw={"width_ratios": [1.2, 1]}
    )

    # Draw conflict graph.
    nx.draw_networkx(
        G,
        pos=positions,
        ax=ax_graph,
        node_color=node_colors,
        node_size=850,
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        width=1.5,
        labels={
            node: course_names.get(node, f"Course {node}")
            for node in G.nodes()
        },
    )

    ax_graph.set_title("Conflict Graph (color = exam slot)")
    ax_graph.axis("off")

    # Draw timetable grid.
    slots = sorted(set(coloring.values()))
    max_exams = max(
        (sum(1 for s in coloring.values() if s == slot)
         for slot in slots),
        default=0,
    )

    columns = max(1, min(capacity, max_exams))
    rows = max(1, len(slots))

    ax_table.set_xlim(0, columns)
    ax_table.set_ylim(0, rows)
    ax_table.set_xticks(
        [i + 0.5 for i in range(columns)],
        [f"Hall {i + 1}" for i in range(columns)],
    )
    ax_table.set_yticks(
        [i + 0.5 for i in range(rows)],
        [f"Slot {slot}" for slot in slots],
    )
    ax_table.tick_params(length=0)
    ax_table.set_title("Exam Timetable")
    ax_table.set_aspect("auto")

    for row_index, slot in enumerate(slots):
        courses = sorted(
            course for course, assigned in coloring.items()
            if assigned == slot
        )

        for col_index in range(columns):
            if col_index < len(courses):
                course = courses[col_index]
                face_color = slot_colors[slot]
                label = course_names.get(
                    course, f"Course {course}"
                )
            else:
                face_color = "white"
                label = ""

            cell = plt.Rectangle(
                (col_index, row_index),
                1, 1,
                facecolor=face_color,
                edgecolor="black",
                linewidth=1,
            )
            ax_table.add_patch(cell)
            ax_table.text(
                col_index + 0.5,
                row_index + 0.5,
                label,
                ha="center",
                va="center",
                fontsize=9,
            )

    ax_table.invert_yaxis()
    plt.tight_layout()
    plt.show()
