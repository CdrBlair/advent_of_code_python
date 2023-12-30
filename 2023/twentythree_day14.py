import os
import time
from functools import cache
from math import e
from typing import final


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/dishrocks.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    rocks = {}
    heigth = len(lines)
    width = len(lines[0].strip())

    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            rocks[(j, i)] = char
    # print rocks
    # for i in range(heigth):
    #     for j in range(width):
    #         print(rocks[(j, i)], end="")
    #     print()
    rocks_tuple = tuple(
        tuple(rocks[(j, i)] for j in range(width)) for i in range(heigth)
    )
    movedRocks = moveRocks(rocks_tuple, width, heigth)
    print()
    # print rocks
    # for i in range(heigth):
    #     for j in range(width):
    #         print(movedRocks[(j, i)], end="")
    #     print()

    print()
    print("Weight: ", calculateWeight(movedRocks, width, heigth))
    endTimeP1 = time.time()
    print("Part one time: ", endTimeP1 - start_time)
    print("Part one time in ms: ", (endTimeP1 - start_time) * 1000)

    # Part two
    start_timeP2 = time.time()
    movedRocks = rocks_tuple
    weight = 0
    weigths = []
    finalrocks = {}
    for i in range(1000000000):
        movedRocks = moveRocks(movedRocks, width, heigth, "up")

        movedRocks = tuple(
            tuple(movedRocks[(j, i)] for j in range(width)) for i in range(heigth)
        )
        movedRocks = moveRocks(movedRocks, width, heigth, "left")

        movedRocks = tuple(
            tuple(movedRocks[(j, i)] for j in range(width)) for i in range(heigth)
        )
        movedRocks = moveRocks(movedRocks, width, heigth, "down")

        movedRocks = tuple(
            tuple(movedRocks[(j, i)] for j in range(width)) for i in range(heigth)
        )
        movedRocks = moveRocks(movedRocks, width, heigth, "right")

        movedRocks = tuple(
            tuple(movedRocks[(j, i)] for j in range(width)) for i in range(heigth)
        )
        rocks = {
            (j, i): char
            for i, row in enumerate(movedRocks)
            for j, char in enumerate(row)
        }
        currentWeigth = calculateWeight(rocks, width, heigth)
        if moveRocks.cache_info().hits > 4:
            # if moveRocks.cache_info().hits == 2:
            #     print("first loop at iteration: ", i)
            # print(i)
            # print("cache hits: ", moveRocks.cache_info().hits)

            # print(i)
            # print("Current weight: ", currentWeigth)
            # print(weigths)
            if currentWeigth in [x[0] for x in weigths]:
                # print("Found loop at iteration: ", i)
                indices = [
                    index for weight, index in weigths if weight == currentWeigth
                ]
                indexFoundWeight = indices[0] if indices else None

                if (999999999 - i) % (i - indexFoundWeight) == 0:
                    # print(i)
                    # print("Index found weight: ", indexFoundWeight)
                    # print("mode", (999999999 - i) % (i - indexFoundWeight))
                    # print("Weight: ", currentWeigth)
                    # for i in range(heigth):
                    #     for j in range(width):
                    #         print(rocks[(j, i)], end="")
                    #     print()
                    finalrocks = rocks
                    break

        weigths.append((currentWeigth, i))

    print("Weight: ", calculateWeight(finalrocks, width, heigth))
    endTimeP2 = time.time()
    print("Part two time: ", endTimeP2 - start_timeP2)
    print("Part two time in ms: ", (endTimeP2 - start_timeP2) * 1000)
    print("Total time: ", endTimeP2 - start_time)


# calculate Weitght
def calculateWeight(rocks, width, heigth):
    weight = 0
    for i in range(heigth):
        for j in range(width):
            if rocks[(j, i)] == "O":
                weight += heigth - i
    return weight


# Move rocks up one row
@cache
def moveRocks(rocks, width, heigth, direction="up"):
    rocks = {(j, i): char for i, row in enumerate(rocks) for j, char in enumerate(row)}

    if direction == "up":
        # rows y
        for i in range(heigth):
            # columns x
            for j in range(width):
                # row above y
                # print(j, i)
                if rocks[(j, i)] == "O":
                    for k in range(i - 1, -1, -1):
                        # print(j, i, k)
                        if not rocks[(j, k)] == ".":
                            if k < i - 1:
                                rocks[(j, k + 1)] = "O"
                                rocks[(j, i)] = "."
                            # print rocks
                            # print(rocks)
                            # for a in range(heigth):
                            #     for b in range(width):
                            #         print(rocks[(b, a)], end="")
                            #     print()
                            break
                        elif k == 0:
                            rocks[(j, k)] = "O"
                            rocks[(j, i)] = "."
    if direction == "down":
        # rows y
        for i in range(heigth - 1, -1, -1):
            # columns x
            for j in range(width):
                # row above y
                # print(j, i)
                if rocks[(j, i)] == "O":
                    for k in range(i + 1, heigth):
                        # print(j, i, k)
                        if not rocks[(j, k)] == ".":
                            if k > i + 1:
                                rocks[(j, k - 1)] = "O"
                                rocks[(j, i)] = "."
                            # print rocks
                            # print(rocks)
                            # for a in range(heigth):
                            #     for b in range(width):
                            #         print(rocks[(b, a)], end="")
                            #     print()
                            break
                        elif k == heigth - 1:
                            rocks[(j, k)] = "O"
                            rocks[(j, i)] = "."
    if direction == "left":
        # columns x
        for j in range(width):
            # rows y
            for i in range(heigth):
                if rocks[(j, i)] == "O":
                    for k in range(j - 1, -1, -1):
                        # print(j, i, k)
                        if not rocks[(k, i)] == ".":
                            if k < j - 1:
                                rocks[(k + 1, i)] = "O"
                                rocks[(j, i)] = "."
                            # print rocks
                            # print(rocks)
                            # for a in range(heigth):
                            #     for b in range(width):
                            #         print(rocks[(b, a)], end="")
                            #     print()
                            break
                        elif k == 0:
                            rocks[(k, i)] = "O"
                            rocks[(j, i)] = "."
    if direction == "right":
        # columns x
        for j in range(width - 1, -1, -1):
            # rows y
            for i in range(heigth):
                if rocks[(j, i)] == "O":
                    for k in range(j + 1, width):
                        # print(j, i, k)
                        if not rocks[(k, i)] == ".":
                            if k > j + 1:
                                rocks[(k - 1, i)] = "O"
                                rocks[(j, i)] = "."
                            # print rocks
                            # print(rocks)
                            # for a in range(heigth):
                            #     for b in range(width):
                            #         print(rocks[(b, a)], end="")
                            #     print()
                            break
                        elif k == width - 1:
                            rocks[(k, i)] = "O"
                            rocks[(j, i)] = "."

                # print(rocks)
                # for a in range(heigth):
                #     for b in range(width):
                #         print(rocks[(b, a)], end="")
                #     print()
    return rocks


if __name__ == "__main__":
    main()
