# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day5.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        readRanges = False
        ranges = []
        foodIds = []
        for line in lines:
            line = line.strip()
            if line == "":
                readRanges = True
                continue
            if not readRanges:
                parts = line.split("-")
                ranges.append((int(parts[0]), int(parts[1])))
            else:
                foodIds.append(int(line))

    numberOfvalidIds = 0
    for id in foodIds:
        for start, end in ranges:
            if start <= id <= end:
                numberOfvalidIds += 1
                break

    print(numberOfvalidIds)
    endP1 = time.time()
    print("Part 1 execution time:", endP1 - start_time, "seconds")
    print("Part 1 time in ms:", (endP1 - start_time) * 1000, "ms ")

    ranges.sort(key=lambda x: x[0])
    mergedRanges = []
    currentStart, currentEnd = ranges[0]
    print(ranges)
    for start, end in ranges[1:]:
        print(start, end, currentStart, currentEnd)
        if start <= currentEnd + 1:
            currentEnd = max(currentEnd, end)
        else:
            mergedRanges.append((currentStart, currentEnd))
            currentStart, currentEnd = start, end
        print("Current merged:", mergedRanges)
    mergedRanges.append((currentStart, currentEnd))

    totalValidIds = 0
    print(mergedRanges)
    for start, end in mergedRanges:
        totalValidIds += end - start + 1
    print(totalValidIds)


if __name__ == "__main__":
    main()
