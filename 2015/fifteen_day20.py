

import time
import math



def main():
    startTime = time.time()
    minPresents = 34000000
    house = {}
    

   
    for i in range(1, int(minPresents/10)):
    
        for j in range(i,int(minPresents/10), i):
            if j not in house:
                house[j] = 0

            house[j] += i*10
    
    sorted_dict = dict(sorted(house.items()))
    print(sorted_dict[1])
    for key in sorted_dict:
        if sorted_dict[key] >= minPresents:
            print(key)
            break

    endTimeP1 = time.time()
    print("Time Part 1: ", endTimeP1 - startTime)
    print("Time P1 in ms: ", (endTimeP1 - startTime)*1000)

    minPresents = 34000000
    house = {}
    

   
    for i in range(1, int(minPresents/10)):
        visitedHouse = 0 
        for j in range(i,int(minPresents/10), i):
            if visitedHouse == 50:
                break
            if j not in house:
                house[j] = 0

            house[j] += i*11
            visitedHouse += 1
    
    sorted_dict = dict(sorted(house.items()))
    print(sorted_dict[1])
    for key in sorted_dict:
        if sorted_dict[key] >= minPresents:
            print(key)
            break

    print("Time Part 2: ", time.time() - endTimeP1)
    print("Time P2 in ms: ", (time.time() - endTimeP1)*1000)
    print("Time Total: ", time.time() - startTime)
    print("Time Total in ms: ", (time.time() - startTime)*1000)

    
            
            


   

if __name__ == "__main__":
    main()