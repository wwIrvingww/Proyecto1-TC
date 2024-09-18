import networkx as nx
import matplotlib.pyplot as plt
import copy
from collections import defaultdict

def graph_main(afd):
    transitions = copy.deepcopy(afd['δ'])
    final_states = set(afd['F'])  # Convert the final states array to a set for faster lookup
    initial_state = copy.deepcopy(afd['q0'])

    # Create a directed graph (only one edge between nodes)
    G = nx.DiGraph()

    # Store multiple transitions between the same nodes
    edge_labels = defaultdict(list)

    # Add edges to the graph and accumulate transition labels
    for key, dest_state in transitions.items():
        # Extract the start state and symbol from the key
        start_state, symbol = key.strip("()").split(",")
        start_state = start_state.strip()
        symbol = symbol.strip()

        # Add the transition label to the list of edge labels
        edge_labels[(start_state, dest_state)].append(symbol)

        # Add the edge to the graph
        G.add_edge(start_state, dest_state)

    # Draw the graph
    pos = nx.spring_layout(G)  # Layout for visualization

    # Combine multiple transitions into one label (comma-separated)
    combined_edge_labels = {key: "|".join(labels) for key, labels in edge_labels.items()}

    # Assign colors based on initial state and final states
    node_colors = ["#478dbf" if node == initial_state 
                   else "#65bf9a" if node in final_states 
                   else "#94dfe0" for node in G.nodes()]

    # Draw nodes
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors,
            font_size=10, font_weight='bold', arrowsize=20)

    # Draw edges
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', min_source_margin=15, min_target_margin=15)

    # Draw edge labels (combined transitions)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=combined_edge_labels, font_color='red')

    plt.title("Finite Automaton Graph with Combined Transition Labels")
    plt.show()
