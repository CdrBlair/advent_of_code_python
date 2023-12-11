import os
import time
from collections import deque
from itertools import combinations
from multiprocessing import Pool


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/galaxies.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    map = {}
    galaxies = []
    emptyRows = set()
    emptyColumns = set()

    for i, line in enumerate(lines):
        row_empty = True
        for j, char in enumerate(line.strip()):
            map[(j, i)] = char
            if char == "#":
                row_empty = False
                galaxies.append((j, i))
        if row_empty:
            emptyRows.add(i)

    # Find the original columns
    original_columns = set(x for x, y in map.keys())
    max_x = max(x for x, y in map.keys())

    # Iterate over the original columns in descending order
    for column in original_columns:
        if checkIfEmpty(map, column, max_x) == True:
            emptyColumns.add(column)

    # for coord in map.keys():
    #     if map[coord] == "#":
    #         galaxies.append(coord)

    # Print map
    # for i in range(max(y for x, y in map.keys()) + 1):
    #     for j in range(max(x for x, y in map.keys()) + 1):
    #         print(map[(j, i)], end="")
    #     print()

    galaxiesCombinations = list(combinations(galaxies, 2))

    # Find shortest path between all galaxy pairs
    # print("Number of galaxy pairs:", len(galaxiesCombinations))
    # print("Pairs: ", galaxiesCombinations)
    shortestPaths = []
    # for galaxyPair in galaxiesCombinations:
    #     shortestPaths.append(find_shortest_path(map, galaxyPair))
    #     # print("Found already ", len(shortestPaths), "of", len(galaxiesCombinations))
    # Create a pool of worker processes
    p1 = True
    # with Pool() as p:
    #     shortestPaths = p.starmap(
    #         find_shortest_path,
    #         [(map, pair, emptyColumns, emptyRows, p1) for pair in galaxiesCombinations],
    #     )

    with Pool() as p:
        shortestPaths = p.starmap(
            find_shortest_path_alt,
            [(pair, emptyColumns, emptyRows, p1) for pair in galaxiesCombinations],
        )

    # shortestPaths.append(
    #     find_shortest_path(map, ((3, 0), (7, 8)), emptyColumns, emptyRows)
    # )

    print(sum(shortestPaths))
    end_time_p1 = time.time()
    print("Time taken part 1: ", end_time_p1 - start_time)
    print("Time taken in ms part 1: ", (end_time_p1 - start_time) * 1000)

    shortestPaths = []
    p1 = False
    # with Pool() as p:
    #     shortestPaths = p.starmap(
    #         find_shortest_path,
    #         [(map, pair, emptyColumns, emptyRows, p1) for pair in galaxiesCombinations],
    #     )

    with Pool() as p:
        shortestPaths = p.starmap(
            find_shortest_path_alt,
            [(pair, emptyColumns, emptyRows, p1) for pair in galaxiesCombinations],
        )

    print(sum(shortestPaths))
    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total: ", end_time_p2 - start_time)
    print("Time taken total in ms: ", (end_time_p2 - start_time) * 1000)


# Alternative path finding
def find_shortest_path_alt(galaxyPair, emptyColumns, emptyRows, p1):
    if p1:
        factorEmpty = 2
    else:
        factorEmpty = 1000000

    start = galaxyPair[0]
    end = galaxyPair[1]

    # X Steps
    if start[0] <= end[0]:
        xSteps = end[0] - start[0]
        columns_between = set(range(start[0] + 1, end[0]))
        xSteps += len(columns_between.intersection(emptyColumns)) * (factorEmpty - 1)
    else:
        xSteps = start[0] - end[0]
        columns_between = set(range(end[0] + 1, start[0]))
        xSteps += len(columns_between.intersection(emptyColumns)) * (factorEmpty - 1)

    # Y Steps
    if start[1] <= end[1]:
        ySteps = end[1] - start[1]
        rows_between = set(range(start[1] + 1, end[1]))
        ySteps += len(rows_between.intersection(emptyRows)) * (factorEmpty - 1)
    else:
        ySteps = start[1] - end[1]
        rows_between = set(range(end[1] + 1, start[1]))
        ySteps += len(rows_between.intersection(emptyRows)) * (factorEmpty - 1)
    steps = xSteps + ySteps
    return steps


# Find shortest path between two galaxies
def find_shortest_path(map, galaxyPair, emptyColumns, emtpyRows, p1):
    # start_time = time.time()
    # print(galaxyPair)
    if p1:
        factorEmpty = 2
    else:
        factorEmpty = 1000000
    start = (galaxyPair[0], 0)

    end = (galaxyPair[1], None)
    stack = deque([start])
    maxY = max(y for x, y in map.keys())
    maxX = max(x for x, y in map.keys())
    visited = set()

    while stack:
        currentNode = stack.popleft()

        if currentNode[0] == end[0]:
            end = currentNode

            break
        if currentNode[0] in visited:
            continue

        visited.add(currentNode[0])
        map[currentNode[0]] = "X"

        # os.system("cls" if os.name == "nt" else "clear")
        # for i in range(maxY + 1):
        #     for j in range(maxX + 1):
        #         print(map[(j, i)][0], end="")
        #     print()
        # time.sleep(0.1)

        # above
        if currentNode[0][1] - 1 > -1 and not currentNode[0][1] - 1 < end[0][1]:
            if currentNode[0][1] - 1 in emtpyRows:
                stack.append(
                    (
                        (currentNode[0][0], currentNode[0][1] - 1),
                        currentNode[1] + factorEmpty,
                    )
                )
            else:
                stack.append(
                    ((currentNode[0][0], currentNode[0][1] - 1), currentNode[1] + 1)
                )
        # below
        if currentNode[0][1] + 1 < maxY + 1 and not currentNode[0][1] + 1 > end[0][1]:
            if currentNode[0][1] + 1 in emtpyRows:
                stack.append(
                    (
                        (currentNode[0][0], currentNode[0][1] + 1),
                        currentNode[1] + factorEmpty,
                    )
                )
            else:
                stack.append(
                    ((currentNode[0][0], currentNode[0][1] + 1), currentNode[1] + 1)
                )
        # left
        if currentNode[0][0] - 1 > -1 and not currentNode[0][0] - 1 < end[0][0]:
            if currentNode[0][0] - 1 in emptyColumns:
                stack.append(
                    (
                        (currentNode[0][0] - 1, currentNode[0][1]),
                        currentNode[1] + factorEmpty,
                    )
                )
            else:
                stack.append(
                    ((currentNode[0][0] - 1, currentNode[0][1]), currentNode[1] + 1)
                )
        # right
        if currentNode[0][0] + 1 < maxX + 1 and not currentNode[0][0] + 1 > end[0][0]:
            if currentNode[0][0] + 1 in emptyColumns:
                stack.append(
                    (
                        (currentNode[0][0] + 1, currentNode[0][1]),
                        currentNode[1] + factorEmpty,
                    )
                )
            else:
                stack.append(
                    ((currentNode[0][0] + 1, currentNode[0][1]), currentNode[1] + 1)
                )
    # print("Pair: ", galaxyPair, "Distance: ", end)
    # end_time = time.time()
    # print("Time taken: ", end_time - start_time)
    # print("Time taken in ms: ", (end_time - start_time) * 1000)
    return end[1]


def checkIfEmpty(map, column, maxX):
    # Find the maximum x-coordinate

    # Check if all characters in the column are the same
    chars = {map[(x, y)] for x, y in map.keys() if x == column}
    if len(chars) == 1:
        return True
    return False


if __name__ == "__main__":
    main()
