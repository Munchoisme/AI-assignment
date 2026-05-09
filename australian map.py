#A simple backtracking solver for the map coloring problem, with visualization using NetworkX and Matplotlib.
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#Checks that the provided graph is valid,ensuring that no node is adjacent to itself,all neighbors are known nodes in the graph,and that adjacency is symmetric.
def check_valid(graph):
    for n, nexts in graph.items():
        assert n not in nexts, f"Node {n} cannot be adjacent to itself"
        for nxt in nexts:
            assert nxt in graph, f"Node {n} has unknown neighbor {nxt}"
            assert n in graph[nxt], f"Adjacency must be symmetric: {n} is neighbor of {nxt} but not vice versa"

# Checks that the provided solution is valid for the given graph, ensuring that no adjacent nodes share the same color.
def check_solution(graph, solution):
    if solution is not None:
        for node, nexts in graph.items():
            assert node in solution
            color = solution[node]
            for nxt in nexts:
                assert nxt in solution and solution[nxt] != color

#Backtracking solver
def find_best_candidate(graph, guesses):
    candidates_with_add_info = [
        (
            -len({guesses[neigh] for neigh in graph[n] if neigh in guesses}),#Number of already used colors among neighbors; negative for sorting in descending order
            -len({neigh for neigh in graph[n] if neigh not in guesses}),#Number of uncolored neighbors; negative for sorting in descending order
            n
        ) for n in graph if n not in guesses
    ]
    candidates_with_add_info.sort()
    candidates = [n for _, _, n in candidates_with_add_info]
    if candidates:
        candidate = candidates[0]
        assert candidate not in guesses
        return candidate
    assert set(graph.keys()) == set(guesses.keys())
    return None

#Global counter to track the number of calls to the solver function to analyze the performance of the backtracking algo.
aus_calls = 0

#The main recursive backtracking function that attempts to assign colors to the nodes of the graph while respecting the constraints of the map coloring problem.It uses the find_best_candidate function to select the next node to color and tries all valid colors for that node,recursively calling itself until a solution is found or all options are exhausted.
def solve(graph, colors, guesses, depth):
    global aus_calls
    aus_calls += 1
    n = find_best_candidate(graph, guesses)
    if n is None:
        return guesses  #Solution found
    for c in colors - {guesses[neigh] for neigh in graph[n] if neigh in guesses}:
        guesses[n] = c
        indent = '  ' * depth
        print(f"{indent}Trying to give color {c} to {n}")
        if solve(graph, colors, guesses, depth + 1):
            print(f"{indent}Gave color {c} to {n}")
            return guesses
        else:
            del guesses[n]
            print(f"{indent}Cannot give color {c} to {n}")
    return None

#The main function that sets up the problem,calls the solver,checks the solution,and visualizes it if found.
def solve_problem(graph, colors):
    check_valid(graph)
    solution = solve(graph, colors, dict(), 0)
    print(solution)
    check_solution(graph, solution)
    return solution

#Visualization function that uses NetworkX to create a graph representation of the map and Matplotlib to visualize it.It colors the nodes according to the solution found by the solver and includes a legend to indicate which color corresponds to which label and saves the visualization as an image file.
def visualize(graph, solution, title="Map Coloring"):
    G = nx.Graph()
    for node, neighbors in graph.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    color_name_map = {
        'Red': '#e74c3c',
        'Green': '#2ecc71',
        'Blue': '#3498db',
        'Yellow': '#f1c40f',
        'Orange': '#e67e22',
        'Purple': '#9b59b6',
    }

    node_colors = [color_name_map.get(solution[n], solution[n]) for n in G.nodes()]

    #Uses a fixed seed for reproducible layout
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 7))
    nx.draw_networkx(
        G, pos,
        node_color=node_colors,
        node_size=2500,
        font_size=8,
        font_weight='bold',
        edge_color='#555555',
        width=2,
        with_labels=True
    )

    #Creates legend based on unique colors used in the solution
    unique_colors = set(solution.values())
    patches = [mpatches.Patch(color=color_name_map.get(c, c), label=c) for c in unique_colors]
    plt.legend(handles=patches, loc='upper left', fontsize=9)

    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/colormap.png', dpi=150)
    plt.show()
    print("Saved to colormap.png")


#Defines the graph for the map coloring problem where each key is a region and its value is a set of neighboring regions.

WA  = 'Western Australia'
NT  = 'Northwest Territories'
SA  = 'Southern Australia'
Q   = 'Queensland'
NSW = 'New South Wales'
V   = 'Victoria'
T   = 'Tasmania'

australia = {
    T:   {V},
    WA:  {NT, SA},
    NT:  {WA, Q, SA},
    SA:  {WA, NT, Q, NSW, V},
    Q:   {NT, SA, NSW},
    NSW: {Q, SA, V},
    V:   {SA, NSW, T}
}

colors = {'Red', 'Green', 'Blue', 'Yellow'}
#Solves the problem and visualizes the solution
solution = solve_problem(australia, colors)
print(f"\nTotal solver calls: {aus_calls}")

if solution:
    visualize(australia, solution, title="Australia Map Coloring")
