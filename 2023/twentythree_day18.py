import os
import time


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/digging_plan.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    digInstruction = []
    for line in lines:
        line = line.strip()
        parts = line.split(" ")
        digInstruction.append(
            (parts[0], int(parts[1]), parts[2].replace("(", "").replace(")", ""))
        )

    lagoon = {}
    lagoon[(0, 0)] = ("#", None)

    current = (0, 0)
    for instruction in digInstruction:
        direction = instruction[0]
        steps = instruction[1]
        color = instruction[2]

        if direction == "R":
            for i in range(steps):
                current = (current[0] + 1, current[1])
                lagoon[current] = ("#", color)
        elif direction == "L":
            for i in range(steps):
                current = (current[0] - 1, current[1])
                lagoon[current] = ("#", color)
        elif direction == "U":
            for i in range(steps):
                current = (current[0], current[1] - 1)
                lagoon[current] = ("#", color)
        elif direction == "D":
            for i in range(steps):
                current = (current[0], current[1] + 1)
                lagoon[current] = ("#", color)

    # Find width and height
    maxX = max(lagoon.keys(), key=lambda x: x[0])[0]
    maxY = max(lagoon.keys(), key=lambda x: x[1])[1]
    minX = min(lagoon.keys(), key=lambda x: x[0])[0]
    minY = min(lagoon.keys(), key=lambda x: x[1])[1]

    # fill all empty spaces with .
    for i in range(minY, maxY + 1):
        for j in range(minX, maxX + 1):
            if (j, i) not in lagoon:
                lagoon[(j, i)] = (".", None)

    # Print lagoon
    # for i in range(minY, maxY + 1):
    #     for j in range(minX, maxX + 1):
    #         print(lagoon[(j, i)][0], end="")

    #     print()
    # print()

    # extend map by an outer layer
    maxX += 1
    maxY += 1
    minX -= 1
    minY -= 1

    # Fill outer layer with .
    for i in range(minY, maxY + 1):
        lagoon[(minX, i)] = (".", None)
        lagoon[(maxX, i)] = (".", None)
    for j in range(minX, maxX + 1):
        lagoon[(j, minY)] = (".", None)
        lagoon[(j, maxY)] = (".", None)

    # print lagoon
    # for i in range(minY, maxY + 1):
    #     for j in range(minX, maxX + 1):
    #         print(lagoon[(j, i)][0], end="")

    #     print()
    # print()

    outer = flood_fill(lagoon, maxX, maxY, minY, minX)
    border = set([key for key, value in lagoon.items() if value[0] == "#"])

    # set all inner places to #, none

    for coord in lagoon:
        if coord not in outer and coord not in border:
            lagoon[coord] = ("#", None)

    # print lagoon
    # for i in range(minY, maxY + 1):
    #     for j in range(minX, maxX + 1):
    #         print(lagoon[(j, i)][0], end="")

    #     print()
    # print()

    # Find all #
    numberOfHoles = len([key for key, value in lagoon.items() if value[0] == "#"])
    print("Part 1: ", numberOfHoles)
    endTimePart1 = time.time()
    print("time part 1: ", endTimePart1 - start_time)
    print("time p1 in ms: ", (endTimePart1 - start_time) * 1000)

    # Part 2
    newDigInstructions = []
    for inst in digInstruction:
        # Remove last char from color
        codedDir = int(inst[2][-1])
        if codedDir == 0:
            codedDir = "R"
        elif codedDir == 1:
            codedDir = "D"
        elif codedDir == 2:
            codedDir = "L"
        elif codedDir == 3:
            codedDir = "U"
        hexSteps = inst[2][1:-1]
        newSteps = int(hexSteps, 16)
        newDigInstructions.append((codedDir, newSteps))

    cornerCoords = []
    cornerCoords.append((0, 0))
    current = (0, 0)
    totalSteps = 0
    for inst in newDigInstructions:
        direction = inst[0]
        steps = inst[1]
        totalSteps += steps

        if direction == "R":
            cornerCoords.append((current[0] + steps, current[1]))
        elif direction == "L":
            cornerCoords.append((current[0] - steps, current[1]))
        elif direction == "U":
            cornerCoords.append((current[0], current[1] - steps))
        elif direction == "D":
            cornerCoords.append((current[0], current[1] + steps))
        current = cornerCoords[-1]

    area = 0
    for i in range(len(cornerCoords) - 1):
        xi = cornerCoords[i][0]
        yi = cornerCoords[i][1]
        if i + 1 >= len(cornerCoords):
            xi1 = cornerCoords[0][0]
            yi1 = cornerCoords[0][1]
        else:
            xi1 = cornerCoords[i + 1][0]
            yi1 = cornerCoords[i + 1][1]
        area += (yi + yi1) * (xi - xi1)
    print("totalSteps: ", totalSteps)

    area = abs(area) * 0.5
    print("area: ", area)
    # inner = area + 1 - totalSteps // 2

    # Sum = I + b -> area +1 - steps // 2 + steps = area + 1 + steps // 2

    wholeArea = area + 1 + totalSteps // 2
    print("Part 2: ", int(wholeArea))
    endTimePart2 = time.time()
    print("time part 2: ", endTimePart2 - endTimePart1)
    print("time p2 in ms: ", (endTimePart2 - endTimePart1) * 1000)
    print("total time: ", endTimePart2 - start_time)


# Flood Fill
def flood_fill(map, maxX, maxY, minY, minX):
    stack = [(minX, minY)]
    visited = set()
    outer = set()
    # Add extra rows and columsn to outside of map
    while stack:
        current = stack.pop(0)
        if (
            current[0] > maxX
            or current[0] < minX
            or current[1] > maxY
            or current[1] < minY
            or current in visited
            or map[current][0] == "#"
        ):
            continue
        visited.add(current)
        outer.add(current)

        stack.append((current[0] + 1, current[1]))
        stack.append((current[0] - 1, current[1]))
        stack.append((current[0], current[1] + 1))
        stack.append((current[0], current[1] - 1))

    return outer


if __name__ == "__main__":
    main()
