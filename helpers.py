import networkx as nx
import matplotlib.pyplot as plt
from random import sample
import statistics


def calculate_stats(G: nx.graph):
    degrees = nx.degree(G)
    degree_values = [deg[1] for deg in degrees]
    return int(statistics.mean(degree_values)), statistics.median(degree_values)


def graph_degree_distribution_histogram(degrees):
    degrees_count = {}
    for i in degrees:
        count = i[1]
        if count in degrees_count:
            degrees_count[count] += 1
        else:
            degrees_count[count] = 1
    keys = list(degrees_count.keys())
    values = list(degrees_count.values())
    plt.bar(keys, values)
    plt.xticks(keys)


def sorted_nodes(G: nx.graph):
    degrees = nx.degree(G)
    sorted_degrees = sorted(degrees, key=lambda x: x[1])
    nodes = [node[0] for node in sorted_degrees]
    return nodes


def save_values_to_file(filename, values):
    value_string = ""
    for value in values:
        value_string += f","


def get_2_random_nodes(G: nx.graph):
    degrees: list = list(nx.degree(G))
    random_nodes = sample(degrees, 2)
    return [random_nodes[0][0], random_nodes[1][0]]

# def get_degrees(degree_values, nodes):
#     for x in degree_values:
#         for n in nodes:
#             if n == x[0]:
#                 print(x[1])


def get_node_degree(G: nx.graph, node):
    degrees = nx.degree(G)
    for x in degrees:
        if x[0] == node:
            return x[1]


def cascasde(G: nx.graph, infected_nodes: list, exclusion_theshold: int, degrees):
    for node in infected_nodes:
        for x in get_neighbors(G, node):
            if x in infected_nodes:
                pass
            elif degrees[x] < exclusion_theshold:
                pass
            elif similarity_measure(G.neighbours(node), G.neighbors(x)) >= 0.8:
                infected_nodes.append(x)
    return infected_nodes



def get_neighbors(G: nx.graph, node):
    return list(G.neighbors(node))


def similarity_measure(infected_nodes, node_neghibors):
    infected_nodes = set(infected_nodes)
    node_neghibors = set(node_neghibors)
    return len(infected_nodes & node_neghibors) / len(node_neghibors)




### ----- GRAPHING ----------------


# import networkx as nx
# import matplotlib.pyplot as plt
#
# # Create an empty graph
# G = nx.Graph()
#
# # Add nodes with the attribute 'color'
# G.add_node(1, color=1)
# G.add_node(2, color=0)
# G.add_node(3, color=1)
# G.add_node(4, color=0)
#
# # Add some edges
# G.add_edge(1, 2)
# G.add_edge(2, 3)
# G.add_edge(3, 4)
# G.add_edge(4, 1)
#
# # Define a color map
# color_map = {0: 'green', 1: 'red'}
#
# # Draw the graph
# nx.draw(G, with_labels=True, node_color=[color_map[G.nodes[node]['color']] for node in G.nodes])
# plt.show()
