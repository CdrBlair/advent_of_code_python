import os
import time
import math
from random import shuffle


# Main method
def main():
    start_time = time.time()
    # Open file
   
    weapons = []
    armor = []
    rings = []
    weapons.append((8,4,0))
    weapons.append((10,5,0))
    weapons.append((25,6,0))
    weapons.append((40,7,0))
    weapons.append((74,8,0))

    armor.append((0,0,0))
    armor.append((13,0,1))
    armor.append((31,0,2))
    armor.append((53,0,3))
    armor.append((75,0,4))
    armor.append((102,0,5))

    rings.append((0,0,0))
    rings.append((25,1,0))
    rings.append((50,2,0))
    rings.append((100,3,0))
    rings.append((20,0,1))
    rings.append((40,0,2))
    rings.append((80,0,3))

    gearCombos = []
    for weapon in weapons:
        for arm in armor:
            for ring1 in rings:
                for ring2 in rings:
                    if ring1 == ring2 and ring1 != (0,0,0):
                        continue
                    combinedGear = (weapon[0] + arm[0] + ring1[0] + ring2[0], weapon[1] + arm[1] + ring1[1] + ring2[1], weapon[2] + arm[2] + ring1[2] + ring2[2])
                    gearCombos.append(combinedGear)
    gearCombos.sort()
    #print(gearCombos)


    player = (100,0,0)
    boss = (103,9,2)
        
    
    for gear in gearCombos:
        playerDamagePR = gear[1] - boss[2]
        if playerDamagePR < 1:
            playerDamagePR = 1
        bossDamagePR = boss[1] - gear[2]
        if bossDamagePR < 1:
            bossDamagePR = 1
        playerTurns = boss[0] / playerDamagePR
        bossTurns = player[0] / bossDamagePR
        playerTurns =  math.ceil(playerTurns)
        bossTurns = math.ceil(bossTurns)
        #print(playerTurns, bossTurns)
        if playerTurns <= bossTurns:
            print(gear)
            break
    endTimeP1 = time.time()
    print("Part 1 time: ", endTimeP1 - start_time)
    print("Part 1 time in ms: ", (endTimeP1 - start_time) * 1000)
    player = (100,0,0)
    boss = (103,9,2)
    loses = []
        
    
    for gear in gearCombos:
        playerDamagePR = gear[1] - boss[2]
        if playerDamagePR < 1:
            playerDamagePR = 1
        bossDamagePR = boss[1] - gear[2]
        if bossDamagePR < 1:
            bossDamagePR = 1
        playerTurns = boss[0] / playerDamagePR
        bossTurns = player[0] / bossDamagePR
        playerTurns =  math.ceil(playerTurns)
        bossTurns = math.ceil(bossTurns)
        #print(playerTurns, bossTurns)
        if playerTurns > bossTurns:
            loses.append(gear)
            
    loses.sort(reverse=True)
    print(loses[0])
    endTimeP2 = time.time()
    print("Part 2 time: ", endTimeP2 - endTimeP1)
    print("Part 2 time in ms: ", (endTimeP2 - endTimeP1) * 1000)
    print("Total time: ", endTimeP2 - start_time)
    print("Total time in ms: ", (endTimeP2 - start_time) * 1000 )

    


if __name__ == "__main__":
    main()
