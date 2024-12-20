import os
import time
from functools import lru_cache
from collections import deque
import itertools



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


    #riddle says only one path is possible so we work with that....
    standardTrackTime, path = findShortestPath(start, finish, track)
    print(f"Time to find standard track: {time.time() - starttimetrack}")
    print(standardTrackTime)
    #print(path)

    # make all possible combinations of points on path
    possibleCombinations = []
    pathWithDistant = []
    for i in range(0, len(path)):
        pathWithDistant.append((path[i], i))
    #print(pathWithDistant)  
    possibleCombinations.extend(itertools.combinations(pathWithDistant, 2))
    
    print(len(possibleCombinations))

    shorterPaths = 0 
    shortestPathsMoreCheats = 0 
    for combination in possibleCombinations:
        p1 , p2 = combination
        originalDistance = p2[1] - p1[1]
        if originalDistance <= 0: 
            continue
        #manhatten distance
        distance = abs(p1[0][0] - p2[0][0]) + abs(p1[0][1] - p2[0][1])
        if distance < originalDistance and distance == 2 and originalDistance - distance >= 100:
            shorterPaths += 1
        if distance < originalDistance and distance < 21 and originalDistance - distance >= 100:
            shortestPathsMoreCheats += 1
    print(shorterPaths)
    print(shortestPathsMoreCheats)
    
    endtime = time.time()
    print("Time taken;" , endtime - starttime)  
    print("Time taken in ms;", (endtime - starttime) * 1000)    





def findShortestPath(start, finish, track):
    visited = set()
    q = deque([(start, [], 0)])
    while q:
        (x, y), path, distance = q.popleft()
        if (x, y) == finish:
            path = path + [(x, y)]  
            return distance, path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [ (1, 0), (0, 1), (-1, 0), (0, -1)]:
            if track.get((x + dx, y + dy)) != '#':
                q.append(((x + dx, y + dy), path + [(x, y)],distance + 1))
    return None
        

if __name__ == "__main__":
    main()