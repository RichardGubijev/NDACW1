import networkx as nx
from random import sample
import statistics


def calculate_stats(G: nx.graph) -> dict:
    degrees = nx.degree(G)
    degree_values = [deg[1] for deg in degrees]
    return {
        "degrees": degrees,
        "mean_degree": statistics.mean(degree_values),
        "median_degree": statistics.median(degree_values),
        "max_degree": max(degree_values),
    }


def get_neighbors(G: nx.graph, node):
    return list(G.neighbors(node))


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
