import os
import time
from gettext import find


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/pipes.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    map = {}

    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            map[(j, i)] = (char, None, None)
            if char == "S":
                start = (j, i)

    # for i in range(max(map.keys())[0] + 1):
    #     for j in range(max(map.keys())[1] + 1):
    #         print(map[(j, i)][0], end="")
    #     print()

    # set connecting pipes to start
    connectingPipes = find_conecting_pipes(map, start)
    map[start] = (
        "S",
        connectingPipes[0],
        connectingPipes[1],
    )

    reachedStart = False
    currentNodeCoord = map[start][2]
    beforeNode = start
    steps = 1
    allLoopTiles = []
    allLoopTiles.append(
        (
            start,
            (map[start][1][0] - start[0], map[start][1][1] - start[1]),
            (map[start][2][0] - start[0], map[start][2][1] - start[1]),
        )
    )
    while not reachedStart:
        nextPipes = find_next_pipes(map, currentNodeCoord)
        currentNode = map[currentNodeCoord]
        map[currentNodeCoord] = (
            currentNode[0],
            nextPipes[0],
            nextPipes[1],
            steps,
        )
        allLoopTiles.append(
            (
                currentNodeCoord,
                (
                    nextPipes[0][0] - currentNodeCoord[0],
                    nextPipes[0][1] - currentNodeCoord[1],
                ),
                (
                    nextPipes[1][0] - currentNodeCoord[0],
                    nextPipes[1][1] - currentNodeCoord[1],
                ),
            )
        )

        if not beforeNode == start and start in nextPipes:
            steps += 1
            reachedStart = True

            break

        for node in nextPipes:
            if not node == beforeNode:
                beforeNode = currentNodeCoord
                currentNodeCoord = node
                break

        steps += 1

    steps_to_farthest_node = steps // 2
    print("Steps to farthest node: ", steps_to_farthest_node)

    end_time_p1 = time.time()
    print("Time taken part 1: ", end_time_p1 - start_time)
    print("Time taken in ms part 1: ", (end_time_p1 - start_time) * 1000)

    originalKeys = map.keys()
    newMaxX = max(originalKeys)[0] * 2
    newMaxY = max(originalKeys)[1] * 2
    extended_map = {
        (x, y): ("I", None, None)
        for x in range(newMaxX + 1)
        for y in range(newMaxY + 1)
    }

    extended_map.update({((x * 2, y * 2)): value for ((x, y), value) in map.items()})

    for addNode in allLoopTiles:
        # first connected pipe
        extended_map[
            (addNode[0][0] * 2 + addNode[1][0], addNode[0][1] * 2 + addNode[1][1])
        ] = (
            "X",
            None,
            None,
        )
        # second connected pipe
        extended_map[
            (addNode[0][0] * 2 + addNode[2][0], addNode[0][1] * 2 + addNode[2][1])
        ] = (
            "X",
            None,
            None,
        )

    visited = set()
    allLoopTileCoords = [(tile[0][0] * 2, tile[0][1] * 2) for tile in allLoopTiles]

    allLoopTileCoords = set(allLoopTileCoords)
    flood_fill(extended_map, (0, 0), visited, newMaxX, newMaxY, allLoopTileCoords)

    final_map = {
        ((x // 2, y // 2)): value
        for ((x, y), value) in extended_map.items()
        if x % 2 == 0 and y % 2 == 0
    }

    # Replace Loop Tiles with X
    for tile in allLoopTiles:
        final_map[tile[0]] = ("X", None, None)

    # Print final map
    # for i in range(max(final_map.keys())[0] + 1):
    #     for j in range(max(final_map.keys())[1] + 1):
    #         print(final_map[(j, i)][0], end="")
    #     print()

    inside = 0
    for tile in final_map:
        if not final_map[tile][0] in ["O", "X"]:
            inside += 1

    print("Inside: ", inside)
    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total in ms: ", (end_time_p2 - start_time) * 1000)


# Flood Fill
def flood_fill(map, start, visited, maxX, maxY, loopTiles):
    stack = [start]
    while stack:
        current = stack.pop()
        if (
            current[0] > maxX
            or current[0] < 0
            or current[1] > maxY
            or current[1] < 0
            or current in visited
            or current in loopTiles
            or map[current][0] == "X"
        ):
            continue
        visited.add(current)
        map[current] = ("O", None, None)
        stack.append((current[0] + 1, current[1]))
        stack.append((current[0] - 1, current[1]))
        stack.append((current[0], current[1] + 1))
        stack.append((current[0], current[1] - 1))


# Find next pipe
def find_next_pipes(map, node):
    direction = map[node][0]
    if direction == "|":
        return ((node[0], node[1] - 1), (node[0], node[1] + 1))
    if direction == "-":
        return ((node[0] - 1, node[1]), (node[0] + 1, node[1]))
    if direction == "L":
        return ((node[0] + 1, node[1]), (node[0], node[1] - 1))
    if direction == "J":
        return ((node[0] - 1, node[1]), (node[0], node[1] - 1))
    if direction == "7":
        return ((node[0] - 1, node[1]), (node[0], node[1] + 1))
    if direction == "F":
        return ((node[0] + 1, node[1]), (node[0], node[1] + 1))


# Find conecting pipes
def find_conecting_pipes(map, start):
    allconnectors = ["|", "-", "L", "J", "7", "F"]
    connectorsDown = ["|", "F", "7"]
    connectorsUp = ["|", "J", "L"]
    connectorsRight = ["-", "F", "L"]
    connectorsLeft = ["-", "J", "7"]

    # Find max x and y
    maxX = max(map.keys())[0]
    maxY = max(map.keys())[1]

    connecting_pipes = []
    # above
    if start[1] - 1 > -1 and map[(start[0], start[1] - 1)][0] in connectorsDown:
        connecting_pipes.append(start[0], start[1] - 1)
    # below
    if start[1] + 1 < maxY + 1 and map[(start[0], start[1] + 1)][0] in connectorsUp:
        connecting_pipes.append((start[0], start[1] + 1))
    # left
    if start[0] - 1 > -1 and map[(start[0] - 1, start[1])][0] in connectorsRight:
        connecting_pipes.append((start[0] - 1, start[1]))
    # right
    if start[0] + 1 < maxX and map[(start[0] + 1, start[1])][0] in connectorsLeft:
        connecting_pipes.append((start[0] + 1, start[1]))
    return connecting_pipes


if __name__ == "__main__":
    main()
