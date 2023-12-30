import os
import time
import itertools
from math import prod

# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2015/packages.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
    packages = []
    for line in lines:
        packages.append(int(line.strip()))
    totalWeight = sum(packages)
    # modify for parts: 3 or 4
    groupWeight = totalWeight // 4

    possibleCombinations = []
    found = False
    #modify for parts: 3 or 4
    for i in range(1, len(packages)-4):
        pos = itertools.combinations(packages, i)
        print(pos.__sizeof__())
        for group1 in pos:
            if sum(group1) == groupWeight:
                possibleCombinations.append((group1, prod(group1)))
                found = True
        if found:
            break
                            
    #print(possibleCombinations)
    possibleCombinations.sort(key=lambda x: (len(x[0]), x[1]))
    # for combination in possibleCombinations:
    #     print(combination)
    print(possibleCombinations[0])


if __name__ == "__main__":
    main()                                        