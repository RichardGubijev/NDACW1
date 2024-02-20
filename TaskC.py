import networkx as nx
from taska import parseWikiData
import enum
from helpers import get_neighbors, similarity_measure, get_2_random_nodes, calculate_stats, sorted_nodes
import matplotlib.pyplot as plt
from decimal import Decimal

THRESHOLD = 0.8


class Stats(enum.Enum):
    MEAN = 1
    MEDIAN = 2


class TaskC:
    def __init__(self, G: nx.graph) -> None:
        self.G = G
        self.mean, self.median = calculate_stats(G)
        self.degrees = dict(nx.degree(G))
        self.sorted_nodes = sorted_nodes(G)
        self.random_nodes = get_2_random_nodes(G)

    def node_similarity(self, current_node_neighbours: list) -> dict:
        node_similarity = {}
        for neighbouring_node in current_node_neighbours:
            neighbouring_node_neighbours = get_neighbors(G, neighbouring_node)
            node_similarity[neighbouring_node] = {
                'similarity': similarity_measure(current_node_neighbours, neighbouring_node_neighbours),
                'degree': len(neighbouring_node_neighbours),
                'neighbors': neighbouring_node_neighbours,
            }
        return node_similarity

    def question_one(self, stat_measure) -> dict:
        random_node_neighbours = {}
        for node in self.random_nodes:
            random_node_neighbours[node] = get_neighbors(self.G, node)
        node_similarity = {}
        for n in random_node_neighbours:
            current_node_neighbours = get_neighbors(G, n)
            if len(current_node_neighbours) > stat_measure:
                node_similarity[n] = self.node_similarity(current_node_neighbours)
        return node_similarity

    def graph_question_one(self, node_similarity: dict, threshold: float, stat_measure):
        G = nx.Graph()
        for node in node_similarity:
            G.add_node(node, color=0)
            for neighbor in node_similarity[node]:
                if node_similarity[node][neighbor]['degree'] > stat_measure: #and node_similarity[node][neighbor]['similarity'] > threshold:
                    colour = 1
                else:
                    colour = 2
                G.add_node(neighbor, color=colour)
                G.add_edge(node, neighbor)

                #! don't delete this, uncomment and see for yourself
                # for next_neighbor in node_similarity[node][neighbor]['neighbors']:
                #     if G.has_node(next_neighbor):
                #         pass
                #     else:
                #         G.add_node(next_neighbor, color=3)
                #     G.add_edge(neighbor, next_neighbor)

        color_map = {0: 'yellow',     # initial node
                     1: 'red',        # infected node
                     2: 'lightgreen',  # not infected
                     3: 'black'       # not considered
        }
        size_map = {0: 500,
                    1: 300,
                    2: 200,
                    3: 5,

        }

        # Draw the graph with specific node colors and sizes
        pos = nx.spring_layout(G)
        nx.draw_networkx_edges(G, pos, width=0.5)  # Adjust the number as needed

        # Draw the graph with specific node colors and sizes
        nx.draw(G, pos, with_labels=False,
                node_color=[color_map[G.nodes[node]['color']] for node in G.nodes],
                node_size=[size_map[G.nodes[node]['color']] for node in G.nodes]
                )

        # Draw the red nodes again with smaller size and white color to create a "ring" effect
        draw_black_nodes = [node for node in G.nodes if G.nodes[node]['color'] == 3]
        nx.draw_networkx_nodes(G, pos, nodelist=draw_black_nodes, node_color='white',
                               node_size=2)  # Adjust the number as needed

        green_nodes = [node for node in G.nodes if G.nodes[node]['color'] == 2]
        nx.draw_networkx_nodes(G, pos, nodelist=green_nodes, node_color='lightgreen',
                               node_size=[size_map[G.nodes[node]['color']] for node in green_nodes])

        red_node = [node for node in G.nodes if G.nodes[node]['color'] == 1]
        nx.draw_networkx_nodes(G, pos, nodelist=red_node, node_color='red',
                               node_size=[size_map[G.nodes[node]['color']] for node in red_node])

        yellow_nodes = [node for node in G.nodes if G.nodes[node]['color'] == 0]
        nx.draw_networkx_nodes(G, pos, nodelist=yellow_nodes, node_color='yellow',
                               node_size=[size_map[G.nodes[node]['color']] for node in yellow_nodes])
        plt.show()


    def question_two(self, node_similarity: dict):
        priority = {}
        for node in node_similarity:
            new_dict = {}
            for neighbour in node_similarity[node]:
                similarity = Decimal(node_similarity[node][neighbour]['similarity'])
                degree = Decimal(node_similarity[node][neighbour]['degree'])
                new_dict[neighbour] = similarity * degree
            priority[node] = sorted(new_dict.items(), reverse=True)
        print(priority)

    def run(self, threshold, stat_measure):
        node_similarity = self.question_one(stat_measure)
        self.graph_question_one(node_similarity, threshold, stat_measure)

        self.question_two(node_similarity)


if __name__ == "__main__":
    datasets = ['INTERWIKI_CONFLICT.csv', 'REQUEST_FOR_DELETION.csv', 'WIKIPROJECTS.csv']
    path = 'datasets/'
    networks = [parseWikiData(path + datasets[0])]
    G = networks[0]
    tasks_c = TaskC(G)
    threshold = 0.5
    stat_measure = 1
    tasks_c.run(threshold=threshold, stat_measure=stat_measure)


# Demonstrated understanding of network data analysis concepts and how they can
# apply to the questions in the coursework tasks.

# Technical ability in using programming to tackle a data analytics problem, showing
# ability to research and apply data manipulation techniques as required for the
# problem.
