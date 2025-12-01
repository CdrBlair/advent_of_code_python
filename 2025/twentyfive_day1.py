# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day1.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        directions = []
        for line in lines:
            direction, steps = line.strip()[:1], int(line.strip()[1:])
            directions.append((direction, steps))

    # print(directions)

    curpos = 50
    timesatzero = 0
    for direction, steps in directions:
        steps = steps % 100
        if direction == "R":
            curpos += steps
        elif direction == "L":
            curpos -= steps
        if curpos > 99:
            curpos = curpos - 100
        elif curpos < 0:
            curpos = 100 + curpos
        if curpos == 0:
            timesatzero += 1

    print("Final Position: ", curpos)
    print("Times at zero: ", timesatzero)
    endtime = time.time()
    print("Time part 1: ", endtime - start_time)
    print("Time part 1 in ms: ", (endtime - start_time) * 1000)

    curpos = 50
    timesatzero = 0
    for direction, steps in directions:
        rotatedfull = steps // 100
        timesatzero += rotatedfull
        steps = steps % 100
        original = curpos
        if direction == "R":
            curpos += steps
        elif direction == "L":
            curpos -= steps
        if curpos > 99:
            curpos = curpos - 100
            if curpos != 0:
                timesatzero += 1
        elif curpos < 0:
            curpos = 100 + curpos
            if curpos != 0 and original != 0:
                timesatzero += 1
        if curpos == 0:
            timesatzero += 1
    print("Final Position: ", curpos)
    print("Times at zero: ", timesatzero)


if __name__ == "__main__":
    main()
