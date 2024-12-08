import os
import time
import itertools
import math 


# Main method
def main():
 
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/antennamap.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
    maxX = len(lines[0].strip())
    maxY = len(lines)

    antennas = {}
    cityMap = {}
    for j, line in enumerate(lines):
        for i,  c in enumerate(line.strip()):
            cityMap[(i, j)] = c
            if not c ==  ".":
                if c in antennas:
                    antennas[c].append((i, j))
                else:
                    antennas[c] = [(i, j)]
    
    # print map
    # for j in range(maxY):
    #     for i in range(maxX):
    #         print(cityMap[(i, j)], end="")
    #     print()

    nodes = set()
    for frequency in antennas:
        combinations = list(itertools.combinations(antennas[frequency], 2))   
        #print(frequency, combinations)
        for combination in combinations:
            #print(combination)
            distanceAntennas = math.sqrt((combination[0][0] - combination[1][0])**2 + (combination[0][1] - combination[1][1])**2)
            #print(distanceAntennas)
            unitvector = ((combination[1][0] - combination[0][0])/distanceAntennas, (combination[1][1] - combination[0][1])/distanceAntennas)
            #print(unitvector)
            #print((int(combination[0][0] + unitvector[0]*distanceAntennas), int(combination[0][1] + unitvector[1]*distanceAntennas)))
            distanceNode = (combination[0][0] - combination[1][0])/unitvector[0]
            #print(distanceNode)

            node1 = (int(combination[0][0] + unitvector[0]*distanceNode), int(combination[0][1] + unitvector[1]*distanceNode))
            node2 = (int(combination[0][0] - unitvector[0]*2*distanceNode), int(combination[0][1] - unitvector[1]*2*distanceNode))
            if node1 in cityMap: 
                nodes.add(node1)
            if node2 in cityMap:
                nodes.add(node2)
    #print(nodes)
    
    print("Unique nodes", len(nodes))
    endtime = time.time()
    print("Time taken;" , endtime - start_time)
    print("Time taken in ms;", (endtime - start_time) * 1000)



    nodesNew = set()
    tolerance = 1e-9
    for frequency in antennas:
        combinations = list(itertools.combinations(antennas[frequency], 2))   
        #print(frequency, combinations)
        for combination in combinations:
            #print("Combination", combination)
            #print(combination)
            distanceAntennas = math.sqrt((combination[0][0] - combination[1][0])**2 + (combination[0][1] - combination[1][1])**2)
            #print(distanceAntennas)
            unitvector = ((combination[1][0] - combination[0][0])/distanceAntennas, (combination[1][1] - combination[0][1])/distanceAntennas)
            #print(unitvector)
            #print((int(combination[0][0] + unitvector[0]*distanceAntennas), int(combination[0][1] + unitvector[1]*distanceAntennas)))
            for i in range(maxY):
                posNodeX = ((i-combination[0][1])*unitvector[0])/unitvector[1] + combination[0][0]
                
                # Check if posNodeX is close enough to an integer
                if abs(posNodeX - round(posNodeX)) < tolerance:
                    posNodeX = round(posNodeX)
                else:
                    continue
                #print("i",i,"PosNodeX", posNodeX, "coord", (posNodeX, i), combination)    
                posNode = (posNodeX, i)
                if posNode in cityMap:
                    nodesNew.add(posNode)

            
    #print(nodesNew)
    print("Unique nodes", len(nodesNew))
    endtimeP2 = time.time()
    print("Time taken;" , endtimeP2 - endtime)
    print("Time taken in ms;", (endtimeP2 - endtime) * 1000)
    
    # print map
    # for j in range(maxY):
    #     for i in range(maxX):
    #         if (i,j) in nodesNew and cityMap[(i, j)] == ".":
    #             print("X", end="")
    #         else:
    #             print(cityMap[(i, j)], end="")
    #     print()
    

            




if __name__ == "__main__":
    main()