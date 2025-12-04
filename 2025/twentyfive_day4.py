# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day4.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        maxY = len(lines)
        maxX = len(lines[0].strip())
        paperRolls = {}
        for y in range(maxY):
            line = lines[y].strip()
            for x in range(maxX):
                paperRolls[(x, y)] = line[x]

    # print paperRolls
    # for y in range(maxY):
    #     for x in range(maxX):
    #         print(paperRolls[(x, y)], end="")
    #     print()

    freeCount = 0
    freeRolls = []
    for y in range(maxY):
        for x in range(maxX):
            if paperRolls[(x, y)] == "@" and checkAdjacents(x, y, paperRolls):
                freeCount += 1
                freeRolls.append((x, y))

    # print map with free rolls marked with *
    # for y in range(maxY):
    #     for x in range(maxX):
    #         if (x, y) in freeRolls:
    #             print("x", end="")
    #         else:
    #             print(paperRolls[(x, y)], end="")
    #     print()

    print("Free rolls:", freeCount)
    endP1 = time.time()
    print("Part 1 execution time:", endP1 - start_time, "seconds")
    print("Part 1 time in ms:", (endP1 - start_time) * 1000, "ms ")

    freeRollsTotal = 0
    noFreeRoll = False
    while not noFreeRoll:
        freeCount = 0
        freeRolls = []
        for y in range(maxY):
            for x in range(maxX):
                if paperRolls[(x, y)] == "@" and checkAdjacents(x, y, paperRolls):
                    freeCount += 1
                    freeRolls.append((x, y))
        if freeCount == 0:
            noFreeRoll = True
        else:
            freeRollsTotal += freeCount
            for roll in freeRolls:
                paperRolls[roll] = "."
    print("Total free rolls removed:", freeRollsTotal)

    # print paperRolls
    # for y in range(maxY):
    #     for x in range(maxX):
    #         print(paperRolls[(x, y)], end="")
    #     print()

    endP2 = time.time()
    print("Part 2 execution time:", endP2 - endP1, "seconds")
    print("Part 2 time in ms:", (endP2 - endP1) * 1000, "ms ")


def checkAdjacents(x, y, paperRolls):
    adjancentRolls = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (
                abs(dx) + abs(dy) != 0
                and (x + dx, y + dy) in paperRolls
                and paperRolls[(x + dx, y + dy)] == "@"
            ):
                adjancentRolls += 1

    # print(f"Roll at ({x},{y}) has {adjancentRolls} adjacent rolls")
    return adjancentRolls < 4


if __name__ == "__main__":
    main()
