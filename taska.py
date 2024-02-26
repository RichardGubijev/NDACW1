import networkx as nx
import csv

def parseWikiData(filepath):

    # CSV FORMAT:
    #   [0]             [1]         [2]
    #   thread_subject  username    pagename

    threadDictionary = {}  #{pagename/thread: [user1, user2]}

    with open(filepath, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        next(csv_reader) # Skip header line
        for row in csv_reader: 
            # Mulitple threads might have the same thread_subject, 
            # so to differinate them combine them with page name
            key = f"{row[0]}/{row[2]}".replace("\n","") 
            if threadDictionary.get(key) is None:
                threadDictionary[key] = [row[1]]
            else:
                threadDictionary[key].append(row[1])             

    G = nx.Graph()

    # For each thread in the dictionary, add all the permuations of relationships
    # between the users. 
    for key in threadDictionary.keys():
        userList = threadDictionary.get(key)
        G = _add_all_perumations_of_relationships(userList, G)
        
    return G

def ParseWikiDataWithThreadsLength(filepath):
    # Same function as parseWikiData(), but also returns number of threads
    threadDictionary = {} 
    with open(filepath, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        next(csv_reader) 
        for row in csv_reader: 
            key = f"{row[0]}/{row[2]}".replace("\n","")
            if threadDictionary.get(key) is None:
                threadDictionary[key] = [row[1]]
            else:
                threadDictionary[key].append(row[1])             

    G = nx.Graph()

    for key in threadDictionary.keys():
        userList = threadDictionary.get(key)
        G = _add_all_perumations_of_relationships(userList, G)
        
    return G, len(threadDictionary.keys())

def _add_all_perumations_of_relationships(userList, G):
    if len(userList) > 1:
            for i in range(0, len(userList) -1):
                for x in range(i + 1, len(userList)): # Don't add I and I as a relationship
                        # Networkx handles creating the nodes if they don't already exist, so add_edge is all that's needed to add the nodes. 
                        G.add_edge(userList[i], userList[x])
    elif len(userList) == 1: 
        # If list length is == 1, just add the node to the graph. Sometimes nodes don't have relationships to any other node.
        G.add_node(userList[0])
    return G

if __name__ == "__main__":
    import os
    import time
    import matplotlib.pyplot as pt

    node_quantity = []
    edge_quantity = []
    thread_quantity = []
    average_time_to_run = []
    dataset_name = []

    iterations = 100

    relative_folder_path = 'datasets/'
    csv_filename = "task_a_runtime_preformance_stats.csv"
    files = [f for f in os.listdir(relative_folder_path) if os.path.isfile(os.path.join(relative_folder_path, f)) and f.endswith(".csv")]
    # Create a list of all files in "relative_folder_path" that end with CSV

    print(f"Generating statistics for datasets in '{relative_folder_path}'")
    print(f"Preforming {iterations} iteration(s)")

    # Calculate the average runtime for parseWikiData() with all the datasets in the files folder. 
    for file in files:
        total_time = 0.
        for i in range(0, iterations):
            start_time = time.time()
            G, number_of_threads = ParseWikiDataWithThreadsLength(relative_folder_path + file)
            end_time = time.time()
            total_time += end_time - start_time
            if i == 0:
                node_quantity.append(len(G.nodes))
                edge_quantity.append(len(G.edges))
                thread_quantity.append(number_of_threads)
                dataset_name.append(file)
            del(G)        
        average_time_to_run.append(total_time / iterations)

    print(f"Writing to {csv_filename}")

    with open(csv_filename, "w", newline="") as csv_file: 
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["dataset name", "average run time", "node quantity", "edge quantity", "thread quantity"])
        for i in range(0, len(node_quantity)):
            csv_writer.writerow([dataset_name[i], average_time_to_run[i], node_quantity[i], edge_quantity[i], thread_quantity[i]])
    
    print("Done")
