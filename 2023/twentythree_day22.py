import copy
import os
import time
from collections import deque
from multiprocessing import Pool


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/bricks.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    bricks = []
    for i, line in enumerate(lines):
        positions = line.strip().split("~")
        start = positions[0].split(",")
        end = positions[1].split(",")
        bricks.append(
            {
                "start": (int(start[0]), int(start[1]), int(start[2])),
                "end": (int(end[0]), int(end[1]), int(end[2])),
                "id": i,
            }
        )
    grid = {}
    for brick in bricks:
        for x in range(brick["start"][0], brick["end"][0] + 1):
            for y in range(brick["start"][1], brick["end"][1] + 1):
                for z in range(brick["start"][2], brick["end"][2] + 1):
                    grid[(x, y, z)] = ("#", brick["id"])

    maxX = max([x[0] for x in grid.keys()])
    maxY = max([x[1] for x in grid.keys()])
    maxZ = max([x[2] for x in grid.keys()])

    bricks = sorted(bricks, key=lambda k: k["start"][2])

    # print view from y
    # for z in range(maxZ + 1, -1, -1):
    #     for x in range(maxX + 1):
    #         yFound = False
    #         for y in range(maxY + 1):
    #             if (x, y, z) in grid:
    #                 print(grid[(x, y, z)][0], end="")
    #                 yFound = True
    #                 break
    #         if not yFound:
    #             print(".", end="")

    #     print()
    # print()

    for brick in bricks:
        brick, grid = letBrickFall(brick, grid)
    maxX = max([x[0] for x in grid.keys()])
    maxY = max([x[1] for x in grid.keys()])
    maxZ = max([x[2] for x in grid.keys()])

    # print view from y
    # for z in range(maxZ + 1, -1, -1):
    #     for x in range(maxX + 1):
    #         yFound = False
    #         for y in range(maxY + 1):
    #             if (x, y, z) in grid:
    #                 print(grid[(x, y, z)][0], end="")
    #                 yFound = True
    #                 break
    #         if not yFound:
    #             print(".", end="")

    #     print()
    # print()

    supportingBrickList = {}
    for brick in bricks:
        supportingBrickList[brick["id"]] = findSupportingBricks(brick, grid)
    # print(supportingBrickList)

    canNotDesintegrated = set()
    # check if only one brick is supporting, if yes add to canNotDesintegrated
    for brick in bricks:
        if len(supportingBrickList[brick["id"]]) == 1:
            canNotDesintegrated.add(list(supportingBrickList[brick["id"]])[0])
    # remove ground
    canNotDesintegrated.discard(-1)

    # print all bricks which are not in canNotDesintegrated
    all_brick_ids = {brick["id"] for brick in bricks}  # set of all brick IDs
    canBeDisintegrated = all_brick_ids - canNotDesintegrated  # set difference operation

    print("Number of bricks which can be disintegrated: ", len(canBeDisintegrated))
    endTimeP1 = time.time()
    print("Time taken p1: ", endTimeP1 - start_time)
    print("Time in ms p1: ", (endTimeP1 - start_time) * 1000)

    # P2
    # desintegrate blocks and check if others will fall, add to falling list
    # print(supportingBrickList)
    # fallingBricks = []
    # for brick in bricks:
    #     fallingBricks.append(checkMovingBricks(brick, supportingBrickList))

    with Pool() as p:
        fallingBricks = p.starmap(
            checkMovingBricks,
            [(brick, supportingBrickList) for i, brick in enumerate(bricks)],
        )
        # stack = deque([brick["id"]])
        # tempSupportingBrickList = copy.deepcopy(supportingBrickList)

        # fallingBrickCount = 0
        # while stack:
        #     currentBrick = stack.pop()

        #     for supportedBrick in tempSupportingBrickList:
        #         if currentBrick in tempSupportingBrickList[supportedBrick]:
        #             tempSupportingBrickList[supportedBrick].remove(currentBrick)
        #             if len(tempSupportingBrickList[supportedBrick]) == 0:
        #                 stack.append(supportedBrick)
        #                 fallingBrickCount += 1
        # fallingBricks.append(fallingBrickCount)

    print("Number of bricks which will fall: ", sum(fallingBricks))
    endTimeP2 = time.time()
    print("Time taken p2: ", endTimeP2 - endTimeP1)
    print("Time in ms p2: ", (endTimeP2 - endTimeP1) * 1000)
    print("Total time: ", endTimeP2 - start_time)


