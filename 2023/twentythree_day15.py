import os
import time
from collections import OrderedDict
from functools import cache


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/lava_init.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        full_init = file.readlines()[0].strip()

    steps = full_init.split(",")

    overallSum = 0
    for step in steps:
        overallSum += reindeerHash(step)

    print("Overall sum: ", overallSum)
    endTimeP1 = time.time()
    print("Part one time: ", endTimeP1 - start_time)
    print("Part one time in ms: ", (endTimeP1 - start_time) * 1000)

    reindeerHash.cache_clear()

    boxes = [OrderedDict() for _ in range(256)]
    convertedSteps = []
    for step in steps:
        if step[-2] == "=":
            parts = step.split("=")
            convertedSteps.append((parts[0], "=", int(parts[1])))
        else:
            parts = step.split("-")
            convertedSteps.append((parts[0], "-", None))

    for step in convertedSteps:
        hash = reindeerHash(step[0])
        if step[1] == "=":
            boxes[hash][step[0]] = step[2]
        else:
            if step[0] in boxes[hash]:
                boxes[hash].pop(step[0])

    focalSum = 0
    for i, box in enumerate(boxes):
        if len(box) > 0:
            boxaslist = list(box)
            for j, key in enumerate(box):
                focalSum += (1 + i) * (j + 1) * box[key]
    print("Cache information: ", reindeerHash.cache_info())
    print("Focal sum: ", focalSum)
    endTimeP2 = time.time()
    print("Part two time: ", endTimeP2 - endTimeP1)
    print("Part two time in ms: ", (endTimeP2 - endTimeP1) * 1000)
    print("Total time: ", endTimeP2 - start_time)
    print("Total time in ms: ", (endTimeP2 - start_time) * 1000)


# HASH Algorhitm
@cache
def reindeerHash(step):
    currentValue = 0
    for char in step:
        currentValue += ord(char)
        currentValue *= 17
        currentValue %= 256
    # print("Step: ", step, " hash: ", currentValue)
    return currentValue


if __name__ == "__main__":
    main()
