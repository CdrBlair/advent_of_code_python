import os
import time


def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/3bit.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    regA = 0
    regB = 0
    regC = 0
    program = []

    readRegs = False
    for line in lines:
        if line.strip() == "":
            readRegs = True
            continue
        if not readRegs:
            reg, value = line.strip().split(":")
            if "A" in reg:
                regA = int(value.strip())
            if "B" in reg:
                regB = int(value.strip())
            if "C" in reg:
                regC = int(value.strip())
        else:
            _, values = line.strip().split(":")
            programString = values.strip()
            values = values.strip().split(",")
            for value in values:
                program.append(int(value.strip()))
    regAp2, regBp2, regCp2 = regA, regB, regC
    print(regA, regB, regC)
    print(program)
    i = 0
    output = ""
    # while i is valid index
    while i < len(program):
        # print(i)
        instr = program[i]
        value = program[i + 1]
        if instr == 0:
            regA = int(regA / (2 ** getComboOperand(value, regA, regB, regC)))
        if instr == 1:
            regB = regB ^ value
        if instr == 2:
            regB = getComboOperand(value, regA, regB, regC) % 8
        if instr == 3:
            if not regA == 0:
                i = value
                continue
        if instr == 4:
            regB = regB ^ regC
        if instr == 5:
            if not output == "":
                output += ","
            output += str(getComboOperand(value, regA, regB, regC) % 8)
        if instr == 6:
            regB = int(regA / (2 ** getComboOperand(value, regA, regB, regC)))
        if instr == 7:
            regC = int(regA / (2 ** getComboOperand(value, regA, regB, regC)))
        i += 2
    print(output)
    endTime = time.time()
    print("Part 1 took", endTime - starttime)
    print("Part 1 took in ms:", (endTime - starttime) * 1000)

    initRegA = 0
    while not output == programString:
        regB, regC = regBp2, regCp2
        output = ""
        i = 0
        regA = initRegA
        # print("cur Reg A", regA)

        while i < len(program):
            # print(i)
            instr = program[i]
            value = program[i + 1]
            if instr == 0:
                regA = int(regA / (2 ** getComboOperand(value, regA, regB, regC)))
            if instr == 1:
                regB = regB ^ value
            if instr == 2:
                regB = getComboOperand(value, regA, regB, regC) % 8
            if instr == 3:
                if not regA == 0:
                    i = value
                    continue
            if instr == 4:
                regB = regB ^ regC
            if instr == 5:
                if not output == "":
                    output += ","
                output += str(getComboOperand(value, regA, regB, regC) % 8)
            if instr == 6:
                regB = int(regA / (2 ** getComboOperand(value, regA, regB, regC)))
            if instr == 7:
                regC = int(regA / (2 ** getComboOperand(value, regA, regB, regC)))
            i += 2
        if programString == output:
            print(initRegA)
            break
        if programString.endswith(output):
            initRegA *= 8
        else:
            initRegA += 1
        # print(output)
    endTimeP2 = time.time()
    print("Part 2 took:", endTimeP2 - endTime)
    print("Part 2 took in ms: ", (endTimeP2 - endTime) * 1000)


def getComboOperand(value, regA, regB, regC):
    if value in [0, 1, 2, 3]:
        return value
    if value == 4:
        return regA
    if value == 5:
        return regB
    if value == 6:
        return regC
    if value == 7:
        return None
    return None


if __name__ == "__main__":
    main()
