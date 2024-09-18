import networkx as nx
import matplotlib.pyplot as plt
import copy
from collections import defaultdict

def graph_main(afd):
    transitions = copy.deepcopy(afd['δ'])
    final_states = set(afd['F'])  # Convert the final states array to a set for faster lookup
    initial_state = copy.deepcopy(afd['q0'])

    # Create a directed graph
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

    # Draw the graph layout
    pos = nx.spring_layout(G)

    # Combine multiple transitions into one label (comma-separated)
    combined_edge_labels = {key: "|".join(labels) for key, labels in edge_labels.items()}

    # Draw edges with arrows to indicate direction
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=20, min_source_margin=15, min_target_margin=20, connectionstyle="arc3,rad=0.1", edge_color='black')

    # Draw edge labels (combined transitions)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=combined_edge_labels, font_color='red')

    # Custom rendering for the nodes
    ax = plt.gca()

    # Node colors: light green for final states, white for others
    node_colors = ['#90ee90' if node in final_states else '#ffffff' for node in G.nodes]

    # Draw the nodes with custom colors and black outer ring
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes, node_color=node_colors, node_size=2000, edgecolors='black', linewidths=2, ax=ax)

    # Ensure the labels for each node are shown
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Add an arrow pointing towards the initial state
    if initial_state in G.nodes:
        ax.annotate("", xy=(pos[initial_state][0]-0.1,pos[initial_state][1]), xytext=(pos[initial_state][0] - 0.2, pos[initial_state][1]),
                    arrowprops=dict(facecolor='red', shrink=0.1))

    plt.title("AFD REDUCIDO - GRAFO")
    plt.show()
