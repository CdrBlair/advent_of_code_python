import os
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2015/lightbulbs.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    lightGrid = {}
    initialOn = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            lightGrid[(x, y)] = char
            if char == "#":
                initialOn.add((x, y))

    maxX = max([x for x, y in lightGrid.keys()])
    maxY = max([y for x, y in lightGrid.keys()])
    # print grid
    for y in range(maxY + 1):
        for x in range(maxX + 1):
            print(lightGrid[(x, y)], end="")
        print()
    print()

    currentlyOn = initialOn.copy()
    steps = 100
    corners = [(0, 0), (0, maxY), (maxX, 0), (maxX, maxY)]
    for i in range(steps):
        newOn = set()
        possibleOn = {}
        turnOff = set()
        for bulb in currentlyOn:
            onNeighbours, possibleOnBulb = determineOnNeighbours(lightGrid, bulb)
            if (onNeighbours == 2 or onNeighbours == 3) or (bulb in corners):
                newOn.add(bulb)
            else:
                turnOff.add(bulb)
            for possible in possibleOnBulb:
                if possible in possibleOn:
                    possibleOn[possible] += 1
                else:
                    possibleOn[possible] = 1
        for possible in possibleOn:
            if possibleOn[possible] == 3:
                newOn.add(possible)
        for bulb in turnOff:
            lightGrid[bulb] = "."
        for bulb in newOn:
            lightGrid[bulb] = "#"
        currentlyOn = newOn.copy()

    # print grid
    for y in range(maxY + 1):
        for x in range(maxX + 1):
            print(lightGrid[(x, y)], end="")
        print()
    print()

    print("Part 1: ", len(currentlyOn))
    endTimeP1 = time.time()
    print("Time Part 1: ", endTimeP1 - start_time)
    print("Time P1 in ms: ", (endTimeP1 - start_time) * 1000)


def determineOnNeighbours(lightGrid, coord):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    onNeighbours = 0
    possbileON = set()
    # Iterate over each direction to check the neighbors
    for direction in directions:
        neighbour = (coord[0] + direction[0], coord[1] + direction[1])
        if neighbour in lightGrid and lightGrid[neighbour] == "#":
            onNeighbours += 1
        elif neighbour in lightGrid:
            possbileON.add(neighbour)
    return onNeighbours, possbileON


if __name__ == "__main__":
    main()
