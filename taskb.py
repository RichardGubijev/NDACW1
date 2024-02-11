import numpy as np
import networkx as nx
from bokeh.io import output_notebook
from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx
import seaborn as sns
import matplotlib.pyplot as plt

# Note: these methods are largely taken from the lab sessions

# i) Characteristics

#Graph Properties
def print_graph_properties(graph:nx.Graph, title:str):

    print(f'Graph {title} Statistics')
    print_graph_statistics(graph)

    print(f'Graph {title} high level Statistics')
    print_statistics_for_largest_component(graph)

    print(f'Graph {title} node level descriptors')
    show_node_level_descriptors(graph)


# i)1) Graph Statistics
def print_graph_statistics(graph:nx.Graph):
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

# i)2) high level statistics
def print_connected_statistics_with_average_shortest_path(component:nx.Graph):
    print("Number of nodes: {}\nNumber of edges: {}".format(
        component.number_of_nodes(), component.number_of_edges()
    ))
    print("Average path length: {}".format(
    nx.average_shortest_path_length(component)
    ))
    print("Number of connected components: {}".format(
        nx.algorithms.components.number_connected_components(component),
    ))
    print("Average degree: {}\nClustering coefficient: {}".format(
        np.mean([deg for _, deg in component.degree]),
        nx.algorithms.cluster.average_clustering(component)
    ))

    try:  # attempt to compute the diameter of the graph
        diam = nx.algorithms.approximation.distance_measures.diameter(component)
        print("Graph diameter: {}".format(diam))
    except:  # an error has  occurred
        print("\nERROR: Could not compute the diameter of the graph.")

def print_statistics_for_largest_component(graph:nx.Graph):
    largest_component = max(nx.connected_components(graph), key=len)
    graph_largest_components = graph.subgraph(largest_component)
    print_connected_statistics_with_average_shortest_path(graph_largest_components)
    #Could do for all components
    # for i, conn_component in enumerate(
    #     nx.connected_components(graph)):
    #     print(f"[Graph component {i}]")
    #     sub_graph = graph.subgraph(conn_component)  # XXX Careful to manupulations!
    #     print_connected_component_statistics(sub_graph)
    #     print("-"*50 + "\n")

# i)3) Node Level statistics
 # *graph and title should be a tuple
def show_node_level_descriptors(*graph_and_title):
    graphs, titles = [ [graph] [title] for graph, title in graph_and_title]
    
    descriptors = [get_node_level_descriptors(graph) for graph in graphs]

    plot_helper_node_level_descriptors(descriptors, titles, 'degrees')
    plot_helper_node_level_descriptors(descriptors, titles, 'degree_centrality')
    plot_helper_node_level_descriptors(descriptors, titles, 'clustering coefficients')
    plot_helper_node_level_descriptors(descriptors, titles, 'closenes centrality')

def get_node_level_descriptors(graph:nx.Graph):
    degrees = [d for _, d in graph.degree()]
    degree_centrality = [d for _, d in nx.degree_centrality(graph).items()]
    ccoeffs = [d for _, d in nx.algorithms.cluster.clustering(graph).items()]
    ccentra = [d for _, d in nx.closeness_centrality(graph).items()]

    return {'degrees': degrees, 'degree_centrality': degree_centrality, 'clustering coefficients': ccoeffs, 'closenes centrality': ccentra}

def plot_helper_node_level_descriptors(descriptors, titles, key):
    data = {titles[i]: descriptors[i][key] for i in range(len(titles))}
    sns.displot(data, height=4, aspect=2, kde=True)


 # If we want to plot the graph = subgraph(largest_component)
def bokeh_plot_simple(graph:nx.Graph, title:str, crop_factors = None):
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


# -----------------------
# ii) shortest paths using Dijkstra and BF
def get_shortest_path_largest_component_Dijkstra(graph:nx.Graph):
    size = len(graph.nodes)
    start_node = graph.nodes[0] # not sure if this will work
    end_node = int(start_node + size/2) % size

    print(f"Start node: {start_node}\nEnd node: {end_node}") 

    spath = nx.algorithms.dijkstra_path(graph, start_node, end_node)
    print("\nShortest path: " + " -> ".join([str(n) for n in spath]))

    print("How long is the path among these farthest nodes? {}".format(
    len(spath) - 1))  # here we do -1 to avoid counting the starting node!
    print(f'Should be the same as the diameter of the graph!!!')


def get_shortest_path_largest_component_BF(graph:nx.Graph):
    size = len(graph.nodes)
    start_node = graph.nodes[0]
    end_node = int(start_node + size/2) % size

    print(f"Start node: {start_node}\nEnd node: {end_node}") 

    spath = nx.algorithms.bellman_ford_path(graph, start_node, end_node)
    print("\nShortest path: " + " -> ".join([str(n) for n in spath]))

    print("How long is the path among these farthest nodes? {}".format(
    len(spath) - 1))  # here we do -1 to avoid counting the starting node!
    print(f'Should be the same as the diameter of the graph!!!')

# Could alternatively use:
    # nx.shortest_path(graph, 'start_node', 'end_node', method='dijkstra')
    # nx.shortest_path(graph, 'start_node', 'end_node', method='bellman-ford')



# -----------------------
    

# iii) Compare against a random and regular graph
def print_random_graph_comparison(graph:nx.Graph):
    equivalent_random = get_equivalent_random_graph(graph)
    print_graph_statistics(equivalent_random)

    equivalent_regular = get_equivalent_regular_graph(graph)
    print_graph_statistics(equivalent_regular)


    
def get_equivalent_random_graph(graph:nx.Graph):
    # n : number of nodes
    # p : frequency of edge occurence
        # max edges: n (n - 1) / 2
        # frequency of edge occurence: number of edges / max edges
    n = graph.number_of_nodes()
    number_edges = graph.number_of_edges()
    max_edges = n(n - 1)/2
    p = number_edges/max_edges


    return np.erdos_renyi_graph(n=n, p=p)

def get_equivalent_regular_graph(graph:nx.Graph):
    regular_graph = nx.Graph()

    nodes = graph.number_of_nodes()

    regular_graph.add_nodes_from(list(range(nodes)))

    for node in graph.nodes():
        next_one = (node + 1) % nodes 
        jump_node = (node + 2) % nodes
        regular_graph.add_edge(node, next_one)
        regular_graph.add_edge(node, jump_node)

    fig, ax = plt.subplots(figsize=(10,10))
    nx.draw(regular_graph, pos=nx.circular_layout(graph), with_labels=True)
    return regular_graph


# -----------------------

# v) Two editors are connected iff they have both contributed to any thread in the same page, but not necessarily to the same thread? 


