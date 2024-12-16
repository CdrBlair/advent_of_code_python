import os
import sys
import time
from collections import deque


def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/reindeer_maze.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    maze = {}
    startPos = None
    endPos = None
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            maze[(x, y)] = char
            if char == "S":
                startPos = (x, y)
            if char == "E":
                endPos = (x, y)

    startDire = ">"

    maxX = max(x[0] for x in maze.keys())
    maxY = max(x[1] for x in maze.keys())
    # print(maze)
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(maze[(x, y)], end="")
    #     print()

    startingState = (startPos, startDire, 0, 0, frozenset())

    queue = deque([startingState])
    possibleways = set()
    visitedState = {}

    while queue:
        curPos, curDir, rotations, steps, path = queue.popleft()

        if curPos == endPos:
            nextPath = set(path)
            nextPath.add(curPos)
            nextPath = frozenset(nextPath)
            possibleways.add((rotations, steps, nextPath))
            continue
        if (curPos, curDir) in visitedState and visitedState[(curPos, curDir)] < (
            rotations * 1000 + steps
        ):
            continue
        visitedState[(curPos, curDir)] = rotations * 1000 + steps
        if curDir == "^":
            nextPos = (curPos[0], curPos[1] - 1)
            if maze.get(nextPos) in [".", "E"]:
                nextDir = "^"
                nextRotations = rotations
                nextSteps = steps + 1
                nextPath = set(path)
                nextPath.add(curPos)
                nextPath = frozenset(nextPath)
                queue.append((nextPos, nextDir, nextRotations, nextSteps, nextPath))
            # Turn left
            nextDir = "<"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
            # Turn right
            nextDir = ">"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
        elif curDir == "v":
            nextPos = (curPos[0], curPos[1] + 1)
            if maze.get(nextPos) in [".", "E"]:
                nextDir = "v"
                nextRotations = rotations
                nextSteps = steps + 1
                nextPath = set(path)
                nextPath.add(curPos)
                nextPath = frozenset(nextPath)
                queue.append((nextPos, nextDir, nextRotations, nextSteps, nextPath))
            # Turn left
            nextDir = ">"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
            # Turn right
            nextDir = "<"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
        elif curDir == "<":
            nextPos = (curPos[0] - 1, curPos[1])
            if maze.get(nextPos) in [".", "E"]:
                nextDir = "<"
                nextRotations = rotations
                nextSteps = steps + 1
                nextPath = set(path)
                nextPath.add(curPos)
                nextPath = frozenset(nextPath)
                queue.append((nextPos, nextDir, nextRotations, nextSteps, nextPath))
            # Turn left
            nextDir = "v"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
            # Turn right
            nextDir = "^"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
        elif curDir == ">":
            nextPos = (curPos[0] + 1, curPos[1])
            if maze.get(nextPos) in [".", "E"]:
                nextDir = ">"
                nextRotations = rotations
                nextSteps = steps + 1
                nextPath = set(path)
                nextPath.add(curPos)
                nextPath = frozenset(nextPath)
                queue.append((nextPos, nextDir, nextRotations, nextSteps, nextPath))
            # Turn left
            nextDir = "^"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))
            # Turn right
            nextDir = "v"
            nextRotations = rotations + 1
            queue.append((curPos, nextDir, nextRotations, steps, path))

    possibleways = list(possibleways)
    # sort by rotations then by steps
    possibleways.sort(key=lambda x: (x[0], x[1]))

    price = possibleways[0][0] * 1000 + possibleways[0][1]
    # winningway = possibleways[0][2]
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         if (x, y) in winningway and (x, y) != startPos and (x, y) != endPos:
    #             print("O", end="")
    #         else:
    #             print(maze[(x, y)], end="")
    #     print()

    print(price)
    endtimeP1 = time.time()
    print("P1 took: ", endtimeP1 - starttime)
    print("P1 took in ms:", (endtimeP1 - starttime) * 1000)

    allTiles = set()
    for way in possibleways:
        if way[0] * 1000 + way[1] == price:
            allTiles = allTiles.union(way[2])
    # combine tiles from all best ways
    print(len(allTiles))
    endtimeP2 = time.time()
    print("Part 2 took: ", endtimeP2 - endtimeP1)
    print("Part 2 took in ms:", (endtimeP2 - endtimeP2) * 1000)


if __name__ == "__main__":
    main()
