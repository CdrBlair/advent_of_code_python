import os
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/pageset.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    instructions = {}
    updates = []
    eoinst = False
    for line in lines:
        if not eoinst:
            if line.strip() == "":
                eoinst = True
            else:
                instr = line.strip().split("|")
                key = int(instr[1])
                value = int(instr[0])
                if key in instructions:
                    instructions[key].append(value)
                else:
                    instructions[key] = [value]
        else:
            updates.append([int(x) for x in line.strip().split(",")])

    # print(instructions)
    # print(updates)

    violation = False
    goodUpdate = []
    badUpdate = []
    for update in updates:
        # print(update)
        for inst in instructions:
            # print(inst)
            if inst not in update:
                continue
            index = update.index(inst)
            right = update[index + 1 :]
            # print(left)
            # print(instructions[inst])
            if any(x in right for x in instructions[inst]):
                # print("Violation")
                violation = True
                badUpdate.append(update)
                break
        if not violation:
            goodUpdate.append(update)
        else:
            violation = False

    # print(goodUpdate)
    sumofmiddles = sum([x[len(x) // 2] for x in goodUpdate])
    print(sumofmiddles)
    endtime = time.time()
    print("Time taken: ", endtime - start_time)
    print("Time taken in ms: ", (endtime - start_time) * 1000)

    correctedUpdate = []
    for update in badUpdate:
        corected = update
        for inst in instructions:
            if inst not in corected:
                continue
            index = corected.index(inst)
            left = corected[:index]
            right = corected[index + 1 :]
            for i in right:
                if i in instructions[inst]:
                    iindex = right.index(i)
                    left.extend(right[: iindex + 1])
                    right = right[iindex + 1 :]
            corected = left + [inst] + right
            # print(inst)
            # print(corected)
        correctedUpdate.append(corected)
    print()
    # print(correctedUpdate)
    sumofmiddles = sum([x[len(x) // 2] for x in correctedUpdate])
    print(sumofmiddles)
    endtimeP2 = time.time()
    print("Time taken: ", endtimeP2 - endtime)
    print("Time taken in ms: ", (endtimeP2 - endtime) * 1000)


if __name__ == "__main__":
    main()
