import networkx as nx
import matplotlib.pyplot as plt
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
        if len(userList) != 1:
            for i in range(0, len(userList) -1):
                for x in range(i + 1, len(userList)):
                    G.add_edge(userList[i], userList[x])
    return G

if __name__ == "__main__":
    filepath = "datasets/WIKIPROJECTS.csv"
    G = parseWikiData(filepath=filepath)
    nx.draw(G, with_labels = True)
    plt.show()