import os
import time
from collections import deque


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/lavatrail.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    maxX = len(lines[0].strip())
    maxY = len(lines)
    lavamap = {}
    trailheads = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            if int(char) == 0:
                trailheads.append((j, i))
            lavamap[(j, i)] = int(char)

    # print the map
    # for i in range(maxY):
    #     for j in range(maxX):
    #         print(lavamap[(j, i)], end="")
    #     print()
    # print(trailheads)
    trailheadsWithScore = {}
    for trailhead in trailheads:
        visited = set()
        stack = deque([trailhead])
        score = 0
        while stack:
            cur = stack.popleft()
            if cur in visited:
                continue
            visited.add(cur)
            neighbours = findpossibleneighbours(cur, lavamap)
            for neighbour in neighbours:
                if lavamap[neighbour] == 9:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        score += 1

                else:
                    stack.append(neighbour)
        trailheadsWithScore[trailhead] = score

    # print(trailheadsWithScore)
    print(sum(trailheadsWithScore.values()))
    endtimep1 = time.time()
    print("Part 1 time:", endtimep1 - start_time)
    print("Part 1 time in ms:", (endtimep1 - start_time) * 1000)

    trailheadsWithRating = {}
    rating = 0
    for trailhead in trailheads:
        stack = deque([trailhead])

        rating = 0
        while stack:
            # print(stack)
            cur = stack.popleft()
            neighbours = findpossibleneighbours(cur, lavamap)
            for neighbour in neighbours:
                if lavamap[neighbour] == 9:
                    rating += 1
                else:
                    stack.append(neighbour)
        trailheadsWithRating[trailhead] = rating
    # print(trailheadsWithRating)

    print(sum(trailheadsWithRating.values()))
    endtimep2 = time.time()
    print("Part 2 time:", endtimep2 - endtimep1)
    print("Part 2 time in ms:", (endtimep2 - endtimep1) * 1000)


def findpossibleneighbours(cur, lavamap):
    neighbours = []
    posNext = [
        (cur[0], cur[1] - 1),
        (cur[0] + 1, cur[1]),
        (cur[0], cur[1] + 1),
        (cur[0] - 1, cur[1]),
    ]
    for pos in posNext:
        if pos in lavamap and lavamap[pos] - lavamap[cur] == 1:
            neighbours.append(pos)
    return neighbours


if __name__ == "__main__":
    main()
