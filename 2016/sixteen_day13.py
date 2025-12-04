import time
from ast import While

from cycler import V
from pyparsing import deque


def main():

    start_time = time.time()
    start = (1, 1)
    target = (31, 39)
    queue = deque([start])
    visited = set()
    visited.add(start)
    steps = 0
    found = False

    while queue and not found:
        for _ in range(len(queue)):
            curx, cury = queue.popleft()
            if (curx, cury) == target:
                found = True
                break
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                newx = curx + dx
                newy = cury + dy
                if (
                    newx >= 0
                    and newy >= 0
                    and not is_wall(newx, newy)
                    and (newx, newy) not in visited
                ):
                    visited.add((newx, newy))
                    queue.append((newx, newy))
        if not found:
            steps += 1
    print("Steps to target: ", steps)
    print("Time taken: ", time.time() - start_time)
    print("Time taken in ms: ", (time.time() - start_time) * 1000)
    time_part2_start = time.time()
    start = (1, 1)
    queue = deque([start])
    visited = set()
    visited.add(start)
    maxSteps = 50
    steps = 0
    while steps < maxSteps:
        for _ in range(len(queue)):
            curx, cury = queue.popleft()
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                newx = curx + dx
                newy = cury + dy
                if (
                    newx >= 0
                    and newy >= 0
                    and not is_wall(newx, newy)
                    and (newx, newy) not in visited
                ):
                    visited.add((newx, newy))
                    queue.append((newx, newy))
        steps += 1
    print("Positions reachable in 50 steps: ", len(visited))
    endtime = time.time()
    print("Time taken for part 2: ", endtime - time_part2_start)
    print("Time taken for part 2 in ms: ", (endtime - time_part2_start) * 1000)


def is_wall(x, y):
    find = x * x + 3 * x + 2 * x * y + y + y * y
    magic_number = 1362
    find += magic_number
    bits = bin(find)
    ones = bits.count("1")
    if ones % 2 == 0:
        return False
    else:
        return True


if __name__ == "__main__":
    main()
