import os
import time

import matplotlib.pyplot as plt
import networkx


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/lan.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    wireGraph = networkx.Graph()
    for line in lines:
        line.strip()
        source, dest = line.split("-")
        wireGraph.add_edge(source, dest.strip(), capacity=1)
    

    #nodeList = list(wireGraph.nodes())
    #print(nodeList)
    #networkx.draw(wireGraph, with_labels=True)
    #plt.show()

    #came to this after solved P2, slower than my original onem but cool to learn...
    # allCliques = [clique for clique in networkx.enumerate_all_cliques(wireGraph) if len(clique) == 3]
    # #print(len(allCliques))  
    # setsWithT = 0 
    # for clique in allCliques:
    #     if len(clique) == 3:
    #         for node in clique:
    #             if node.startswith("t"):
    #                 setsWithT += 1
    #                 break
    

    threeset = findthreesets(wireGraph)
    setsWithT = 0
    for threes in threeset:
        #print(threes)
        for node in threes:
            if node.startswith("t"):
                setsWithT += 1
                break
    #print(len(threeset))
    print(setsWithT)
    end_timeP1 = time.time()
    print("Part 1 took: ", end_timeP1 - start_time)
    print("Part 1 took in ms: ", (end_timeP1 - start_time) * 1000)


    cliques = list(networkx.find_cliques(wireGraph))
    #print(len(cliques)) 
    biggestClique = max(cliques, key=len)
    #print(biggestClique)
    #print(len(biggestClique))
    biggestCliqueSorted = sorted(biggestClique)
    #print(biggestCliqueSorted)
    print(",".join(biggestCliqueSorted))
    end_timeP2 = time.time()
    print("Part 2 took: ", end_timeP2 - end_timeP1)
    print("Part 2 took in ms: ", (end_timeP2 - end_timeP1) * 1000)

def findthreesets(graph):
    threeset = set()
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        if len(neighbors) < 2:
            continue
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if graph.has_edge(neighbors[i], neighbors[j]):
                    threeset.add(frozenset([node, neighbors[i], neighbors[j]]))
    return threeset


if __name__ == "__main__":
    main()
