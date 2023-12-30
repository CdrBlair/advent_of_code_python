import os
import time



# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/bunnyhqdir.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
    
    bunnyDir = []
    for line in lines:
        line = line.strip()
        directions = line.split(", ")
        for direction in directions:
            bunnyDir.append((direction[0], int(direction[1:])))

    curDir = (0,-1)
    curPos = (0,0)
    for turn in bunnyDir:
        curDir = getNewDirection(curDir, turn[0])
        curPos = (curPos[0] + curDir[0]*turn[1], curPos[1] + curDir[1]*turn[1])

    print(curPos)
    print(abs(curPos[0]) + abs(curPos[1]))
    endTimePart1 = time.time()
    print("Part 1 time: ", endTimePart1 - start_time)
    print("Time P1 in ms: ", (endTimePart1 - start_time)*1000)

    curDir = (0,-1)
    curPos = (0,0)
    visitedPos = set()
    visitedPos.add(curPos)
    found = False
    for turn in bunnyDir:
        newDir = getNewDirection(curDir, turn[0])
        for i in range(1, turn[1]+1):            
            pos = (curPos[0] + newDir[0]*i, curPos[1] + newDir[1]*i)
            if pos in visitedPos:
                print(pos)
                print(abs(pos[0]) + abs(pos[1]))
                found = True
                break
            else:
                visitedPos.add(pos)
        if found:
            break
        curDir = newDir
        curPos = pos


def getNewDirection(curDir, turn):
    if turn == "R":
        if curDir == (0,-1):
            return (1,0)
        elif curDir == (1,0):
            return (0,1)
        elif curDir == (0,1):
            return (-1,0)
        elif curDir == (-1,0):
            return (0,-1)
    elif turn == "L":
        if curDir == (0,-1):
            return (-1,0)
        elif curDir == (-1,0):
            return (0,1)
        elif curDir == (0,1):
            return (1,0)
        elif curDir == (1,0):
            return (0,-1)
        
if __name__ == "__main__":
    main()