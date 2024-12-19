import os
import time
from functools import lru_cache

from numpy import number


def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/towels.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    towels = frozenset()
    designs = []
    readTowel = False
    for line in lines:
        if line.strip() == "":
            readTowel = True
            continue
        if not readTowel:
            towels = towels.union(
                [string.strip() for string in line.strip().split(",")]
            )
        else:
            designs.append(line.strip())
    # print(towels)
    # print(designs)
    numberOfPossibleDesigns = 0
    for design in designs:
        if possibleTowelSequence(towels, design):
            numberOfPossibleDesigns += 1

    print(numberOfPossibleDesigns)

    endtime = time.time()
    print("Part 1 took: ", endtime - starttime)
    print("Part 1 took in ms: ", (endtime - starttime) * 1000)

    sumOfAllWays = 0
    for design in designs:
        designPossible, numberOfWaysToMakeDesign = findAllpossibleTowelSequence(
            towels, design
        )
        if designPossible:
            sumOfAllWays += numberOfWaysToMakeDesign
    print(sumOfAllWays)
    # print cache statistics
    endtimeP2 = time.time()
    print("Part 2 took: ", endtimeP2 - endtime)
    print("Part 2 took in ms: ", (endtimeP2 - endtime) * 1000)


@lru_cache
def possibleTowelSequence(towels, design):
    for towel in towels:
        if design.startswith(towel):
            remainingDesign = design[len(towel) :]
            if remainingDesign == "":
                return True
            if possibleTowelSequence(towels, remainingDesign):
                return True
    return False


@lru_cache
def findAllpossibleTowelSequence(towels, design):
    numberOfWaysToMakeDesign = 0
    designPossible = False
    for towel in towels:
        if design.startswith(towel):
            remainingDesign = design[len(towel) :]
            if remainingDesign == "":
                designPossible = True
                numberOfWaysToMakeDesign += 1
            else:
                possible, ways = findAllpossibleTowelSequence(towels, remainingDesign)
                if possible:
                    designPossible = True
                    numberOfWaysToMakeDesign += ways
    return designPossible, numberOfWaysToMakeDesign


if __name__ == "__main__":
    main()
