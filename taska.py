import networkx as nx
import matplotlib.pyplot as plt
import csv

## Current problem: Sometimes the subject names are surronded with "" and have , in them


filepath = "datasets/WIKIPROJECTS.csv"

#   [0]             [1]         [2]
#   thread_subject  username    pagename

threadDictionary = {} #{pagename/thread: username, username}

with open(filepath, "r", encoding="utf-8") as file:
    file.readline() # Skip heading line
    for line in file: 
        row = line.replace("\n","").split(",")
        key = f"{row[0]}/{row[2]}"
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
                if userList[i] == userList[x]:
                    print(userList)

nx.draw(G, with_labels = False)
plt.show()