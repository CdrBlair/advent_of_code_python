# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day3.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        jolts = [line.strip() for line in lines]

    sumOfCombinations = 0
    for jolt in jolts:
        sumOfCombinations += findHighestCombination(jolt)
    print("Sum of highest combinations:", sumOfCombinations)

    endP1 = time.time()
    print("Part 1 execution time:", endP1 - start_time, "seconds")
    print("Part 1 time in ms:", (endP1 - start_time) * 1000, "ms ")

    sumOfHighest12digits = 0
    for jolt in jolts:
        sumOfHighest12digits += findHighest12digits(jolt)
    print("Sum of highest 12 digits:", sumOfHighest12digits)

    endP2 = time.time()
    print("Part 2 execution time:", endP2 - endP1, "seconds")
    print("Part 2 time in ms:", (endP2 - endP1) * 1000, "ms ")


def findHighestCombination(jolt):
    # jolt as int list
    joltint = [int(x) for x in jolt]
    # find index of hihgest number which is latest in the list
    highest = max(joltint[:-1])
    highestIndex = jolt.find(str(highest))
    # find highest after first highest
    nextHighest = max(joltint[highestIndex + 1 :])
    combination = int(str(highest) + str(nextHighest))
    return combination


def findHighest12digits(jolt):
    joltint = [int(x) for x in jolt]

    digitsfound = 0
    digits = []
    highestIndex = -1
    while digitsfound < 12:
        # print(highestIndex, digitsfound)
        # print(joltint[highestIndex + 1 : (-(12 - digitsfound))])
        endIndex = (-12 + digitsfound + 1) if (-12 + digitsfound + 1) != 0 else None

        highest = max(joltint[highestIndex + 1 : endIndex])
        # print(jolt[highestIndex + 1 :])
        highestIndex = jolt[highestIndex + 1 :].find(str(highest)) + highestIndex + 1
        # print(highestIndex)

        # print(highestIndex)
        digits.append(str(highest))
        digitsfound += 1
        # print(digits)
        # print(digitsfound)
    # print("".join(digits))
    return int("".join(digits))


if __name__ == "__main__":
    main()
