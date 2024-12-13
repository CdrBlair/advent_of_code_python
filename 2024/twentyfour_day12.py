import os
import time
from collections import deque


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/gardenmap.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    gardenMap = {}
    plantTypes = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            gardenMap[(x, y)] = char
            plantTypes.add(char)
    # add a outer layer in each direction
    # left
    for y in range(0, len(lines)):
        gardenMap[(-1, y)] = "."
    # right
    for y in range(0, len(lines)):

        gardenMap[(len(lines[0].strip()), y)] = "."
    # top
    for x in range(0, len(lines[0].strip())):
        gardenMap[(x, -1)] = "."
    # bottom
    for x in range(0, len(lines[0].strip())):
        gardenMap[(x, len(lines))] = "."
    # corners
    gardenMap[(-1, -1)] = "."
    gardenMap[(len(lines[0].strip()), -1)] = "."
    gardenMap[(-1, len(lines))] = "."
    gardenMap[(len(lines[0].strip()), len(lines))] = "."

    minX = -1
    minY = -1
    maxX = max([x for x, y in gardenMap.keys()])
    maxY = max([y for x, y in gardenMap.keys()])
    # print map
    # for y in range(minY, maxY + 1):
    #     for x in range(minX, maxX + 1):
    #         print(gardenMap[(x, y)], end="")
    #     print()
    # order plant type
    plantTypes = list(plantTypes)
    plantTypes.sort()
    regions = {}
    regionId = 0
    # print(plantTypes)
    for plantType in plantTypes:
        visited = set()
        for start in gardenMap:
            if gardenMap[start] == plantType and start not in visited:
                area, perimeter, visitedtemp, edges = findAreaAndPerimeter(
                    start, plantType, gardenMap
                )
                visited.update(visitedtemp)
                regions[regionId] = (plantType, area, perimeter, edges)
                regionId += 1

    # print(regions)
    price = 0
    for region in regions:
        plantType, area, perimeter, edges = regions[region]
        price += area * perimeter
        # print(edges)
    print(price)
    endtimep1 = time.time()
    print("Time part 1: ", endtimep1 - start_time)
    print("Time part 1 in ms: ", (endtimep1 - start_time) * 1000)

    for region in regions:
        plantType, area, perimeter, edges = regions[region]
        checkedges = set()
        sides = 0
        for edge in edges:
            if edge in checkedges:
                continue
            inside, outside = edge
            # determine edge directtion
            checkedges.add(edge)
            if inside[0] == outside[0]:
                # right
                i = 1
                while (inside[0] + i, inside[1]) in gardenMap and (
                    (inside[0] + i, inside[1]),
                    (outside[0] + i, outside[1]),
                ) in edges:
                    checkedges.add(
                        ((inside[0] + i, inside[1]), (outside[0] + i, outside[1]))
                    )
                    i += 1
                # left
                i = 1
                while (inside[0] - i, inside[1]) in gardenMap and (
                    (inside[0] - i, inside[1]),
                    (outside[0] - i, outside[1]),
                ) in edges:
                    checkedges.add(
                        ((inside[0] - i, inside[1]), (outside[0] - i, outside[1]))
                    )
                    i += 1
            else:
                # down
                i = 1
                while (inside[0], inside[1] + i) in gardenMap and (
                    (inside[0], inside[1] + i),
                    (outside[0], outside[1] + i),
                ) in edges:
                    checkedges.add(
                        ((inside[0], inside[1] + i), (outside[0], outside[1] + i))
                    )
                    i += 1
                # up
                i = 1
                while (inside[0], inside[1] - i) in gardenMap and (
                    (inside[0], inside[1] - i),
                    (outside[0], outside[1] - i),
                ) in edges:
                    checkedges.add(
                        ((inside[0], inside[1] - i), (outside[0], outside[1] - i))
                    )
                    i += 1

            sides += 1
        regions[region] = (plantType, area, perimeter, sides)

    # print(regions)
    newPrice = 0
    for region in regions:
        plantType, area, perimeter, sides = regions[region]
        newPrice += area * sides
    print(newPrice)
    endtimep2 = time.time()
    print("Time part 2: ", endtimep2 - endtimep1)
    print("Time part 2 in ms: ", (endtimep2 - endtimep1) * 1000)


def findAreaAndPerimeter(start, plantType, map):
    area = 0
    perimeter = 0
    stack = deque([start])
    visited = set()
    edges = set()
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        area += 1
        neighbors = getNeighbors(current)
        for neighbor in neighbors:
            if neighbor in visited or neighbor not in map:
                continue
            if map[neighbor] == plantType:
                stack.append(neighbor)
            else:
                edges.add((current, neighbor))
                perimeter += 1
    # print(len(edges))
    return area, perimeter, visited, edges


def getNeighbors(current):
    return [
        (current[0] + 1, current[1]),
        (current[0] - 1, current[1]),
        (current[0], current[1] + 1),
        (current[0], current[1] - 1),
    ]


if __name__ == "__main__":
    main()
