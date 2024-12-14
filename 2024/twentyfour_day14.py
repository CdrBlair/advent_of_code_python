import os
import time
import math


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/easterrobots.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    maxX = 101
    maxY = 103

    midY = maxY // 2
    midX = maxX // 2

    robots = []
    # ((cpx, cpy), (vx, vy))
    for line in lines: 
        start, speed = line.strip().split(" ")
        startnumber = start.split("=")[1]
        position = (int(startnumber.split(",")[0]), int(startnumber.split(",")[1]))
        speednumber = speed.split("=")[1]
        speed = (int(speednumber.split(",")[0]), int(speednumber.split(",")[1]))
        robots.append((position, speed))
    #print(robots)
    print("number of robots: ", len(robots))    

    # print a map
    # for i in range(maxY):
    #     for j in range(maxX):
    #         if (j, i) in [x[0] for x in robots]:
    #             print("R", end="")
    #         else:
    #             print(".", end="")
    #     print()
    robotsp2 = robots.copy()
    seconds = 100
    for s in range(seconds):
        robots = [moveRobot(x) for x in robots]
        # print(robots)
        #print a map
        #print(s)#
    
    
    # # print a map
    # for i in range(maxY):
    #     for j in range(maxX):
    #         if (j, i) in [x[0] for x in robots]:
    #             print("R", end="")
    #         else:
    #             print(".", end="")
    #     print()
    robotsLocations = {}
    for robot in robots:
        if robot[0] in robotsLocations:
            robotsLocations[robot[0]] += 1
        else:
            robotsLocations[robot[0]] = 1
        
    # count by quadrants
    quadrants = {}
    for location in robotsLocations:
        x, y = location
        if x < midX and y < midY:
            if "1" in quadrants:
                quadrants["1"] += robotsLocations[location]
            else:
                quadrants["1"] = robotsLocations[location]
        elif x > midX and y < midY:
            if "2" in quadrants:
                quadrants["2"] += robotsLocations[location]
            else:
                quadrants["2"] = robotsLocations[location]
        elif x < midX and y > midY:
            if "3" in quadrants:
                quadrants["3"] += robotsLocations[location]
            else:
                quadrants["3"] = robotsLocations[location]
        elif x > midX and y > midY:
            if "4" in quadrants:
                quadrants["4"] += robotsLocations[location]
            else:
                quadrants["4"] = robotsLocations[location]
    #print(quadrants)
    safetyfactor = math.prod([x for x in quadrants.values()])
    #print a map
    # for i in range(maxY):
    #     for j in range(maxX):
    #         if (j, i) in [x[0] for x in robots]:
    #             print("R", end="")
    #         else:
    #             print(".", end="")
    #     print()
    print(safetyfactor)
    endtimep1 = time.time()
    print("Part 1 took: ", endtimep1 - start_time)
    print("Part 1 took in ms: ", (endtimep1 - start_time) * 1000)

    

    s = 0 
    
    unique = False
    while not unique:
        s += 1
        robotsp2 = [moveRobot(x) for x in robotsp2]
        robotsposition = set([x[0] for x in robotsp2])
        #print(len(robotsp2), len(robotsposition))
        if len(robotsp2) == len(robotsposition):
            unique = True
    
    #     robots = [moveRobot(x) for x in robots]
        
    print(s)
    endtimep2 = time.time()
    print("Part 2 took: ", endtimep2 - endtimep1)
    print("Part 2 took in ms: ", (endtimep2 - endtimep1) * 1000)
    #print a map
    # for i in range(maxY):
    #     for j in range(maxX):
    #         if (j, i) in [x[0] for x in robotsp2]:
    #             print("R", end="")
    #         else:
    #             print(".", end="")
    #     print()    

    

def moveRobot(robot):
    maxX = 101
    maxY = 103
    (cpx, cpy), (vx, vy) = robot
    newX = cpx + vx
    newY = cpy + vy
    if newX < 0:
        newX = maxX + newX 
    if newX >= maxX:
        newX = newX - maxX
    if newY < 0:
        newY = maxY + newY
    if newY >= maxY:
        newY = newY - maxY
    return ((newX, newY), (vx, vy))



if __name__ == "__main__":
    main()
