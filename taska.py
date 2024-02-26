import networkx as nx
import csv

def parseWikiData(filepath):

    # CSV FORMAT:
    #   [0]             [1]         [2]
    #   thread_subject  username    pagename

    threadDictionary = {} #{pagename/thread: username, username}

    with open(filepath, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        next(csv_reader) # Skip header line
        for row in csv_reader: 
            key = f"{row[0]}/{row[2]}".replace("\n","")
            if threadDictionary.get(key) is None:
                threadDictionary[key] = [row[1]]
            else:
                threadDictionary[key].append(row[1])             

    G = nx.Graph()

    for key in threadDictionary.keys():
        userList = threadDictionary.get(key)
        G = _helperFunc(userList, G)
        
    print(len(threadDictionary.keys()))
    return G

def _helperFunc(userList, G: nx.graph):
    if len(userList) > 1:
            for i in range(0, len(userList) -1):
                for x in range(i + 1, len(userList)):
                        G.add_edge(userList[i], userList[x])
    elif len(userList) == 1:
         G.add_node(userList[0])
    return G

if __name__ == "__main__":
    import os
    import time
    import matplotlib.pyplot as pt

    node_quantity = []
    edge_quantity = []
    average_time_to_run = []
    dataset_name = []

    iterations = 1

    relative_folder_path = 'datasets/'
    file_names = [f for f in os.listdir(relative_folder_path) if os.path.isfile(os.path.join(relative_folder_path, f))]

    for file in file_names:
        total_time = 0.

        for i in range(0, iterations):
            start_time = time.time()
            G = parseWikiData(relative_folder_path + file)
            end_time = time.time()
            total_time += end_time - start_time
            if i == 0:
                node_quantity.append(len(G.nodes))
                edge_quantity.append(len(G.edges))
                dataset_name.append(file)
            del(G)        
        average_time_to_run.append(total_time / iterations)

    print("\n\n\n\n")
    for i in range(0,len(node_quantity)):
        #  print(f"{dataset_name[i]} | # of Nodes: {node_quantity[i]} | # of Nodes: {edge_quantity[i]} | Average time to run: {average_time_to_run[i]}")
        # print(f"({edge_quantity[i] / 1000},{average_time_to_run[i]})")    
        print(node_quantity[i])
    print("\n\n\n\n")
    for i in range(0,len(node_quantity)):
        #  print(f"{dataset_name[i]} | # of Nodes: {node_quantity[i]} | # of Nodes: {edge_quantity[i]} | Average time to run: {average_time_to_run[i]}")
        # print(f"({edge_quantity[i] / 1000},{average_time_to_run[i]})")    
        print(average_time_to_run[i])
    # print(f"{len(node_quantity)}{len(edge_quantity)}{len(dataset_name)}{len(average_time_to_run)}")
    