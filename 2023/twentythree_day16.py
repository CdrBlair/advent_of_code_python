import os
import time
from collections import deque
from turtle import position


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/floor_is_lava.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    machineMap = {}
    energizedStata = {}
    heigth = len(lines)
    width = len(lines[0].strip())

    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            machineMap[(j, i)] = char
            energizedStata[(j, i)] = 0

    start = ((0, 0), "r")
    sumEnergizedPositions = calculateEnergizedState(
        start, machineMap, energizedStata, width, heigth
    )
    print("Sum of energized positions: ", sumEnergizedPositions)
    endTimeP1 = time.time()
    print("Part one time: ", endTimeP1 - start_time)
    print("Part one time in ms: ", (endTimeP1 - start_time) * 1000)
    start_time_p2 = time.time()
    # Construct all possilbe starting positions
    startingPositions = []
    for i in range(heigth):
        startingPositions.append(((0, i), "r"))
        startingPositions.append(((width - 1, i), "l"))
    for i in range(width):
        startingPositions.append(((i, 0), "d"))
        startingPositions.append(((i, heigth - 1), "u"))

    allEnergizedStates = []
    for startingPosition in startingPositions:
        allEnergizedStates.append(
            calculateEnergizedState(
                startingPosition, machineMap, energizedStata, width, heigth
            )
        )
    print("Max energized positions: ", max(allEnergizedStates))
    endTimeP2 = time.time()
    print("Part two time: ", endTimeP2 - start_time_p2)
    print("Part two time in ms: ", (endTimeP2 - start_time_p2) * 1000)


def calculateEnergizedState(start, map, energizedState, width, heigth):
    energizedStata = energizedState.copy()
    machineMap = map.copy()
    # directions = ["u", "r", "d", "l"]

    stack = deque([start])
    visited = set()

    while stack:
        # get current position
        current = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        # energize currect position
        energizedStata[current[0]] = 1

        # get direction
        direction = current[1]

        # check position kind
        positionKind = machineMap[current[0]]

        if positionKind == ".":
            # move forward
            if direction == "u" and current[0][1] - 1 > -1:
                stack.append(((current[0][0], current[0][1] - 1), "u"))
            elif direction == "r" and current[0][0] + 1 < width:
                stack.append(((current[0][0] + 1, current[0][1]), "r"))
            elif direction == "d" and current[0][1] + 1 < heigth:
                stack.append(((current[0][0], current[0][1] + 1), "d"))
            elif direction == "l" and current[0][0] - 1 > -1:
                stack.append(((current[0][0] - 1, current[0][1]), "l"))
        elif positionKind == "/":
            # turning
            if direction == "u" and current[0][0] + 1 < width:
                stack.append(((current[0][0] + 1, current[0][1]), "r"))
            elif direction == "r" and current[0][1] - 1 > -1:
                stack.append(((current[0][0], current[0][1] - 1), "u"))
            elif direction == "d" and current[0][0] - 1 > -1:
                stack.append(((current[0][0] - 1, current[0][1]), "l"))
            elif direction == "l" and current[0][1] + 1 < heigth:
                stack.append(((current[0][0], current[0][1] + 1), "d"))
        elif positionKind == "\\":
            # turning
            if direction == "u" and current[0][0] - 1 > -1:
                stack.append(((current[0][0] - 1, current[0][1]), "l"))
            elif direction == "r" and current[0][1] + 1 < heigth:
                stack.append(((current[0][0], current[0][1] + 1), "d"))
            elif direction == "d" and current[0][0] + 1 < width:
                stack.append(((current[0][0] + 1, current[0][1]), "r"))
            elif direction == "l" and current[0][1] - 1 > -1:
                stack.append(((current[0][0], current[0][1] - 1), "u"))
        elif positionKind == "|":
            # splitting
            if direction == "u" and current[0][1] - 1 > -1:
                stack.append(((current[0][0], current[0][1] - 1), "u"))
            elif direction == "d" and current[0][1] + 1 < heigth:
                stack.append(((current[0][0], current[0][1] + 1), "d"))
            else:
                if current[0][1] - 1 > -1:
                    stack.append(((current[0][0], current[0][1] - 1), "u"))
                if current[0][1] + 1 < heigth:
                    stack.append(((current[0][0], current[0][1] + 1), "d"))
        elif positionKind == "-":
            # splitting
            if direction == "l" and current[0][0] - 1 > -1:
                stack.append(((current[0][0] - 1, current[0][1]), "l"))
            elif direction == "r" and current[0][0] + 1 < width:
                stack.append(((current[0][0] + 1, current[0][1]), "r"))
            else:
                if current[0][0] - 1 > -1:
                    stack.append(((current[0][0] - 1, current[0][1]), "l"))
                if current[0][0] + 1 < width:
                    stack.append(((current[0][0] + 1, current[0][1]), "r"))

        # for i in range(heigth):
        #     for j in range(width):
        #         if machineMap[(j, i)] == ".":
        #             print("#" if energizedStata[(j, i)] == 1 else ".", end="")
        #         else:
        #             print(machineMap[(j, i)], end="")
        #     print()
        # print()

    return sum(energizedStata.values())


if __name__ == "__main__":
    main()
