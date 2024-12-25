import os
import time


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/locks.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()


    keys = {}
    locks = {}
    keyNumber = 0
    lockNumber = 0
    startOfLockKey = True
    for line in lines:
        if line.strip() == "":
            key = None
            lock = None
            startOfLockKey = True
            continue
        if startOfLockKey:
            key = line.strip().startswith(".")
            lock = line.strip().startswith("#")
            height = 1
            if key:
                keyNumber += 1
                keys[keyNumber] = [0,0,0,0,0]
            elif lock:
                lockNumber += 1
                locks[lockNumber] = [0,0,0,0,0]

            startOfLockKey = False
            continue
        else:
            #print(height)
            if height >= 6:
                continue
            if key:
                for i, char in enumerate(line.strip()):
                    if char == "#":
                        keys[keyNumber][i] += 1
            elif lock:
                for i, char in enumerate(line.strip()):
                    if char == "#":
                        locks[lockNumber][i] += 1
        height += 1
    maxSpace = 5
    #print(keys)
    #print(locks)

    uniqueFittingKeys = 0
    for key in keys:
        for lock in locks:
            fits = True
            for i in range(5):
                if keys[key][i] + locks[lock][i] > maxSpace:
                    fits = False
                    break
            if fits:
                uniqueFittingKeys += 1

    print(uniqueFittingKeys)     
    endTimeP1 = time.time()
    print("Part 1 took: ", endTimeP1 - start_time)
    print("Part 1 took in ms: ", (endTimeP1 - start_time) * 1000)
                    
                    
                    
if __name__ == "__main__":
    main()