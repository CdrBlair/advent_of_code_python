import os
import time
import math
import sys


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/warehouse.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    boxpositions = set()
    warehouseMap = {}
    robotPos = None
    movements = ""
    readMap = False
    for y, line in enumerate(lines):
        if line.strip() == "":
            readMap = True
            continue
        if readMap:
            movements += line.strip()
        else:
            for x, char in enumerate(line.strip()):
                if char == "@":
                    robotPos = (x, y)
                elif char == "O":
                    boxpositions.add((x, y))
                warehouseMap[(x, y)] = char

    maxX = max([pos[0] for pos in warehouseMap.keys()])
    maxY = max([pos[1] for pos in warehouseMap.keys()])
    # print(warehouseMap)
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(warehouseMap[(x, y)], end="")
    #     print()

    for move in movements:
        moved, warehouseMap, robotPos, boxpositions = tryMovement(warehouseMap, robotPos, True, robotPos, move, boxpositions)
        
    # print(warehouseMap)
    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(warehouseMap[(x, y)], end="")
    #     print()

    gpssafety = 0
    for pos in boxpositions:
        gpssafety += 100*pos[1] + pos[0]   
    print(gpssafety) 
    endTimeP1 = time.time()
    print("Part 1 execution time: ", endTimeP1 - start_time)
    print("Part 1 execution time in ms: ", (endTimeP1 - start_time)*1000)

    warehouseMap = {}
    boxpositions = set()
    for y,line in enumerate(lines):
        x = 0 
        if line.strip() == "":
            break
        for char in line.strip():
            if char == "@":
                robotPos = (x, y)
                warehouseMap[(x, y)] = "@"
                warehouseMap[(x+1,y)] = "."
            elif char == "O":
                boxpositions.add((x, y))
                warehouseMap[(x, y)] = "["
                warehouseMap[(x+1,y)] = "]"
            elif char == "#":
                warehouseMap[(x, y)] = "#"
                warehouseMap[(x+1,y)] = "#"
            elif char == ".":
                warehouseMap[(x, y)] = "."
                warehouseMap[(x+1,y)] = "."
            x += 2
    maxX = max([pos[0] for pos in warehouseMap.keys()])
    maxY = max([pos[1] for pos in warehouseMap.keys()])

    # for y in range(maxY + 1):
    #     for x in range(maxX + 1):
    #         print(warehouseMap[(x, y)], end="")
    #     print()

    for move in movements:
        moved, warehouseMap, robotPos, boxpositions = tryMovementNew(warehouseMap, robotPos, True, robotPos, move, boxpositions)
    
    # print map with coordinates
        # for y in range(maxY + 1):
        #     for x in range(maxX + 1):
        #         print(warehouseMap[(x, y)], end="")
        #     print()

    newGpsSafety = 0

    for pos in boxpositions:
        newGpsSafety += 100*pos[1] + pos[0]
    print(newGpsSafety)
    endTimeP2 = time.time()
    print("Part 2 execution time: ", endTimeP2 - endTimeP1)
    print("Part 2 execution time in ms: ", (endTimeP2 - endTimeP1)*1000)
    

def tryMovement(warehouseMap, pos, robot, robotPosition, direction, boxPositions):
    if direction == "^":
        newPos = (pos[0], pos[1] - 1)
    elif direction == "v":
        newPos = (pos[0], pos[1] + 1)
    elif direction == "<":
        newPos = (pos[0] - 1, pos[1])
    elif direction == ">":
        newPos = (pos[0] + 1, pos[1])
    
    if warehouseMap[newPos] == "#":
        return False, warehouseMap, robotPosition, boxPositions
    elif warehouseMap[newPos] == ".": # Empty space
        if robot:
            robotPosition = newPos
            warehouseMap[newPos] = "@"
        else:
            boxPositions.remove(pos)
            boxPositions.add(newPos)
            warehouseMap[newPos] = "O"
        warehouseMap[pos] = "."
        return True, warehouseMap, robotPosition, boxPositions
    elif warehouseMap[newPos] == "O": # Box
        moved, warehouseMap, robotPosition, boxPositions = tryMovement(warehouseMap, newPos, False, robotPosition, direction, boxPositions)
        if not moved:
            return False, warehouseMap, robotPosition, boxPositions
        else:
            if robot:
                robotPosition = newPos
                warehouseMap[newPos] = "@"
            else:
                boxPositions.remove(pos)
                boxPositions.add(newPos)
                warehouseMap[newPos] = "O"
            warehouseMap[pos] = "."
            return True, warehouseMap, robotPosition, boxPositions
        
