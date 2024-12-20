import os
import time
from functools import lru_cache
from collections import deque



def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/racetrack.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    track = {}
    start = None
    finish = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            track[(x, y)] = c
            if c == 'S':
                start = (x, y)
            if c == 'E':
                finish = (x, y)
    maxX = max(x for x, y in track)
    maxY = max(y for x, y in track)
    
    # find walls with path around them
    walls = {}
    for (x, y), c in track.items():
        if c == '#' and x > 0 and y > 0 and x < maxX and y < maxY:
            for dx, dy in [ (1, 0), (0, 1), (-1, 0), (0, -1)]:
                if track.get((x + dx, y + dy)) == '.':
                    if (x, y) not in walls:
                        walls[(x, y)] = [(x + dx, y + dy)]
                    else:
                        walls[(x, y)].append((x + dx, y + dy))
    
    # print track
    for y in range(maxY + 1):
        for x in range(maxX + 1):
            print(track[(x, y)], end='')
        print()
    starttimetrack = time.time()
    standardTrackTime = findLengthShortestPath(start, finish, track)
    print(f"Time to find standard track: {time.time() - starttimetrack}")
    print(standardTrackTime)
    # apply cheats
    cheatsavings = {}
    
    for (x, y) in walls:
        #print(x,y)
        #print(i)
        track[(x, y)] = '.'
        cheatTime = findLengthShortestPath(start, finish, track)
        diff = standardTrackTime - cheatTime
        if diff > 0:
            if diff not in cheatsavings:
                cheatsavings[diff] = 1
            else:
                cheatsavings[diff] += 1
        track[(x, y)] = '#'
    
    # filter for diffs >= 100
    countSavings100 = 0
    for diff in cheatsavings:
        if diff >= 100:
            countSavings100 += cheatsavings[diff]
    print(countSavings100)
    endtimep1 = time.time()
    print("part 1 took: ",endtimep1 - starttime)
    print("part 1 took in ms: ",(endtimep1 - starttime) * 1000)






def findLengthShortestPath(start, finish, track):
    visited = set()
    q = deque([start])
    distance = 0
    while q:
        for _ in range(len(q)):
            x, y = q.popleft()
            if (x, y) == finish:
                return distance
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [ (1, 0), (0, 1), (-1, 0), (0, -1)]:
                if track.get((x + dx, y + dy)) != '#':
                    q.append((x + dx, y + dy))
        distance += 1

if __name__ == "__main__":
    main()

    
    