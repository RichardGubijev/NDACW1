import time
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
        G = _helperFunc(userList, G)

    return G

def _parseWikiDataFast_CURRENTLYBROKENDONOTUSE(filepath):
    # This function exploits the fact that the CSV files are ordered by page name and thread subject
    # So no need to create a dictionary
    # CURRENTLY DOES NOT WORK, WHEN COMPARED TO THE OTHER FUNCTION IT DOES NOT RETURN AN ISOMORPHOIC FUNCTION

    prevThreadSubject = ""
    prevPageName = ""
    userList = []
    G = nx.Graph()

    with open(filepath, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        next(csv_reader) # Skip header line
        for row in csv_reader:
            if prevThreadSubject != row[0] or prevPageName != row[2]:
                G = _helperFunc(userList, G)
                userList = []
                prevThreadSubject = row[0]
                prevPageName = row[2]
            userList.append(row[1])

    return G

def _helperFunc(userList, G):

    if len(userList) == 1:
        G.add_node(userList[0])
    else:
        for i in range(0, len(userList) -1):
            for x in range(i + 1, len(userList)):
                    G.add_edge(userList[i], userList[x])
    return G

if __name__ == "__main__":
    filepath = "datasets/WIKIPROJECTS.csv"
    filepath2 = "datasets/REQUEST_FOR_DELETION.csv"
    G1time1 = time.time()
    G1 = parseWikiData(filepath=filepath)
    G1time2 = time.time()
    G2time1 = time.time()
    G2 = parseWikiData(filepath=filepath2)
    G2time2 = time.time()
    print(f'Are the two graphs isomorphic?: {nx.is_isomorphic(G1, G2)}')
    print(f"Time taken to parse CSV into a graph  {G1time2 - G1time1}")
    print(f"Time taken to parse CSV into a graph2 {G2time2 - G2time1}")
    nx.draw(G1, with_labels = False)
    plt.show()
