import os
import time
from functools import cache
from hmac import new
from itertools import product
from multiprocessing import Pool


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/springs.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    springs = []
    for line in lines:
        splitted = line.strip().split(" ")

        springs.append(
            (splitted[0], tuple([int(x) for x in splitted[1].strip().split(",")]))
        )

    # find_possible_combinations(springs[1])
    springs = tuple(springs)

    with Pool() as p:
        sumOfCombinations = p.starmap(
            newCombinationWay,
            [(spring,) for i, spring in enumerate(springs)],
        )

    # for spring in springs:
    #     print("String: ", spring[0], "Combinations:", newCombinationWay(spring))

    print(sum(sumOfCombinations))
    endTimeP1 = time.time()
    print("Time taken p1", endTimeP1 - start_time)
    print("Time taken in ms", (endTimeP1 - start_time) * 1000)

    # Expand springs and values by 5
    expandedSprings = []
    for spring in springs:
        tempString = "?" + spring[0]
        expandedSprings.append(
            (
                spring[0] + 4 * tempString,
                tuple(5 * spring[1]),
            )
        )
    expandedSprings = tuple(expandedSprings)
    with Pool() as p:
        sumOfCombinationsExpanded = p.starmap(
            newCombinationWay,
            [(spring,) for i, spring in enumerate(expandedSprings)],
        )
    print(sum(sumOfCombinationsExpanded))
    endTimeP2 = time.time()
    print("Time taken p2", endTimeP2 - endTimeP1)
    print("Time taken in ms", (endTimeP2 - endTimeP1) * 1000)
    print("Time taken total", endTimeP2 - start_time)
    print("Time taken in ms", (endTimeP2 - start_time) * 1000)


@cache
def newCombinationWay(spring):
    count = 0
    if not spring[1]:
        if "#" in spring[0]:
            return 0
        return 1
    if len(spring[0]) < spring[1][0]:
        return 0
    if not "." in spring[0][: spring[1][0]]:
        if len(spring[0]) == spring[1][0] or spring[0][spring[1][0]] != "#":
            count += newCombinationWay((spring[0][spring[1][0] + 1 :], spring[1][1:]))
    if spring[0][0] != "#":
        count += newCombinationWay((spring[0][1:], spring[1]))

    return count


# Find possible combinations
def find_possible_combinations(index, spring):
    springString = spring[0]
    springValues = spring[1]
    lengthSprings = len(springString)
    # print("Spring String:", lengthSprings)

    possibleCombinations = 0
    # needed number of factors == values -1 (between) + 2 (start and end)
    numberOfFactors = len(springValues) + 1
    # Upper Boundary for factors is the length of the string minus values of the spring minus 1 for each in between space
    upperBoundary = lengthSprings - sum(springValues) - (numberOfFactors - 2)
    # Lower boundary for inner factors is 1
    lowerBoundaryInner = 1
    # Lower boundary for outer factors is 0
    lowerBoundaryOuter = 0

    # Construct factors
    factors = []
    # print(numberOfFactors)
    # print("Upper Boundary:", upperBoundary)
    for i in range(numberOfFactors):
        factors.append([])
        if i == 0 or i + 1 == numberOfFactors:
            for j in range(lowerBoundaryOuter, upperBoundary + 1):
                factors[i].append(j)
        else:
            # +2 because upperboundary was calculated having in mind that in between there is alway 1
            for j in range(lowerBoundaryInner, upperBoundary + 2):
                factors[i].append(j)

    # print(factors)
    # Construct combinations
    factorCombinations = list(product(*factors))
    # print(len(factorCombinations))

    numberOfPossibleCombinations = 0
    # Construct possible strings and check
    for factorCombination in factorCombinations:
        if not sum(factorCombination) + sum(springValues) == lengthSprings:
            # if factorCombination == (1, 3, 4, 1):
            #     print("Not valid:", factorCombination, "Spring Values:", springValues)
            continue

        # Construct string
        string = ""
        # if factorCombination == (1, 3, 4, 1):
        #     print("Number of factors:", numberOfFactors)
        for i in range(numberOfFactors):
            if i == 0 or i + 1 == numberOfFactors:
                if i + 1 == numberOfFactors:
                    string += "#" * springValues[i - 1]
                string += "." * factorCombination[i]
            else:
                string += "#" * springValues[i - 1]
                string += "." * factorCombination[i]

        # Check if string is valid
        if checkString(string, springString):
            numberOfPossibleCombinations += 1

        # if factorCombination == (1, 3, 4, 1):
        #     print("Constr String:", string)
        #     print("Inpput String:", springString)

    # if factorCombination == (1, 3, 4, 1):
    #     print(numberOfPossibleCombinations
    return (index, numberOfPossibleCombinations)


def checkString(possible, real):
    for i, char in enumerate(real):
        if char == "?":
            continue
        if char != possible[i]:
            return False
    return True


if __name__ == "__main__":
    main()
