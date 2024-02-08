import numpy as np
import networkx as nx
from bokeh.io import output_notebook
from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx
import seaborn as sns

# Note: these methods are largely taken from the lab sessions

#Graph Properties
def print_graph_properties(graph, title):

    print(f'Graph {title} Statistics')
    print_graph_statistics(graph)

    print(f'Graph {title} high level Statistics')
    print_high_level_statistics(graph)


# General statistics
def print_graph_statistics(graph):
    print("Number of nodes: {}\nNumber of edges: {}".format(
        graph.number_of_nodes(), graph.number_of_edges()
    ))
    print("Number of connected components: {}".format(
        nx.algorithms.components.number_connected_components(graph),
    ))
    print("Average degree: {}\nClustering coefficient: {}".format(
        np.mean([deg for _, deg in graph.degree]),
        nx.algorithms.cluster.average_clustering(graph)
    ))

    try:  # attempt to compute the diameter of the graph
        diam = nx.algorithms.approximation.distance_measures.diameter(graph)
        print("Graph diameter: {}".format(diam))
    except:  # an error has  occurred
        print("\nERROR: Could not compute the diameter of the graph.")

# Compare with a random graph to get
        # degree distribution
        # diameter
def print_high_level_statistics(graph):
    largest_component = max(nx.connected_components(graph), key=len)
    graph_largest_components = graph.subgraph(largest_component)
    print_graph_statistics(graph_largest_components)

    equivalent_random = get_equivalent_random_graph(graph)
    print_graph_statistics(equivalent_random)

    

def get_equivalent_random_graph(graph):
    # n : number of nodes
    # p : frequency of edge occurence
        # max edges: n (n - 1) / 2
        # frequency of edge occurence: number of edges / max edges
    n = graph.number_of_nodes()
    number_edges = graph.number_of_edges()
    max_edges = n(n - 1)/2
    p = number_edges/max_edges

    return np.erdos_renyi_graph(n=n, p=p)

# If we want to plot the graph
def bokeh_plot_simple(graph, title, crop_factors = None):
    crop_factors = dict(x_range=(-1.1,1.1), y_range=(-1.1,1.1)) \
        if crop_factors is None else crop_factors

    plot = figure(
        title=title, tools="",
        toolbar_location=None, **crop_factors)

    mapping = dict((n, i) for i, n in enumerate(graph.nodes))
    graph_mapped = nx.relabel_nodes(graph, mapping)

    graph_plot = from_networkx(
        graph_mapped, nx.spring_layout, scale=2, center=(0,0))
    plot.renderers.append(graph_plot)

    #output_file("networkx_graph.html")
    show(plot)

