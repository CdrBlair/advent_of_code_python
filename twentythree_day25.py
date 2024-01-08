import os
import random
import time
from itertools import combinations

import matplotlib.pyplot as plt
import networkx


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/wires.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    wireGraph = networkx.Graph()
    for line in lines:
        line.strip()
        source, dests = line.split(":")
        for dest in dests.strip().split(" "):
            wireGraph.add_edge(source, dest.strip(), capacity=1)

    nodeList = list(wireGraph.nodes())

    networkx.draw(wireGraph, with_labels=True)
    plt.show()
    for rsource, rsink in combinations(nodeList, 2):
        # if random gives the same go on
        if rsource == rsink:
            continue
        cut, partitionSet = networkx.minimum_cut(wireGraph, rsource, rsink)

        if cut == 3:
            break

    print(partitionSet)
    print("Result: ", len(partitionSet[0]) * len(partitionSet[1]))
    endtimeP1 = time.time()
    print("Part 1 time: ", endtimeP1 - start_time)
    print("Part 1 time in ms: ", (endtimeP1 - start_time) * 1000)


if __name__ == "__main__":
    main()
