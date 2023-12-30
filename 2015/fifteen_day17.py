import os
import time
import itertools


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2015/eggnogg_containers.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    containers = []
    for line in lines:
        containers.append(int(line.strip()))

    containerCombinations = []
    for i in range(1,len(containers)+1):
        containerCombinations.extend(itertools.combinations(containers, i))

    

    nrOfCombinations = 0
    minCombinationSize = min([len(combination) for combination in containerCombinations if sum(combination) == 150])
    print(minCombinationSize)
    for combination in containerCombinations:
        if sum(combination) == 150 and len(combination) == minCombinationSize:
            nrOfCombinations += 1
    
    print(nrOfCombinations)

    end_time = time.time()
    print("Time: ", end_time - start_time, "seconds")
    print("Time in ms: ", (end_time - start_time)*1000, "ms")
        

if __name__ == "__main__":
    main()

    