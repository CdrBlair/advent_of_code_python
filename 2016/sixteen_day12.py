import os
import time


def main():
    start_time = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/code_monorail.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        instructions = []
        for line in lines:
            instructions.append(line.strip())

    registers = {"a": 0, "b": 0, "c": 1, "d": 0}

    curPos = 0
    while curPos < len(instructions):
        curIns = instructions[curPos]
        com, x, y = (curIns.split(" ") + [None])[:3]
        if com == "cpy":
            ## check if x is a number or a register
            if not x.isnumeric():
                x = registers[x]
            registers[y] = int(x)
        elif com == "inc":
            registers[x] += 1
        elif com == "dec":
            registers[x] -= 1
        elif com == "jnz":
            ## check if x is a number or a register
            if not x.isnumeric():
                x = registers[x]
            if int(x) != 0:
                curPos += int(y) - 1
        curPos += 1

    print("Registers after execution: ", registers)
    endtime = time.time()
    print("Time part 1: ", endtime - start_time)
    print("Time part 1 in ms: ", (endtime - start_time) * 1000)


if __name__ == "__main__":
    main()
