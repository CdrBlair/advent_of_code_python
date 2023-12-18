import os
import time
from heapq import heappop, heappush
from math import dist
from turtle import distance


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/heatMap.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    heatMap = {}
    heigth = len(lines)
    width = len(lines[0].strip())

    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            heatMap[(j, i)] = int(char)

    # for i in range(heigth):
    #     for j in range(width):
    #         print(heatMap[(j, i)], end="")
    #     print()
    # print()
    start1, start2 = (0, 0, 0, ">"), (0, 0, 0, "v")
    end = (width - 1, heigth - 1)

    visited = set()
    stack = [(0, start1), (0, start2)]
    distances = {start1: 0, start2: 0}
    while stack:
        _, position = heappop(stack)

        if position in visited:
            continue
        visited.add(position)
        if (position[0], position[1]) == end:
            end = position
            break

        neighbours = getNeighbours(position, heatMap, False)

        for neighbour, cost in neighbours:
            if neighbour in visited:
                continue
            alternative = distances[position] + cost

            if neighbour not in distances or alternative < distances[neighbour]:
                distances[neighbour] = alternative
                heappush(stack, (alternative, neighbour))

    # Find path

    print("Part 1: ", distances[end])
    endTimePart1 = time.time()
    print("time part 1: ", endTimePart1 - start_time)
    print("time p1 in ms: ", (endTimePart1 - start_time) * 1000)

    # Part 2
    start1, start2 = (0, 0, 0, ">"), (0, 0, 0, "v")
    end = (width - 1, heigth - 1)

    visited = set()
    stack = [(0, start1), (0, start2)]
    distances = {start1: 0, start2: 0}
    while stack:
        _, position = heappop(stack)

        if position in visited:
            continue
        visited.add(position)
        if (position[0], position[1]) == end and position[2] > 3:
            end = position
            break

        neighbours = getNeighbours(position, heatMap, True)

        for neighbour, cost in neighbours:
            if neighbour in visited:
                continue
            alternative = distances[position] + cost

            if neighbour not in distances or alternative < distances[neighbour]:
                distances[neighbour] = alternative
                heappush(stack, (alternative, neighbour))
    print("Part 2: ", distances[end])
    endTimePart2 = time.time()
    print("time part 2: ", endTimePart2 - endTimePart1)
    print("time p2 in ms: ", (endTimePart2 - endTimePart1) * 1000)
    print("total time: ", endTimePart2 - start_time)


def getNeighbours(position, heatMap, part2):
    neighbours = []
    x, y, steps, dir = position
    if dir == ">":
        dx, dy = 1, 0
    elif dir == "<":
        dx, dy = -1, 0
    elif dir == "^":
        dx, dy = 0, -1
    elif dir == "v":
        dx, dy = 0, 1
    # check current direction
    if steps < (10 if part2 else 3) and (x + dx, y + dy) in heatMap:
        neighbours.append(((x + dx, y + dy, steps + 1, dir), heatMap[(x + dx, y + dy)]))

    for newdx, newdy in (-dy, dx), (dy, -dx):
        newDir = ""
        if (newdx, newdy) == (0, 1):
            newDir = "v"
        elif (newdx, newdy) == (0, -1):
            newDir = "^"
        elif (newdx, newdy) == (1, 0):
            newDir = ">"
        elif (newdx, newdy) == (-1, 0):
            newDir = "<"
        if (x + newdx, y + newdy) in heatMap and (not part2 or steps > 3):
            neighbours.append(
                (
                    (x + newdx, y + newdy, 1, newDir),
                    heatMap[(x + newdx, y + newdy)],
                )
            )

    # print("x: ", x, "y: ", y, "steps: ", steps, "dir: ", dir)
    # print("neighbours: ", neighbours)
    # print()
    return neighbours


if __name__ == "__main__":
    main()
