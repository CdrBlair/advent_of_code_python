# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day2.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        line = file.readline()
        rangesText = line.strip().split(",")
        ranges = []
        for rangetxt in rangesText:
            start, end = rangetxt.split("-")
            start = int(start)
            end = int(end)
            ranges.append((start, end))

    print(ranges)

    sumOfWrongIds = 0
    for r in ranges:
        start, end = r
        for i in range(start, end + 1):
            if checkIftwice(i):
                sumOfWrongIds += i
                # print(i)

    print("P1: ", sumOfWrongIds)
    endP1time = time.time()
    print("Time part 1: ", endP1time - start_time)
    print("Time part 1 in ms: ", (endP1time - start_time) * 1000)

    sumOfWrongIds = 0
    for r in ranges:
        start, end = r
        for i in range(start, end + 1):
            if checkRepeating(i):
                sumOfWrongIds += i
                # print(i)
    print("P2: ", sumOfWrongIds)
    endP2time = time.time()
    print("Time part 2: ", endP2time - endP1time)
    print("Time part 2 in ms: ", (endP2time - endP1time) * 1000)


def checkIftwice(x):
    text = str(x)
    length = len(text)
    if length % 2 != 0:
        # print("%2", x)
        return False
    ltext = text[: (length // 2)]
    rtext = text[length // 2 :]
    if ltext == rtext:
        # print("equals l, r, x", ltext, rtext, x)
        return True
    else:
        # print("not equals l, r, x", ltext, rtext, x)
        return False


def checkRepeating(x):
    text = str(x)
    length = len(text)
    halfLength = length // 2
    for i in range(halfLength):
        currentSeq = text[: (i + 1)]
        times = length // (i + 1)
        if times * currentSeq == text:
            return True

    return False


if __name__ == "__main__":
    main()
