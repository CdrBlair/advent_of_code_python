import os
import time
from functools import lru_cache
import math
import itertools



def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/monkey_secrets.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()


    startsecrets = []
    for line in lines:
        startsecrets.append(int(line.strip()))

   
    finalSecrets = {}
    changes = {}
    for secret in startsecrets:
        start = secret
        changes[secret] = [(secret%10,None)]

        for i in range(2000):

            firststep = firstStep(start)
            secondstep = secondStep(firststep)
            thirdstep = thirdStep(secondstep)
            start = thirdstep
            tsmodulo = thirdstep%10
            change = tsmodulo- changes[secret][-1][0]
            changes[secret].append((tsmodulo,change))
        
        finalSecrets[secret] = thirdstep
    
    #print(finalSecrets)
    #print cache_info()
    print(firstStep.cache_info())
    sumOfSecrets = sum(finalSecrets.values())
    print(sumOfSecrets)
    endTimeP1 = time.time()
    print("Part 1 took: ", endTimeP1-starttime)
    print("Part 1 took in ms: ", (endTimeP1-starttime)*1000)
    
    digits = list(range(-9,10))
    permutations = list(itertools.product(digits, repeat=4))
    print(len(permutations))

    bananas = 0 
    highest = 0
    bestsequence= ''
    i = 0 


    possibleSequences = set()
    for change in changes:
        for i in range(1,1997):
            possibleSequences.add(''.join(str(x[1]) for x in changes[change][i:i+4]))
    print(len(possibleSequences))



    # testString = '1-351'
    # testChange = ''.join(str(x[1]) for x in changes[1])
    # testIndex = 0
    # while testIndex != -1:
    #     testIndex = testChange.find(testString, testIndex)
    #     if testIndex == -1:
    #         break
    #     if testIndex == 0 or testChange[testIndex-1] != '-':
    #         break
    #     testIndex += 1
    
    # print('TI: ',testIndex)
    # print(testChange[:testIndex+len(testString)])
    # minusCounts = testChange[:testIndex+len(testString)].count('-')
    # testpriceIndex = testIndex+ len(testString) - minusCounts- 3-1
    # testPrice = changes[1][testpriceIndex][0]
    # print(testpriceIndex)
    # print('TP',testPrice)

    # for index in range(0, 30):
    #     print(changes[8614704][index])
    changesAsStrings = {}
    for secret in changes:
        changeAsString = ''.join(str(x[1]) for x in changes[secret])
        changesAsStrings[secret] = changeAsString


    i = 0
    for perm in possibleSequences:
        #timeperm = time.time()
        print(i)
        i+=1
        premString = ''.join(str(x) for x in perm)
        currentBananas = 0
        for secret in changes:
            changeAsString = changesAsStrings[secret]
            permIndex = 0
            while permIndex != -1:
                permIndex = changeAsString.find(premString, permIndex)
                if permIndex == -1:
                    break
                if permIndex == 0 or changeAsString[permIndex-1] != '-':
                    break
                permIndex += 1
            if permIndex == -1:
                continue

            #find number of '-' until end of perm
            minusCounts = changeAsString[:permIndex+len(premString)].count('-')
            #get index after perm
            priceIndex = permIndex + len(premString) - minusCounts- 3-1
            #get price
            if priceIndex < 0 or priceIndex >= len(changes[secret]):
                continue
            price = changes[secret][priceIndex][0]
            currentBananas += price
        if currentBananas >  highest:
            highest = currentBananas
            bestsequence = premString
        #print((time.time()-timeperm)*1000)
        

    
        
    print(highest)
    print(bestsequence)
        

        
            










@lru_cache(maxsize=None)
def firstStep(secret): 
    return ((secret*64)^secret)%16777216
@lru_cache(maxsize=None)
def secondStep(secret):
    return (math.floor(secret/32) ^ secret) % 16777216
@lru_cache(maxsize=None)
def thirdStep(secret):
    return ((secret*2048)^secret)%16777216

if __name__ == "__main__":
    main()