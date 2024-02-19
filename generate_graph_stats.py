from taska import parseWikiData

def something(G):
    degrees = list(G.degree())
    nodes_1_degree = []
    for node_degree in degrees:
         if node_degree[1] == 1:
              nodes_1_degree.append(node_degree[0])

    print(f"Nodes that have 1 degree: {len(nodes_1_degree)}")
    return(nodes_1_degree)

def top_degrees(G):
    degrees = list(G.degree())
    degrees.sort(key = lambda x : x[1])
    print(degrees[-2:])
    return degrees[-2:]

if __name__ == "__main__":
    filepath = "datasets/WIKIPROJECTS.csv"
    filepath2 = "datasets/REQUEST_FOR_DELETION.csv"

    import os
    folder_path = 'datasets'
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for file in file_names:
         G = parseWikiData(filepath = "datasets/" + file)
         print(f"\n{file}\nTop two nodes with most degrees:")
         top_degrees(G)
         x = len(something(G))
         print(f"Number of nodes: {G.number_of_nodes()}")
         print(f"Precentage of nodes with 1 degree: {x/G.number_of_nodes()}")
        

    # G = parseWikiData(filepath=filepath)
    # something(G)
    # top_nodes = top_degrees(G)
    # G.remove_node(top_nodes[0][0])
    # G.remove_node(top_nodes[1][0])
    # top_degrees(G)
    # x = something(G)
    # n_names = []
    # for nodes in x:
    #     neighbors = list(G.neighbors(nodes))
    #     n_names.append(neighbors[0])
    # print(set(n_names))
        