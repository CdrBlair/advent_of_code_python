import os
import time
from functools import cache
from itertools import count


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/gardenmap.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    gardenMap = {}
    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            gardenMap[(j, i)] = char
            if char == "S":
                start = (j, i)
                gardenMap[start] = "."

    maxX = max([x[0] for x in gardenMap.keys()])
    maxY = max([x[1] for x in gardenMap.keys()])

    # print Gargden map
    for i in range(maxY + 1):
        for j in range(maxX + 1):
            print(gardenMap[(j, i)], end="")
        print()
    gardenMap = tuple(gardenMap.items())
    stepsElf = 64
    # P2 manual variants
    start = (0, 0)
    current = [start]
    for i in range(stepsElf):
        newPositions = set()
        for coord in current:
            newPositions.update(findAllowedNeigbours(coord, gardenMap, maxX, maxY))
        current = newPositions.copy()

    gardenMap = dict(gardenMap)

    print()
    # print Gargden map
    for i in range(maxY + 1):
        for j in range(maxX + 1):
            if (j, i) in current:
                print("O", end="")
            else:
                print(gardenMap[(j, i)], end="")
        print()
    print(len(current))
    # get mins and max of current
    minX = min([x[0] for x in current])
    maxX = max([x[0] for x in current])
    minY = min([x[1] for x in current])
    maxY = max([x[1] for x in current])
    print(minX, maxX, minY, maxY)
    # all # between minX and maxX and minY and maxY
    countRocks = 0
    countTiles = 0
    for i in range(minY, maxY + 1):
        for j in range(minX, maxX + 1):
            if gardenMap[(j, i)] == "#":
                countRocks += 1
            elif (j, i) not in current:
                countTiles += 1
    print(countRocks)
    print(countTiles)
    print("cache info: ", findAllowedNeigbours.cache_info())
    print("Time taken p1: ", time.time() - start_time)
    print("time p1 in ms: ", (time.time() - start_time) * 1000)

    # P2 Pen and Paper: sketching the evolving diamond shape, calcumatlting the two different full filled shapes with above as well as the edge cased, put into calculator


# Find allowed neigbhours
@cache
def findAllowedNeigbours(current, gardenMap, maxX, maxY):
    gardenMap = dict(gardenMap)

    allowedNeigbours = set()
    # check above
    if current[1] > 0:
        if gardenMap[(current[0], current[1] - 1)] == ".":
            allowedNeigbours.add((current[0], current[1] - 1))
    # check below
    if current[1] < maxY:
        if gardenMap[(current[0], current[1] + 1)] == ".":
            allowedNeigbours.add((current[0], current[1] + 1))
    # check left
    if current[0] > 0:
        if gardenMap[(current[0] - 1, current[1])] == ".":
            allowedNeigbours.add((current[0] - 1, current[1]))
    # check right
    if current[0] < maxX:
        if gardenMap[(current[0] + 1, current[1])] == ".":
            allowedNeigbours.add((current[0] + 1, current[1]))
    return allowedNeigbours


if __name__ == "__main__":
    main()
