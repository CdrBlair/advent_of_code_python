import os
import re
import time
from calendar import c
from hmac import new


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/corruptedmemory.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    reports = []
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
    mulPattern = r"mul\(\d{1,3},\d{1,3}\)"

    correctInstructions = []
    for line in lines:
        lineInst = re.findall(mulPattern, line)
        correctInstructions.extend(lineInst)

    sum = 0
    for instruction in correctInstructions:
        numPattern = r"\d{1,3},\d{1,3}"
        nums = re.findall(numPattern, instruction)
        x, y = nums[0].split(",")
        sum += int(x) * int(y)
    print(sum)

    endtime = time.time()
    print("Time part 1: ", endtime - start_time)
    print("Time part 1 in ms: ", (endtime - start_time) * 1000)

    # part 2
    newInstructions = []
    newSum = 0
    # concat all lines
    finalline = "".join(lines)
    lines = [finalline]
    dontPattern = r"don't\(\)"
    dont = "don't()"
    firstPart, secondPart = re.split(dontPattern, finalline, maxsplit=1)
    firsInst = re.findall(mulPattern, firstPart)
    newInstructions.extend(firsInst)
    secondPart = dont + secondPart
    rest = "X"
    while not rest == "":

        eval, secondPart = instSplitter(secondPart)
        if eval != "":
            addInst = re.findall(mulPattern, eval)
            newInstructions.extend(addInst)
        rest = secondPart

    for instruction in newInstructions:
        numPattern = r"\d{1,3},\d{1,3}"
        nums = re.findall(numPattern, instruction)
        x, y = nums[0].split(",")
        newSum += int(x) * int(y)

    print(newSum)
    endtime = time.time()
    print("Time part 2: ", endtime - start_time)
    print("Time part 2 in ms: ", (endtime - start_time) * 1000)


def instSplitter(inst):
    dontPattern = r"don't\(\)"
    dont = "don't()"
    doPattern = r"do\(\)"
    do = "do()"
    # Starts with dont?
    if re.match(dontPattern, inst):
        if re.search(doPattern, inst):
            ignore, rest = re.split(doPattern, inst, maxsplit=1)
            rest = do + rest
            return "", rest
        return "", ""
    else:  # Starts with do
        if re.search(dontPattern, inst):
            eval, rest = re.split(dontPattern, inst, maxsplit=1)
            rest = dont + rest
            return eval, rest
        return inst, ""


if __name__ == "__main__":
    main()
