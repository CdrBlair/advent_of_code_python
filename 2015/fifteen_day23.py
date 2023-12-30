import os
import time
import re
from random import shuffle


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2015/instructionset.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    instructions = []
    for line in lines:
        line = line.strip()
        if not line.__contains__(","):
            line = line.split(" ")
            if line[0] == "jmp":
                instructions.append((line[0], "", int(line[1])))
            else:
                instructions.append((line[0], line[1],0))
        else:
            line = line.split(" ")
            instructions.append((line[0], line[1].replace(",",""), int(line[2])))

    #print(instructions)
    #P1 == 0 , P2 == 1  
    a = 1
    b = 0 
    currentInstruction = 0
    while currentInstruction < len(instructions):
        instruction = instructions[currentInstruction]
        if instruction[0] == "hlf":
            if instruction[1] == "a":
                a = a // 2
            else:
                b = b // 2
            currentInstruction += 1
        elif instruction[0] == "tpl":
            if instruction[1] == "a":
                a = a * 3
            else:
                b = b * 3
            currentInstruction += 1
        elif instruction[0] == "inc":
            if instruction[1] == "a":
                a += 1
            else:
                b += 1
            currentInstruction += 1
        elif instruction[0] == "jmp":
            currentInstruction += instruction[2]
        elif instruction[0] == "jie":
            if instruction[1] == "a":
                if a % 2 == 0:
                    currentInstruction += instruction[2]
                else:
                    currentInstruction += 1
            else:
                if b % 2 == 0:
                    currentInstruction += instruction[2]
                else:
                    currentInstruction += 1
        elif instruction[0] == "jio":
            if instruction[1] == "a":
                if a == 1:
                    currentInstruction += instruction[2]
                else:
                    currentInstruction += 1
            else:
                if b == 1:
                    currentInstruction += instruction[2]
                else:
                    currentInstruction += 1
        else:
            print("Error")
            break
    print(a)
    print(b)
    endTime = time.time()
    print("Time taken: ",endTime  - start_time)
    print("Time taken in ms: ", (endTime - start_time) * 1000)

if __name__ == "__main__":
    main()
