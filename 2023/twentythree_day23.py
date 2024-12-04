import os
import time
from collections import deque
from heapq import heappop, heappush


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/hikemap.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    gardenMap = {}
    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            gardenMap[(j, i)] = char

    maxX = max([x[0] for x in gardenMap.keys()])
    maxY = max([x[1] for x in gardenMap.keys()])

    # Print Map
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(gardenMap[(x, y)], end="")
    #     print()
    # print()

    # State is current coord, steps, before coord, visited places
    start = ((1, 0), 0, None, frozenset())
    queue = deque([start])
    visited = set()
    possiblePaths = set()

    currentLongetPath = {}
    while queue:
        current = queue.popleft()
        if current[0] == (maxX - 1, maxY):
            possiblePaths.add(current[1])
            continue
        if current in visited:
            continue
        visited.add(current)
        if (
            current[0] in currentLongetPath
            and currentLongetPath[current[0]] >= current[1]
        ):
            continue

        currentLongetPath[current[0]] = current[1]

        alreadySeen = set(current[3])
        alreadySeen.add(current[0])
        # normale tiles
        # print(current)
        # print(gardenMap[current[0]])
        if gardenMap[current[0]] == ".":
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                newCoord = (current[0][0] + direction[0], current[0][1] + direction[1])
                if (
                    newCoord not in alreadySeen
                    and newCoord in gardenMap
                    and gardenMap[newCoord] != "#"
                ):
                    queue.append(
                        (newCoord, current[1] + 1, current[0], frozenset(alreadySeen))
                    )
        else:
            if gardenMap[current[0]] == "<":
                direction = (-1, 0)
            elif gardenMap[current[0]] == ">":
                direction = (1, 0)
            elif gardenMap[current[0]] == "^":
                direction = (0, -1)
            elif gardenMap[current[0]] == "v":
                direction = (0, 1)
            newCoord = (current[0][0] + direction[0], current[0][1] + direction[1])
            if (
                newCoord not in alreadySeen
                and newCoord in gardenMap
                and gardenMap[newCoord] != "#"
            ):
                queue.append(
                    (newCoord, current[1] + 1, current[0], frozenset(alreadySeen))
                )

    print(possiblePaths)
    print("Longest Path: ", max(possiblePaths))
    endTime = time.time()
    print("Time P1 elapsed:", endTime - start_time)
    print("Time P1 in ms:", (endTime - start_time) * 1000)

    # P2
    starttimeP2 = time.time()
    # Replace <, >, ^, v with .
    # for key in gardenMap:
    #     if gardenMap[key] in ["<", ">", "^", "v"]:
    #         gardenMap[key] = "."

    start = (1, 0)

    conjuctions = {}
    queue = deque([start])

    visitedStart = set()
    beforeStart = set()
    # find Path betwenn conjunctions
    while queue:
        currentStart = queue.popleft()
        beforeStart.add(currentStart)
        if currentStart in visitedStart:
            continue
        visitedStart.add(currentStart)
        visited = set()

        current = currentStart
        # possible directions
        possible = []
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            newCoord = (current[0] + direction[0], current[1] + direction[1])
            if newCoord in gardenMap and gardenMap[newCoord] != "#":
                possible.append(newCoord)
        visited.add(current)
        for coord in possible:
            foundConjunction = False

            steps = 1
            pathStart = coord
            visited.add(pathStart)
            while not foundConjunction:
                # possible directions
                possible = []
                for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    newCoord = (
                        pathStart[0] + direction[0],
                        pathStart[1] + direction[1],
                    )
                    if (
                        newCoord in gardenMap
                        and gardenMap[newCoord] != "#"
                        and newCoord not in visited
                    ):
                        possible.append(newCoord)

                if len(possible) == 1:
                    pathStart = possible[0]
                    visited.add(pathStart)
                    steps += 1
                else:
                    foundConjunction = True
                    if currentStart not in conjuctions:
                        conjuctions[currentStart] = {}
                    conjuctions[currentStart][pathStart] = steps
                    queue.append(pathStart)

    # Takes roughly 10 minutes, use with caution
    # queue = deque([startState])
    # visited = set()
    # finalPaths = []
    # while queue:
    #     # print(queue)
    #     current = queue.popleft()
    #     if current[0] == end:
    #         finalPaths.append(current[2])
    #         continue
    #     if current in visited:
    #         continue
    #     visited.add(current)

    #     for key in conjuctions[current[0]]:
    #         if key != current[1]:
    #             alreadySeen = set(current[3])
    #             alreadySeen.add(current[0])
    #             if key not in alreadySeen:
    #                 queue.append(
    #                     (
    #                         key,
    #                         current[0],
    #                         current[2] + conjuctions[current[0]][key],
    #                         frozenset(alreadySeen),
    #                     )
    #                 )

    # print(finalPaths)
    # print("Shortest Path: ", max(finalPaths))
    print(conjuctions)
    # this only takes 2 seconds
    maxLenght = recursiveLength((1, 0), (maxX - 1, maxY), conjuctions, set())
    print("Longest Path: ", maxLenght)
    endTimeP2 = time.time()
    print("Time P2 elapsed:", endTimeP2 - starttimeP2)
    print("Time P2 in ms:", (endTimeP2 - starttimeP2) * 1000)
    print("Time elapsed:", endTimeP2 - start_time)
    print("Time in ms:", (endTimeP2 - start_time) * 1000)


def recursiveLength(start, end, conjutionList, before):
    if end in conjutionList[start]:
        return conjutionList[start][end]
    else:
        max = -1
        for key in conjutionList[start]:
            if key not in before:
                before.add(key)
                intermediate = (
                    recursiveLength(key, end, conjutionList, before)
                    + conjutionList[start][key]
                )
                if intermediate > max:
                    max = intermediate
        return max


if __name__ == "__main__":
    main()
