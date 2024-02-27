import networkx as nx
import matplotlib.pyplot as plt

colours = ['yellow', '#F4D4D3', '#E9A8A1', '#E9635E', '#CA1414', '#6B0003', 'black']

colours_with_label = {
    colours[0]: "infected",
    colours[1]: "(0, 0.1)",
    colours[2]: "[0.1, 0.2)",
    colours[3]: "[0.3, 0.4)",
    colours[4]: "[0.4, 0.5)",
    colours[5]: "[0.5, 1]",
    colours[6]: "not infected",
}


def get_colour(similarity: float) -> str:
    if 0 < similarity < 0.1:
        return colours[1]
    elif 0.1 <= similarity < 0.2:
        return colours[2]
    elif 0.2 <= similarity < 0.3:
        return colours[3]
    elif 0.3 <= similarity < 0.4:
        return colours[4]
    elif 0.4 <= similarity <= 1:
        return colours[5]


def display_graph(graph: nx.Graph) -> None:
    plt.figure(figsize=(10, 10))
    layout = nx.random_layout(graph)

    colors = [graph.nodes[node]['color'] for node in graph.nodes]
    sizes = [500 if graph.nodes[node]['color'] == 0 else 300 for node in graph.nodes]
    nx.draw(graph, layout, node_color=colors, node_size=sizes, with_labels=False)
    patches = [plt.plot([], [], marker="o", ms=10, ls="", mec=None, color=colour,
                        label="{:s}".format(label))[0] for colour, label in colours_with_label.items()]
    plt.legend(handles=patches, loc='upper right')
    plt.show()


def display_histogram(graph: nx.Graph) -> None:
    colors = [graph.nodes[node]['color'] for node in graph.nodes]
    color_counts = {color: colors.count(color) for color in set(colors) if color != colours[0]}
    color_labels = [colours_with_label[color] for color in color_counts.keys()]
    frequencies = list(color_counts.values())
    plt.xlabel("similarity range", fontsize=12, fontweight='bold')
    plt.ylabel("similar range occurrences", fontsize=12, fontweight='bold')
    bars = plt.bar(color_labels, frequencies, color=list(color_counts.keys()))
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom')
    plt.show()


def graph_degree_distribution_histogram(degrees):
    degrees_count = {}
    for i in degrees:
        count = i[1]
        if count in degrees_count:
            degrees_count[count] += 1
        else:
            degrees_count[count] = 1
    keys = list(degrees_count.keys())
    values = list(degrees_count.values())
    plt.bar(keys, values)
    plt.xticks(keys)


def colour_count(graph: nx.graph) -> dict:
    colour_dict = {}
    for c in colours:
        if c != colours[0] and c != colours[6]:
            colour_dict[c] = 0
    for node in graph.nodes:
        if graph.nodes[node]['color'] != colours[0] and graph.nodes[node]['color'] != colours[6]:
            if graph.nodes[node]['color'] not in colour_dict:
                colour_dict[graph.nodes[node]['color']] = 1
            else:
                colour_dict[graph.nodes[node]['color']] += 1
    return colour_dict


def plot_with_3_bars_per_bin(averages: dict,
                             datasets: list,
                             x_label: str,
                             y_label: str,
                             title: str):
    colors = list(colours_with_label.values())[1:-1]

    values_0 = list(averages[0].values())
    values_1 = list(averages[1].values())
    values_2 = list(averages[2].values())

    fig, ax = plt.subplots(figsize=(15, 6))
    bar_width = 0.25
    index = range(len(colors))

    bar1 = ax.bar(index, values_0, bar_width, color="red", label=f'{(datasets[0][:-4])}')
    bar2 = ax.bar([i + bar_width for i in index], values_1, bar_width, color="green", label=f'{datasets[1][:-4]}')
    bar3 = ax.bar([i + 2 * bar_width for i in index], values_2, bar_width, color="blue", label=f'{datasets[2][:-4]}')

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(colors)
    ax.legend()

    for bar in bar1 + bar2 + bar3:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., 1.01 * height,
                '%d' % int(height), ha='center', va='bottom')

    plt.show()
