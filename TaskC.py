import networkx as nx
import matplotlib.pyplot as plt
from taska import parseWikiData
from math import floor, ceil

# We are doing cascade model BUT in addition, if a user has les degrees than average or median we do not allow that action to cascades degrees than average or median we do not allow that action to cascade

datasets = ['INTERWIKI_CONFLICT.csv', 'REQUEST_FOR_DELETION.csv', 'WIKIPROJECTS.csv']
path = 'datasets/'
# networks = [parseWikiData(path + datasets[0]), parseWikiData(path + datasets[1]), parseWikiData(path + datasets[2])]
networks = [parseWikiData(path + datasets[1])]
G = networks[0]

def calculateStats(G: nx.graph):
    degrees = nx.degree(G)
    degree_values = (deg[1] for deg in degrees)
    avg_degree = sum(degree_values)/len(degrees)
    sorted_degrees = sorted(degree_values)
    median: int
    if len(sorted_degrees)%2 == 0:
        median = sorted_degrees[len(sorted_degrees)/2]
    else: 
        mid_bot = floor(len(sorted_degrees)/2)
        mid_top = ceil(len(sorted_degrees)/2)
        median = (sorted_degrees[mid_bot] + sorted_degrees[mid_top])/2
    return median, avg_degree

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
    plt.show()


median, avg_deg= calculateStats(G)
print(f"avg degree: {avg_deg}, the median: {median}")




