# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day7.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    grid = {}
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        y = 0
        for line in lines:
            x = 0
            line = line.strip()
            for c in line:
                grid[(x, y)] = c
                if c == "S":
                    start = (x, y)
                x += 1

            y += 1
    maxX = x
    maxY = y
    # print grid
    for y in range(maxY):
        row = ""
        for x in range(maxX):
            row += grid[(x, y)]
        print(row)

    tachyonbeams = set()
    tachyonbeams.add((start[0], start[1] + 1))
    timelines = {}
    timelines[(start[0], start[1] + 1)] = 1
    print("Starting at: ", start)
    print("Initial Beams: ", tachyonbeams)
    splits = 0
    for i in range(2, maxY):
        for j in range(maxX):
            if grid[(j, i)] == "^":
                if (j, i - 1) in tachyonbeams:
                    splits += 1
                    tachyonbeams.add((j - 1, i))
                    tachyonbeams.add((j + 1, i))
                    if (j - 1, i) in timelines:
                        timelines[(j - 1, i)] = (
                            timelines[(j - 1, i)] + timelines[(j, i - 1)]
                        )
                    else:
                        timelines[(j - 1, i)] = timelines[(j, i - 1)]
                    if (j + 1, i) in timelines:
                        timelines[(j + 1, i)] = (
                            timelines[(j + 1, i)] + timelines[(j, i - 1)]
                        )
                    else:
                        timelines[(j + 1, i)] = timelines[(j, i - 1)]
            else:
                if (j, i - 1) in tachyonbeams:
                    tachyonbeams.add((j, i))
                    if (j, i) in timelines:
                        timelines[(j, i)] = timelines[(j, i)] + timelines[(j, i - 1)]
                    else:
                        timelines[(j, i)] = timelines[(j, i - 1)]
    # print("Timelines: ", timelines)
    sumTimelines = sum(
        timelines[(x, maxY - 1)] for x in range(maxX) if (x, maxY - 1) in timelines
    )

    # print with beams
    print("")
    for y in range(maxY):
        row = ""
        for x in range(maxX):
            if (x, y) in tachyonbeams:
                row += "|"
            else:
                row += grid[(x, y)]
        print(row)

    print("Total Timelines: ", sumTimelines)
    print("Total Splits: ", splits)
    end_time = time.time()
    print("Time: ", end_time - start_time)
    print("Time in ms: ", (end_time - start_time) * 1000)


if __name__ == "__main__":
    main()
