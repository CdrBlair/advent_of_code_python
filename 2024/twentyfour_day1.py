import os
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/locationids.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:

        

        # Read line by line
        lines = file.readlines()
        leftlist = []
        rightlist = []
        for line in lines:
            line = line.strip()
            #split line by space and get the two numbers
            left, right = line.split("   ")
            leftlist.append(int(left))
            rightlist.append(int(right))
    

    # order from smalles to largest
    leftlist.sort()
    rightlist.sort()

    diff = [abs(left - right ) for left, right in zip(leftlist, rightlist)]



    # sum of diff
    print(sum(diff))
    endtime = time.time()
    print("Time part 1: ", endtime - start_time)
    print("Time part 1 in ms: ", (endtime - start_time) * 1000) 

    totalsum = 0
    for left in leftlist:
        count = rightlist.count(left)
        if count > 0:
            totalsum += count * left
    print(totalsum)




if __name__ == "__main__":
    main()