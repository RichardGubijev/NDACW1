from taska import parseWikiData
import os

def count_1_degree_nodes(G):
    degrees = list(G.degree())
    nodes_1_degree = []
    for node_degree in degrees:
         if node_degree[1] == 1:
              nodes_1_degree.append(node_degree[0])
    return(nodes_1_degree)

def top_2_degree_nodes(G):
    degrees = list(G.degree())
    degrees.sort(key = lambda x : x[1])
    return degrees[-2:]

if __name__ == "__main__":
    with open("datasets_statistics.txt", "w", encoding='utf-8') as stats_file:
        folder_path = 'datasets'
        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        for file in file_names:
            G = parseWikiData(filepath = "datasets/" + file)
            stats_file.write(f"{file}\nTop two nodes with most degrees:")
            top_degree_nodes = top_2_degree_nodes(G)
            stats_file.write("\n")
            stats_file.write(f"{str(top_degree_nodes)}\n")
            x = len(count_1_degree_nodes(G))
            stats_file.write(f"Nodes that have 1 degree: {x}\n")
            stats_file.write(f"Number of nodes: {G.number_of_nodes()}\n")
            stats_file.write(f"Precentage of nodes with 1 degree: {x/G.number_of_nodes()}\n\n")
        
        