import os
import time
from collections import deque


def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/memory.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    fallingBytes = [
        (int(x), int(y)) for x, y in [line.strip().split(",") for line in lines]
    ]

    # print(fallingBytes)

    memoryMap = {}

    maxX = 70  # 70
    maxY = 70  # 70
    # print(maxX, maxY)
    start = (0, 0)
    end = (maxX, maxY)

    for y in range(maxY + 1):
        for x in range(maxX + 1):
            memoryMap[(x, y)] = "."

    numberOfFallingBytes = 1024  # 1024

    for i in range(numberOfFallingBytes):
        memoryMap[fallingBytes[i]] = "#"

    # # print map
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(memoryMap[(x, y)], end="")
    #     print()

    finalPath = findPath(start, end, memoryMap)

    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         if (x, y) in finalPath:
    #             print("O", end="")
    #         else:
    #             print(memoryMap[(x, y)], end="")
    #     print()

    print(len(finalPath))

    endtimeP1 = time.time()
    print("Part 1 took:", endtimeP1 - starttime)
    print("Part 1 took in ms:", (endtimeP1 - starttime) * 1000)

    # Doing it the other way around. Searching when there is a free path.
    furtherFallingFrom = 1024  # 1024
    for i in range(furtherFallingFrom, len(fallingBytes)):
        memoryMap[fallingBytes[i]] = "#"

    finalPath = findPath(start, end, memoryMap)
    removeFrom = len(fallingBytes) - 1
    while not finalPath:
        removeFrom -= 1
        memoryMap[fallingBytes[removeFrom]] = "."
        finalPath = findPath(start, end, memoryMap)

    print("# byte:", removeFrom, " Byte:", fallingBytes[removeFrom])
    endtimeP2 = time.time()
    print("Part 2 took:", endtimeP2 - endtimeP1)
    print("Part 2 took in ms:", (endtimeP2 - endtimeP1) * 1000)


def findPath(start, end, memoryMap):
    startState = (start, 0, [])
    stack = deque([startState])
    visited = {}
    finalPath = []
    while stack:
        curPos, steps, path = stack.popleft()
        if curPos == end:
            # print("Found the end")
            # print(steps)
            # print(path)
            finalPath = path
            break
        if curPos in visited:
            continue
        visited[curPos] = steps
        x, y = curPos
        if (x, y + 1) in memoryMap and memoryMap[(x, y + 1)] == ".":
            stack.append(((x, y + 1), steps + 1, path + [curPos]))
        if (x, y - 1) in memoryMap and memoryMap[(x, y - 1)] == ".":
            stack.append(((x, y - 1), steps + 1, path + [curPos]))
        if (x + 1, y) in memoryMap and memoryMap[(x + 1, y)] == ".":
            stack.append(((x + 1, y), steps + 1, path + [curPos]))
        if (x - 1, y) in memoryMap and memoryMap[(x - 1, y)] == ".":
            stack.append(((x - 1, y), steps + 1, path + [curPos]))
    return finalPath


if __name__ == "__main__":
    main()
