import os
import re
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/wordsearch.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        lines = [list(line.strip()) for line in lines]

    # print(lines)

    possibleStrings = []
    xLen = len(lines[0])
    yLen = len(lines)
    # constructing possible directions
    # top down
    for i in range(xLen):
        possibleStrings.append("".join([lines[j][i] for j in range(yLen)]))

    # bottom up
    possibleStrings.append(possibleStrings[0][::-1])

    # print(possibleStrings)

    # left to right
    for i in range(yLen):
        possibleStrings.append("".join([lines[i][j] for j in range(xLen)]))
    # right two left
    possibleStrings.append(possibleStrings[-1][::-1])

    # diagonal left up to right down
    for k in range(xLen + yLen - 1):
        diagonal1 = []
        diagonal2 = []
        for j in range(max(0, k - yLen + 1), min(k + 1, xLen)):
            diagonal1.append(lines[k - j][j])
            diagonal2.append(lines[j][k - j])
        if diagonal1:
            possibleStrings.append("".join(diagonal1))
        if diagonal2:
            possibleStrings.append("".join(diagonal2))

    # diagonal right up to left down
    for k in range(xLen + yLen - 1):
        diagonal1 = []
        diagonal2 = []
        for j in range(max(0, k - yLen + 1), min(k + 1, xLen)):
            diagonal1.append(lines[yLen - 1 - (k - j)][j])
            diagonal2.append(lines[yLen - 1 - j][k - j])
        if diagonal1:
            possibleStrings.append("".join(diagonal1))
        if diagonal2:
            possibleStrings.append("".join(diagonal2))

    xmas = "XMAS"

    sum = 0
    for string in possibleStrings:
        sum += string.count(xmas)

    print(sum)
    endtime = time.time()
    print("Time part 1: ", endtime - start_time)
    print("Time part 1 in ms: ", (endtime - start_time) * 1000)
    ms = "MS"
    sumMs = 0
    for i in range(yLen):
        for j in range(xLen):
            if lines[i][j] == "A":
                if i - 1 >= 0 and j - 1 >= 0 and i + 1 < yLen and j + 1 < xLen:

                    firstX = "".join(sorted(lines[i - 1][j - 1] + lines[i + 1][j + 1]))

                    secondX = "".join(sorted(lines[i - 1][j + 1] + lines[i + 1][j - 1]))

                    # print(firstX)
                    # print(secondX)
                    if firstX == ms and secondX == ms:
                        sumMs += 1
    print(sumMs)
    endtime = time.time()
    print("Time part 2: ", endtime - start_time)
    print("Time part 2 in ms: ", (endtime - start_time) * 1000)


if __name__ == "__main__":
    main()
