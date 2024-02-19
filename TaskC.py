import networkx as nx
import matplotlib.pyplot as plt
from taska import parseWikiData
from random import sample
import statistics

# TODO: fix up the histograms to only show the valid values for the x axis
# We are doing cascade model BUT in addition, if a user has les degrees than average or median we do not allow that action to cascades degrees than average or median we do not allow that action to cascade

THRESHOLD = 0.8
datasets = ['INTERWIKI_CONFLICT.csv', 'REQUEST_FOR_DELETION.csv', 'WIKIPROJECTS.csv']
path = 'datasets/'
# networks = [parseWikiData(path + datasets[0]), parseWikiData(path + datasets[1]), parseWikiData(path + datasets[2])]
networks = [parseWikiData(path + datasets[1])]

G = networks[0]

def calculate_stats(G: nx.graph):
    degrees = nx.degree(G)
    degree_values = [deg[1] for deg in degrees]
    return statistics.mean(degree_values), statistics.median(degree_values)

def graph_degree_distribution_histogram(degrees):
    degrees_count = {}
    for i in degrees:
        count = i[1]
        if (count in degrees_count):
            degrees_count[count] += 1
        else:
            degrees_count[count] = 1
            
    print(degrees_count.keys())
    keys = list(degrees_count.keys())
    values = list(degrees_count.values())
    plt.bar(keys, values)
    plt.xticks(keys)

def sorted_nodes(G: nx.graph): 
    degrees = nx.degree(G)
    sorted_degrees = sorted(degrees, key= lambda x : x[1])
    nodes = [node[0] for node in sorted_degrees]
    return nodes

def save_values_to_file(filename, values): 
    value_string = ""
    for value in values:
        value_string += f","

def get_2_random_nodes(G: nx.graph):
    degrees = list(nx.degree(G))
    valid_nodes = []
    for x in degrees:
        if x[1] > 1:  # Show why this is abnormal -> median and histogram
            valid_nodes.append(x[0])
    
    random_nodes = sample(valid_nodes, 2)
    return random_nodes

def get_2_well_connected(nodes):
    return nodes[-2:]

def get_2_not_well_connctd(nodes):
    return nodes[:2]

def get_degrees(degree_values, nodes):
    for x in degree_values:
        for n in nodes:
            if n == x[0]:
                print(x[1])

def get_node_degree(G: nx.graph, node):
    degrees = nx.degree(G)
    for x in degrees:
        if x[0] == node:
            return x[1]

def get_neighbors(G: nx.graph, node):
    return list(G.neighbors(node))

def infected_negibhors_ratio(infected_nodes, node_neghibors):
    infected_nodes = set(infected_nodes)
    node_neghibors = set(node_neghibors)
    return len(infected_nodes & node_neghibors) / len(node_neghibors)


degrees = dict(nx.degree(G))

def cascasde(G:nx.graph, infected_nodes: list, exclusion_theshold: int):
    for node in infected_nodes:
        for x in get_neighbors(G, node):
            if x in infected_nodes:
                pass
            elif degrees[x] < exclusion_theshold:
                pass
            elif infected_negibhors_ratio(G.neighbours(node), G.neighbors(x)) >= THRESHOLD:
                infected_nodes.append(x)
    return infected_nodes


# print(graph_degree_distribution_histogram(G.degree()))

# TODO refine spread critera to ans question 1
    #! get the shortest path to the max node 
    #! get average path to the max node? is the shortest path close?
# TODO Create a priority list from the cascade to investigate whether they are trolls
    #! Maybe with shortest path to early adopters or amount of neighbors connected which are infected?
    #! Or look at the max degree here as well
    
# networkx.classes.reportviews.DegreeView
# something:  nx.classes.reportviews.DegreeView = nx.degree(G)
# degree_values = something.
# nodes = sorted_nodes(G)


# well_connected = get_2_well_connected(nodes)

# cascaded_nodes = cascasde(G, well_connected, 0.5, 3)
# print(cascaded_nodes)


# import networkx as nx
# import ndlib.models.ModelConfig as mc
# import ndlib.models.epidemics as ep



# model = ep.ThresholdModel(G)
# cfg = mc.Configuration()

# infected_nodes = set(get_2_random_nodes(G))
# cfg.add_model_initial_configuration("Infected", infected_nodes)

# def infection_chance(node, graph):
#     neighbors = graph.neighbors(node)
    
#     value = infected_negibhors_ratio(neighbors, infected_nodes)
#     if value > THRESHOLD:
#         return 1
#     else:
#         return 0

# for i in G.nodes():
#     cfg.add_node_configuration("threshold", i, infection_chance(i, G))

# model.set_initial_status(cfg)


# iterations = model.iteration_bunch(1)
# node_status = iterations[0]["status"]

# for key in node_status.key():
#     if node_status[key] == 1:
#         infected_nodes.append(key)
