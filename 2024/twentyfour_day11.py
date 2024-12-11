import os
import string
import time
from functools import lru_cache
from hmac import new


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/stones.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        line = file.readline().strip()

    stones = []

    stones = [int(x) for x in line.split(" ")]
    print(stones)
    stonesp2 = {}
    for stone in stones:
        if stone in stonesp2:
            stonesp2[stone] += 1
        else:
            stonesp2[stone] = 1

    blinks = 25

    for i in range(blinks):
        # print(i)
        # print(len(stones))
        newStones = []
        for stone in stones:
            newStones.extend(processStone(stone))
        stones = newStones
    # print(stones)
    print(len(stones))

    endtimep1 = time.time()
    print("Time part 1: ", endtimep1 - start_time)
    print("Time part 1 in ms: ", (endtimep1 - start_time) * 1000)

    blinks = 75

    for i in range(blinks):
        # print(i)
        # tempcopy
        stonesp2copy = stonesp2.copy()
        for stone in stonesp2copy:
            if stonesp2copy[stone] == 0:
                continue
            current = stonesp2copy[stone]
            stonesp2[stone] -= current
            for newstone in processStone(stone):
                if newstone in stonesp2:
                    stonesp2[newstone] += 1 * current
                else:
                    stonesp2[newstone] = 1 * current
        # print(stonesp2)
    print(sum(stonesp2.values()))

    endtimep2 = time.time()
    print("Time part 2: ", endtimep2 - endtimep1)
    print("Time part 2 in ms: ", (endtimep2 - endtimep1) * 1000)


@lru_cache
def processStone(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 != 0:
        # print(stone)
        return [stone * 2024]
    else:
        # print(stone)
        stringstone = str(stone)
        mid = len(stringstone) // 2
        return [int(stringstone[:mid]), int(stringstone[mid:])]
        # print(newStones)


if __name__ == "__main__":
    main()