def tryMovementNew(warehouseMapIn, pos, robot, robotPosition, direction, boxPositionsIn):
    warehouseMap = warehouseMapIn.copy()
    boxPositions = boxPositionsIn.copy()

    if direction == "^":
        newPos = (pos[0], pos[1] - 1)
    elif direction == "v":
        newPos = (pos[0], pos[1] + 1)
    elif direction == "<":
        newPos = (pos[0] - 1, pos[1])
    elif direction == ">":
        newPos = (pos[0] + 1, pos[1])
    selfkind = warehouseMap[pos]
    if not robot :
        if selfkind == "[":
            secondhalf = (pos[0] + 1, pos[1])
            secondhalfNew = (newPos[0] + 1, newPos[1])
            secondhalfkind = "]"
        else: 
            secondhalf = (pos[0] - 1, pos[1])
            secondhalfNew = (newPos[0] - 1, newPos[1])
            secondhalfkind = "["
    
    if warehouseMap[newPos] == "#":
        return False, warehouseMap, robotPosition, boxPositions
    elif warehouseMap[newPos] == ".": # Empty space
        if robot:
            robotPosition = newPos
            warehouseMap[newPos] = "@"
            warehouseMap[pos] = "."
            return True, warehouseMap, robotPosition, boxPositions
        elif direction == ">" or direction == "<":
            warehouseMap[newPos] = selfkind
            warehouseMap[pos] = "."
            if selfkind == "[":
                boxPositions.remove(pos)
                boxPositions.add(newPos)
            return True, warehouseMap, robotPosition, boxPositions
        else:
            if warehouseMap[secondhalfNew] == ".":
                warehouseMap[secondhalfNew] = secondhalfkind
                warehouseMap[secondhalf] = "."
                warehouseMap[newPos] = selfkind
                warehouseMap[pos] = "."
                if selfkind == "[":
                    boxPositions.remove(pos)
                    boxPositions.add(newPos)
                else:
                    boxPositions.remove(secondhalf)
                    boxPositions.add(secondhalfNew)
                return True, warehouseMap, robotPosition, boxPositions
            elif warehouseMap[secondhalfNew] == "#":
                return False, warehouseMap, robotPosition, boxPositions
            else:
                #print("current pos", pos, "secondhalf", secondhalfNew)
                moved, warehouseMap, robotPosition, boxPositions = tryMovementNew(warehouseMap, secondhalfNew, False, robotPosition, direction, boxPositions)
                if not moved:
                    return False, warehouseMap, robotPosition, boxPositions
                else:
                    
                    warehouseMap[newPos] = selfkind
                    warehouseMap[pos] = "."
                    warehouseMap[secondhalfNew] = secondhalfkind   
                    warehouseMap[secondhalf] = "."
                    if selfkind == "[":
                        boxPositions.remove(pos)
                        boxPositions.add(newPos)
                    else:
                        boxPositions.remove(secondhalf)
                        boxPositions.add(secondhalfNew)
                    return True, warehouseMap, robotPosition, boxPositions
    else:
        if direction == ">" or direction == "<":
            moved, warehouseMap, robotPosition, boxPositions = tryMovementNew(warehouseMap, newPos, False, robotPosition, direction, boxPositions)
            if not moved:
                return False, warehouseMap, robotPosition, boxPositions
            else:
                if robot:
                    robotPosition = newPos
                    warehouseMap[newPos] = "@"
                else:
                    if selfkind == "[":
                        boxPositions.remove(pos)
                        boxPositions.add(newPos)
                    warehouseMap[newPos] = selfkind
                warehouseMap[pos] = "."
                return True, warehouseMap, robotPosition, boxPositions
        else:
            movedSelf, warehouseMapSelf, robotPositionSelf, boxPositionsSelf = tryMovementNew(warehouseMap, newPos, False, robotPosition, direction, boxPositions)
            if not movedSelf:
                return False, warehouseMap, robotPosition, boxPositions
            elif not robot:
                if warehouseMapSelf[secondhalfNew] == ".":
                    warehouseMapSelf[secondhalfNew] = secondhalfkind
                    warehouseMapSelf[secondhalf] = "."
                    warehouseMap = warehouseMapSelf
                    boxPositions = boxPositionsSelf
                   
                    if selfkind == "[":
                        boxPositions.remove(pos)
                        boxPositions.add(newPos)
                    else:
                        boxPositions.remove(secondhalf)
                        boxPositions.add(secondhalfNew)
                    warehouseMap[newPos] = selfkind
                    warehouseMap[pos] = "."
                    return True, warehouseMap, robotPosition, boxPositions
                elif warehouseMapSelf[secondhalfNew] == "#":
                    return False, warehouseMap, robotPosition, boxPositions
                else:
                    movedSecond, warehouseMapSecond, robotPositionSecond, boxPositionsSecond = tryMovementNew(warehouseMapSelf, secondhalfNew, False, robotPositionSelf, direction, boxPositionsSelf)
                
                    if not movedSecond:
                        return False, warehouseMap, robotPosition, boxPositions
                    else:
                        warehouseMap = warehouseMapSecond
                        boxPositions = boxPositionsSecond
                        if selfkind == "[":
                            boxPositions.remove(pos)
                            boxPositions.add(newPos)
                        else:
                            boxPositions.remove(secondhalf)
                            boxPositions.add(secondhalfNew)
                        warehouseMap[newPos] = selfkind
                        warehouseMap[secondhalfNew] = secondhalfkind
                        warehouseMap[secondhalf] = "."
                        warehouseMap[pos] = "."
                        return True, warehouseMap, robotPosition, boxPositions
            else: 
                warehouseMap = warehouseMapSelf
                boxPositions = boxPositionsSelf
                robotPosition = newPos
                warehouseMap[newPos] = "@"
                warehouseMap[pos] = "."
                return True, warehouseMap, robotPosition, boxPositions

   


           


if __name__ == "__main__":
    main()
    