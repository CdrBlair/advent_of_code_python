from collections import deque
import os
import time



# Main method
def main():
    start_time = time.time()
    boss = (58,9,0)
    player = (50,0,0,500)

    spells = []
    spells.append(("M",53,4,0,0,0,False,0))
    spells.append(("D",73,2,2,0,0,False,0))
    spells.append(("S",113,0,0,7,0,True,6))
    spells.append(("P",173,3,0,0,0,True,6))
    spells.append(("R",229,0,0,0,101,True,5))


    stack= deque([("R",229,player, boss,False,0,False,0,False,0)])
    stack.append(("P",173,player, boss,False,0,False,0,False,0))
    stack.append(("S",113,player, boss,False,0,False,0,False,0))
    stack.append(("D",73,player, boss,False,0,False,0,False,0))
    stack.append(("M",53,player, boss,False,0,False,0,False,0))
    
    visited = set()
    bossDefeats = []
    while stack:
        
        spell, manaSpent, player, boss, shield,shieldCounter, poison,poisonCounter, recharge,rechargeCounter = stack.popleft()
        if (spell, player, boss, shield,shieldCounter, poison,poisonCounter, recharge,rechargeCounter) in visited:
       
            continue
       
        visited.add((spell, player, boss, shield,shieldCounter, poison,poisonCounter, recharge,rechargeCounter))
        #Players turn
        # part 2 modification
        player = (player[0]-1, player[1], player[2], player[3])
        if player[0] <= 0:
            #print("You died")
            continue
        if poison:
            boss = (boss[0]-3, boss[1], boss[2])
            poisonCounter -= 1
            if poisonCounter == 0:
                poison = False
        if recharge:
            player = (player[0], player[1], player[2], player[3]+101)
            rechargeCounter -= 1
            if rechargeCounter == 0:
                recharge = False
        if shield:
            player = (player[0], player[1], 7, player[3])
            shieldCounter -= 1
            if shieldCounter == 0:
                shield = False
        else:
            player = (player[0], player[1], 0, player[3])
        
        if boss[0] <= 0:
            bossDefeats.append(manaSpent)
            continue
        
        if spell == "M":
            boss = (boss[0]-4, boss[1], boss[2])
            player = (player[0], player[1], player[2], player[3]-53)
        elif spell == "D":
            boss = (boss[0]-2, boss[1], boss[2])
            player = (player[0]+2, player[1], player[2], player[3]-73)
        elif spell == "S":
            shield = True
            shieldCounter = 6
            player = (player[0], player[1], player[2], player[3]-113)
        elif spell == "P":
            poison = True
            poisonCounter = 6
            player = (player[0], player[1], player[2], player[3]-173)
        elif spell == "R":
            recharge = True
            rechargeCounter = 5
            player = (player[0], player[1], player[2], player[3]-229)
        

        if boss[0] <= 0:
            bossDefeats.append(manaSpent)
            continue
        
        #Boss turn
        if poison:
            boss = (boss[0]-3, boss[1], boss[2])
            poisonCounter -= 1
            if poisonCounter == 0:
                poison = False
        if recharge:
            player = (player[0], player[1], player[2], player[3]+101)
            rechargeCounter -= 1
            if rechargeCounter == 0:
                recharge = False
        if shield:
            player = (player[0], player[1], 7, player[3])
            shieldCounter -= 1
            if shieldCounter == 0:
                shield = False
        else:
            player = (player[0], player[1], 0, player[3])
        if boss[0] <= 0:
            bossDefeats.append(manaSpent)
            continue
            

        player = (player[0]-max(1, boss[1]-player[2]), player[1], player[2], player[3])        
        # print(player)
        # print(boss)
        
        if player[0] <= 0:
            #print("You died")
            continue

        
        for spell in spells:
            if spell[1] > player[3]:
                continue
            if spell[0] == "S" and shield and shieldCounter > 1:
                continue
            if spell[0] == "P" and poison and poisonCounter > 1:
                continue
            if spell[0] == "R" and recharge and rechargeCounter > 1:
                continue
            stack.append((spell[0], manaSpent+spell[1], player, boss, shield,shieldCounter, poison,poisonCounter, recharge,rechargeCounter))
    #print(bossDefeats)
    print(min(bossDefeats))
    endTimeP1 = time.time()
    print("Part 1 time: ", endTimeP1 - start_time)
    print("Part 1 time in ms: ", (endTimeP1 - start_time) * 1000)


if __name__ == "__main__":
    main()