import networkx as nx
from taska import parseWikiData
from random import sample
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DEGREE_THRESHOLD = 10

colours = ['yellow', '#F4D4D3', '#E9A8A1', '#E9635E', '#CA1414', '#6B0003', 'black']

colours_with_label = {
    colours[0]: "infected",
    colours[1]: "[0, 0.1)",
    colours[2]: "[0.1, 0.2)",
    colours[3]: "[0.3, 0.4)",
    colours[4]: "[0.4, 0.5)",
    colours[5]: "[0.5, 1]",
    colours[6]: "not infected",
}

def get_2_semi_random_nodes(graph: nx.graph, threshold: int) -> list:
    degrees = list(nx.degree(graph))
    valid_nodes = []
    for x in degrees:
        if x[1] > threshold:
            valid_nodes.append(x[0])
    random_nodes = sample(valid_nodes, 2)
    return random_nodes


def calculate_jaccard_similarity(node1_neighbours, node2_neighbours) -> float:
    neighbors_node1 = set(node1_neighbours)
    neighbors_node2 = set(node2_neighbours)
    intersection = neighbors_node1 & neighbors_node2
    union = neighbors_node1 | neighbors_node2
    return len(intersection) / len(union)


def calculate_transmission_risk(graph: nx.graph,
                                infected_node: str,
                                susceptible_node: str,
                                degree_threshold: int) -> float:
    if nx.has_path(graph, infected_node, susceptible_node):
        susceptible_node_neighbours = list(graph.neighbors(susceptible_node))
        # if the degree is lower than a threshold the node isn't susceptible
        if len(susceptible_node_neighbours) < degree_threshold:
            return 0.0
        infected_node_neighbours = list(graph.neighbors(infected_node))
        path_length = nx.shortest_path_length(graph, infected_node, susceptible_node)
        similarity = calculate_jaccard_similarity(infected_node_neighbours,
                                                  susceptible_node_neighbours)
        risk = similarity / path_length   # division by zero
        return risk
    else:
        return 0.0  # No path, no risk


def get_risk_scores_of_valid_nodes(graph: nx.graph,
                                   initially_infected: list[str],
                                   susceptible_editors: list[str]) -> dict:
    risk_scores = {}
    for infected in initially_infected:
        for susceptible in susceptible_editors:
            risk = calculate_transmission_risk(graph, infected, susceptible, DEGREE_THRESHOLD)
            if risk == 0:
                pass
            elif risk not in risk_scores:
                risk_scores[susceptible] = risk
            else:
                current_risk = risk_scores[susceptible]
                risk_scores[susceptible] = max(current_risk, risk)
    return risk_scores


def get_colour(similarity: float) -> str:
    if 0 <= similarity < 0.1:
        return colours[1]
    elif 0.1 <= similarity < 0.2:
        return colours[2]
    elif 0.2 <= similarity < 0.3:
        return colours[3]
    elif 0.3 <= similarity < 0.4:
        return colours[4]
    elif 0.4 <= similarity <= 1:
        return colours[5]


def generate_risk_graph(old_graph: nx.graph, nodes: dict, infected_nodes: list) -> nx.graph:
    graph = nx.Graph()
    graph.add_nodes_from(infected_nodes, color=colours[0])
    node_keys = set(nodes.keys())
    appended_nodes = set()
    for node in nodes:
        graph.add_node(node, color=get_colour(nodes[node]))
    for node in node_keys:
        for infected in infected_nodes:
            shortest_path = nx.shortest_path(old_graph, source=infected, target=node)
            if len(shortest_path) == 2:
                graph.add_edge(shortest_path[0], shortest_path[1])
            else:
                for i in range(len(shortest_path) - 1):
                    next_elem = shortest_path[i + 1]
                    if (next_elem not in node_keys
                            and next_elem not in infected_nodes
                            and next_elem not in appended_nodes):
                        appended_nodes.add(next_elem)
                        graph.add_node(shortest_path[i + 1], color=colours[6])
                    graph.add_edge(shortest_path[i], shortest_path[i + 1])
    return graph


def display_graph(graph: nx.Graph) -> None:
    plt.figure(figsize=(10, 10))
    layout = nx.random_layout(graph)

    colors = [graph.nodes[node]['color'] for node in graph.nodes]
    sizes = [500 if graph.nodes[node]['color'] == 0 else 300 for node in graph.nodes]
    nx.draw(graph, layout, node_color=colors, node_size=sizes, with_labels=False)
    patches = [plt.plot([],[], marker="o", ms=10, ls="", mec=None, color=colour,
                label="{:s}".format(label))[0]  for colour, label in colours_with_label.items()]
    plt.legend(handles=patches, loc='upper right')
    plt.show()


def display_histogram(graph: nx.Graph) -> None:
    colors = [graph.nodes[node]['color'] for node in graph.nodes]
    color_counts = {color: colors.count(color) for color in set(colors)}
    color_labels = [colours_with_label[color] for color in color_counts.keys()]
    frequencies = list(color_counts.values())
    plt.figure(figsize=(10, 6))
    plt.xlabel("similarity range", fontsize=12, fontweight='bold')
    plt.ylabel("similar range occurrences", fontsize=12, fontweight='bold')
    bars = plt.bar(color_labels, frequencies, color=list(color_counts.keys()))
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom')
    plt.show()


if __name__ == "__main__":
    datasets = ['INTERWIKI_CONFLICT.csv', 'REQUEST_FOR_DELETION.csv', 'WIKIPROJECTS.csv']
    path = 'datasets/'
    networks = [parseWikiData(path + datasets[2])]
    G = networks[0]

    random_nodes = get_2_semi_random_nodes(G, 100)

    all_nodes = [node for node in G.nodes() if node not in random_nodes]

    risky_nodes = get_risk_scores_of_valid_nodes(G, random_nodes, all_nodes)

    new_graph = generate_risk_graph(G, risky_nodes, random_nodes)
    display_graph(new_graph)
    display_histogram(new_graph)
