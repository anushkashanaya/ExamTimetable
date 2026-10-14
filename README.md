# Exam Timetable Scheduler Using Graph Coloring

A Python-based examination scheduling system that uses graph coloring algorithms to generate conflict-free timetables while considering limited examination hall capacity.

## Problem Statement

A university has *N* courses, where two courses conflict if at least one student is enrolled in both. Conflicting courses cannot be scheduled in the same time slot. Additionally, each time slot can accommodate at most *R* examinations due to limited hall availability.

The objective is to generate a valid timetable that minimizes the total number of time slots required.

## Objectives

- Generate conflict-free examination schedules.
- Enforce the maximum number of examinations permitted per time slot.
- Implement and compare greedy and exact graph coloring algorithms.
- Minimize the number of time slots required.
- Visualize the conflict graph and generated timetable.
- Export the timetable as a CSV file.
- Compare algorithm performance across different graph sizes.

## Technologies Used

- **Programming Language:** Python
- **Libraries:** NetworkX, Matplotlib
- **Concepts:** Graph Theory, Graph Coloring, Greedy Algorithms, Backtracking, Algorithm Analysis, File Handling

## Algorithms Implemented

### 1. DSatur Greedy Algorithm

The DSatur algorithm selects courses based on their saturation degree and assigns each course to an available time slot while respecting conflicts and hall capacity. It provides a fast scheduling solution but does not guarantee the minimum number of time slots.

### 2. Exact Backtracking Algorithm

The exact backtracking algorithm explores possible course assignments to find a valid schedule using the minimum number of time slots. The implementation uses a time limit and reports whether optimality has been proven.

## Features

- Manual conflict graph input.
- Random conflict graph generation with configurable edge density.
- File-based conflict graph input.
- Course-name input for readable timetables.
- Conflict and hall-capacity validation.
- Comparison of greedy and exact scheduling results.
- CSV timetable export.
- Conflict graph visualization with nodes colored according to assigned time slots.
- Timetable grid visualization using the same color scheme.
- Benchmark charts comparing the number of time slots and execution time.

## Project Structure

```text
ExamTimetable/
├── main.py
├── graph_coloring.py
├── visualization.py
├── benchmark.py
├── conflicts.txt
├── requirements.txt
├── .gitignore
├── timetable.csv
├── slot_comparison.png
└── runtime_comparison.png
```

The CSV and PNG files are generated outputs. Include them only if they exist in your repository.

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ExamTimetable.git
cd ExamTimetable
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The project requires the following libraries:

```text
matplotlib
networkx
```

### 3. Run the Scheduler

```bash
python3 main.py
```

Choose one of the available options:

1. Enter a conflict graph manually.
2. Generate a random conflict graph.
3. Load conflict information from `conflicts.txt`.

Follow the terminal prompts to enter course information and generate the timetable.

### 4. Run the Benchmark

```bash
python3 benchmark.py
```

The benchmark compares both algorithms across increasing graph sizes and displays charts for slot counts and execution times. If chart saving is enabled, the results are also saved as PNG files.

## Input Format

### Option 1: Manual Graph Input

Enter the number of courses (*N*), conflict edges (*M*), and maximum examinations per time slot (*R*).

Example:

```text
5 5 2
1 2
1 3
2 3
3 4
4 5
```

Each subsequent line represents a conflict between two courses.

### Option 2: Random Graph Generation

Enter the number of courses, hall capacity, and edge density between 0 and 1. A higher edge density generally produces more conflicts.

### Option 3: File-Based Input

The `conflicts.txt` file follows the same format as manual input. The first line contains `N M R`, followed by the conflict edges.

## Output

The scheduler reports the results of both algorithms, including the number of time slots used and whether optimality was proven.

The program produces:

- A slot-wise examination timetable.
- A CSV file named `timetable.csv`, with time slots as rows and halls as columns.
- A conflict graph colored according to assigned time slots.
- A visual timetable grid.
- Benchmark charts comparing slot counts and execution times.

## Algorithm Comparison

The benchmark evaluates the algorithms using different graph sizes and compares:

- Number of time slots used.
- Execution time.
- Whether the exact algorithm proved its solution optimal.

The exact algorithm has a time limit, so optimality may remain unproven for larger or more difficult graphs.

## Future Improvements

- Automatically construct conflict graphs from student course registrations.
- Consider exam durations, room sizes, faculty availability, and holidays.
- Develop a graphical user interface.
- Add animated visualization of course assignments.
- Support exporting timetables to PDF.
- Improve performance for larger graphs.

## Learning Outcomes

This project demonstrates the application of graph coloring to a practical scheduling problem. It provides experience with greedy heuristics, exact search, constraint validation, visualization, file handling, and empirical algorithm comparison.
