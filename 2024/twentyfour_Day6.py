import os
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/1518.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    guardMap = {}
    startPos = None

    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            if char == "^" or char == "v" or char == "<" or char == ">":
                startPos = (j, i)
                startDir = char
            guardMap[(j, i)] = char

    maxX = max([x[0] for x in guardMap.keys()])
    maxY = max([x[1] for x in guardMap.keys()])
    # Print Map
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(guardMap[(x, y)], end="")
    #     print()
    # print()

    pos = startPos
    visited = set()
    lastPost = None
    while pos in guardMap:
        visited.add(pos)
        lastPost = pos
        pos = move(guardMap, pos)

    #    for visit in visited:
    #       guardMap[visit] = "X"
    # Print Map
    guardMap[startPos] = startDir
    guardMap[lastPost] = "."
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(guardMap[(x, y)], end="")
    #     print()
    # print()

    print(len(visited))
    endtime = time.time()
    print("Time taken: ", endtime - start_time)
    print("Time taken in ms: ", (endtime - start_time) * 1000)

    curObs = None
    loopObs = 0

    for key in guardMap:

        # print("startPos", startPos, "key", key, "mapstartPos", guardMap[startPos])
        if not guardMap[key] == "." or key == startPos:
            # print(key)
            continue
        curObs = key
        guardMap[curObs] = "#"

        pos = startPos
        # print("StartPos", pos, guardMap[pos])
        visitedDir = set()
        while pos in guardMap:
            lastPost = pos
            visitedDir.add((pos, guardMap[pos]))
            pos = move(guardMap, pos)
            # if curObs == (3, 6):
            # print("Post", pos, guardMap[pos])
            if pos in guardMap and (pos, guardMap[pos]) in visitedDir:
                # print("loop")
                lastPost = pos
                loopObs += 1
                break

        guardMap[startPos] = startDir
        if not lastPost == startPos:
            guardMap[lastPost] = "."
        guardMap[curObs] = "."
    print(loopObs)

    endtimeP2 = time.time()
    print("Time taken: ", endtimeP2 - endtime)
    print("Time taken in ms: ", (endtimeP2 - endtime) * 1000)


def move(map, pos):
    # print("map Pos", pos, map[pos])
    direction = None
    turn = None
    if map[pos] == "^":
        direction = (0, -1)
        turn = ">"
    elif map[pos] == "v":
        direction = (0, 1)
        turn = "<"
    elif map[pos] == "<":
        direction = (-1, 0)
        turn = "^"
    elif map[pos] == ">":
        direction = (1, 0)
        turn = "v"

    newPos = (pos[0] + direction[0], pos[1] + direction[1])
    if newPos not in map:
        return newPos
    if map[newPos] == "#":
        map[pos] = turn
        return pos
    else:
        map[newPos] = map[pos]
        map[pos] = "."
        return newPos


if __name__ == "__main__":
    main()
