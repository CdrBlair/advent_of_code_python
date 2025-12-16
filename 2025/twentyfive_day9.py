# Main method
import os
import time

from shapely import Point, Polygon


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day9.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        redTiles = []
        for line in lines:
            line = line.strip()
            parts = line.split(",")
            redTiles.append((int(parts[0]), int(parts[1])))

    # print("Red tiles: ", redTiles)

    biggestArea = 0
    rectangles = []
    for i in range(len(redTiles)):
        for j in range(i + 1, len(redTiles)):
            corner1 = redTiles[i]
            corner2 = redTiles[j]
            area = calcRectangleSize(corner1, corner2)
            # print("Area between ", corner1, " and ", corner2, " is ", area)
            rectangles.append((area, corner1, corner2))
            if area > biggestArea:
                biggestArea = area
    print("Biggest area: ", biggestArea)
    endP1 = time.time()
    print("Part 1 took ", endP1 - start_time, " seconds")
    print("Part 1 took in ms: ", (endP1 - start_time) * 1000)

    # build loop
    greenTiles = []
    for i in range(len(redTiles)):
        tile1 = redTiles[i]
        tile2 = redTiles[(i + 1) % len(redTiles)]
        greenTiles.extend(findConnectingTiles(tile1, tile2))

    # print("Connecting tiles: ", greenTiles)
    # print a map of the loop
    maxX = max([tile[0] for tile in redTiles + greenTiles]) + 1
    maxY = max([tile[1] for tile in redTiles + greenTiles]) + 1
    # for y in range(maxY + 1):
    #     row = ""
    #     for x in range(maxX + 1):
    #         if (x, y) in redTiles:
    #             row += "#"
    #         elif (x, y) in greenTiles:
    #             row += "X"
    #         else:
    #             row += "."
    #     print(row)

    # fill in the area inside the loop

    # for y in range(maxY + 1):
    #     row = ""
    #     for x in range(maxX + 1):
    #         if (x, y) in redTiles:
    #             row += "#"
    #         elif (x, y) in greenTiles:
    #             row += "X"
    #         elif (x, y) in filledTiles:
    #             row += "X"
    #         else:
    #             row += "."
    #     print(row)

    # sort rectangles by area decreasing
    rectangles.sort(key=lambda x: x[0], reverse=True)

    print(len(rectangles), " rectangles to check for filling")
    p = Polygon(redTiles)
    for rect in rectangles:
        # print("Checking rectangle: ", rect)
        area, corner1, corner2 = rect

        minX = min(corner1[0], corner2[0])
        maxX = max(corner1[0], corner2[0])
        minY = min(corner1[1], corner2[1])
        maxY = max(corner1[1], corner2[1])

        # Clockwise from bottom-left
        allTiles = [
            (minX, minY),  # bottom-left
            (maxX, minY),  # bottom-right
            (maxX, maxY),  # top-right
            (minX, maxY),  # top-left
        ]

        # print("All tiles of rectangle: ", allTiles)
        rectPoly = Polygon(allTiles)
        # print(allTiles)
        # print(rectPoly)
        # print("Rectangle polygon: ", rectPoly.area)
        if p.contains(rectPoly):
            print("Found biggest fillable rectangle: ", rect)
            break

    end_time = time.time()
    print("Part 2 took ", end_time - endP1, " seconds")
    print("Part 2 took in ms: ", (end_time - endP1) * 1000)


def getOutlineTiles(corner1, corner2):
    tiles = set()
    minX = min(corner1[0], corner2[0])
    maxX = max(corner1[0], corner2[0])
    minY = min(corner1[1], corner2[1])
    maxY = max(corner1[1], corner2[1])
    for x in range(minX, maxX + 1):
        tiles.add((x, minY))
        tiles.add((x, maxY))
    for y in range(minY, maxY + 1):
        tiles.add((minX, y))
        tiles.add((maxX, y))
    return tiles


def findConnectingTiles(tile1, tile2):
    connectingTiles = []
    if tile1[0] == tile2[0]:
        # same x
        x = tile1[0]
        for y in range(min(tile1[1], tile2[1]) + 1, max(tile1[1], tile2[1])):
            connectingTiles.append((x, y))
    elif tile1[1] == tile2[1]:
        # same column
        y = tile1[1]
        for x in range(min(tile1[0], tile2[0]) + 1, max(tile1[0], tile2[0])):
            connectingTiles.append((x, y))
    return connectingTiles


def calcRectangleSize(corner1, corner2):
    length = abs(corner1[0] - corner2[0]) + 1
    width = abs(corner1[1] - corner2[1]) + 1
    return length * width


if __name__ == "__main__":
    main()
