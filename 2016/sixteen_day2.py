import os
import time



# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/bathroomcode.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    instructions = []
    for line in lines:
        line = line.strip()
        instructions.append(line)

    directions = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}
    keypad = {(0,0):1, (1,0):2, (2,0):3, (0,1):4, (1,1):5, (2,1):6, (0,2):7, (1,2):8, (2,2):9}

    curNum  = (1,1)
    code = 0
    for instruction in instructions:
        
        for char in instruction:
            # print(curNum)
            # print(char)
            newNum = (curNum[0] + directions[char][0], curNum[1] + directions[char][1])
            #print(newNum)
            if newNum in keypad:
                curNum = newNum
        code = code*10 + keypad[curNum]
    print(code)
    endP1 = time.time()
    print("Part 1 time: ", endP1 - start_time)
    print("Part 1 in ms: ", (endP1 - start_time)*1000)  

    part2KeyPad = {(2,0):"1", (1,1):"2",(2,1):"3", (3,1):"4",
                   (0,2):"5", (1,2):"6", (2,2):"7", (3,2):"8", (4,2):"9",
                   (1,3):"A", (2,3):"B", (3,3):"C",
                   (2,4):"D"}
    curNum  = (0,2)
    code = ""
    for instruction in instructions:
        
        for char in instruction:
            # print(curNum)
            # print(char)
            newNum = (curNum[0] + directions[char][0], curNum[1] + directions[char][1])
            #print(newNum)
            if newNum in part2KeyPad:
                curNum = newNum
        code = code + part2KeyPad[curNum]
    print(code)



if __name__ == "__main__":
    main()
