import os
import time
from dis import disco


def main():
    start_time = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/discpos.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        discs = []
        for line in lines:
            parts = line.strip().split(" ")
            discs.append((int(parts[3]), int(parts[-1].replace(".", ""))))

    # initialize discs so that they are stored at the time they are reached
    reposdiscs = []
    for index in range(len(discs)):
        pos = (discs[index][1] + index + 1) % discs[index][0]
        reposdiscs.append((discs[index][0], pos))

    timetoTry = 0
    found = False
    while not found:
        if all(
            (reposdiscs[i][1]) % reposdiscs[i][0] == 0 for i in range(len(reposdiscs))
        ):
            found = True
            break
        for i in range(len(reposdiscs)):
            reposdiscs[i] = (
                reposdiscs[i][0],
                (reposdiscs[i][1] + 1) % reposdiscs[i][0],
            )
        timetoTry += 1
    print("Time to try:", timetoTry)
    endP1 = time.time()
    print("Time taken P1: ", endP1 - start_time)
    print("Time taken P1 in ms: ", (endP1 - start_time) * 1000)

    newDiscs = discs + [(11, 0)]
    reposdiscs = []
    for index in range(len(newDiscs)):
        pos = (newDiscs[index][1] + index + 1) % newDiscs[index][0]
        reposdiscs.append((newDiscs[index][0], pos))
    timetoTry = 0
    found = False
    while not found:
        if all(
            (reposdiscs[i][1]) % reposdiscs[i][0] == 0 for i in range(len(reposdiscs))
        ):
            found = True
            break
        for i in range(len(reposdiscs)):
            reposdiscs[i] = (
                reposdiscs[i][0],
                (reposdiscs[i][1] + 1) % reposdiscs[i][0],
            )
        timetoTry += 1
    print("Time to try:", timetoTry)
    endP2 = time.time()
    print("Time taken P2: ", endP2 - endP1)
    print("Time taken P2 in ms: ", (endP2 - endP1) * 1000)


if __name__ == "__main__":
    main()