def checkMovingBricks(brick, supportingBrickList):
    stack = deque([brick["id"]])

    # tempSupportingBrickList = copy.deepcopy(supportingBrickList)
    tempSupportingBrickList = {
        k: {x for x in v} for k, v in supportingBrickList.items()
    }

    fallingBrickCount = 0
    while stack:
        currentBrick = stack.pop()

        for supportedBrick in tempSupportingBrickList:
            supportedSet = tempSupportingBrickList[supportedBrick]
            if currentBrick in supportedSet:
                supportedSet.remove(currentBrick)
                if len(supportedSet) == 0:
                    stack.append(supportedBrick)
                    fallingBrickCount += 1

    return fallingBrickCount


# For all bricks find supporting bricks
def findSupportingBricks(brick, grid):
    # Ground
    if brick["start"][2] == 1:
        return set([-1])
    supportingBricks = set()
    for x in range(brick["start"][0], brick["end"][0] + 1):
        for y in range(brick["start"][1], brick["end"][1] + 1):
            if (x, y, brick["start"][2] - 1) in grid:
                supportingBricks.add(grid[(x, y, brick["start"][2] - 1)][1])
    return supportingBricks


# Move one brick if there is space beneath
def letBrickFall(brick, grid):
    # print("letBrickFall", brick)
    # check orientation
    if brick["start"][0] != brick["end"][0]:
        orientation = "x"
    elif brick["start"][1] != brick["end"][1]:
        orientation = "y"
    else:
        orientation = "z"

    originalStart = brick["start"]
    originalEnd = brick["end"]

    # only need to check below one block
    if orientation == "z":
        z = brick["start"][2] - 1
        while z > 0 and (brick["start"][0], brick["start"][1], z) not in grid:
            z -= 1
        if z + 1 != brick["start"][2]:
            oldDeltaZ = brick["end"][2] - brick["start"][2]
            brick["start"] = (brick["start"][0], brick["start"][1], z + 1)
            brick["end"] = (brick["end"][0], brick["end"][1], z + 1 + oldDeltaZ)
            # remove old brick
            for z in range(originalStart[2], originalEnd[2] + 1):
                del grid[(originalStart[0], originalStart[1], z)]
            # add new brick
            for z in range(brick["start"][2], brick["end"][2] + 1):
                grid[(brick["start"][0], brick["start"][1], z)] = ("#", brick["id"])

    elif orientation == "x":
        z = brick["start"][2] - 1
        nothingInWay = True
        while z > 0 and nothingInWay:
            for x in range(brick["start"][0], brick["end"][0] + 1):
                if (x, brick["start"][1], z) in grid:
                    nothingInWay = False
                    break
            if nothingInWay:
                z -= 1
        if z + 1 != brick["start"][2]:
            brick["start"] = (brick["start"][0], brick["start"][1], z + 1)
            brick["end"] = (brick["end"][0], brick["end"][1], z + 1)
            # remove old brick
            for x in range(originalStart[0], originalEnd[0] + 1):
                del grid[(x, originalStart[1], originalStart[2])]
            # add new brick
            for x in range(brick["start"][0], brick["end"][0] + 1):
                grid[(x, brick["start"][1], brick["start"][2])] = ("#", brick["id"])
    elif orientation == "y":
        z = brick["start"][2] - 1
        nothingInWay = True
        while z > 0 and nothingInWay:
            for y in range(brick["start"][1], brick["end"][1] + 1):
                if (brick["start"][0], y, z) in grid:
                    nothingInWay = False
                    break
            if nothingInWay:
                z -= 1
        if z + 1 != brick["start"][2]:
            brick["start"] = (brick["start"][0], brick["start"][1], z + 1)
            brick["end"] = (brick["end"][0], brick["end"][1], z + 1)
            # remove old brick
            for y in range(originalStart[1], originalEnd[1] + 1):
                del grid[(originalStart[0], y, originalStart[2])]
            # add new brick
            for y in range(brick["start"][1], brick["end"][1] + 1):
                grid[(brick["start"][0], y, brick["start"][2])] = ("#", brick["id"])

    # print("letBrickFall", brick)
    return brick, grid


if __name__ == "__main__":
    main()
