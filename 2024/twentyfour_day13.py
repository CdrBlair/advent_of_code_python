import os
import time
from collections import deque


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/clawmachine.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    clawmachines = []
    # ((vax, vay), (vbx, vby), (tx, ty))
    nextclaw = None
    for line in lines:
        if line.strip() == "":
            clawmachines.append(nextclaw)
            nextclaw = None
            continue
        splitted = line.strip().split(":")
        if splitted[0] == "Button A":
            vax = int(splitted[1].split(",")[0].split("+")[1])
            vay = int(splitted[1].split(",")[1].split("+")[1])
            nextclaw = ((vax, vay), None, None)
        elif splitted[0] == "Button B":
            vbx = int(splitted[1].split(",")[0].split("+")[1])
            vby = int(splitted[1].split(",")[1].split("+")[1])
            nextclaw = (nextclaw[0], (vbx, vby), None)
        else:
            tx = int(splitted[1].split(",")[0].split("=")[1])
            ty = int(splitted[1].split(",")[1].split("=")[1])
            nextclaw = (nextclaw[0], nextclaw[1], (tx, ty))
    clawmachines.append(nextclaw)

    # print(clawmachines)

    wins = []

    for clawmachine in clawmachines:
        (vax, vay), (vbx, vby), (tx, ty) = clawmachine
        # print(vax, vay, vbx, vby, tx, ty)

        valueA = (vby * tx - vbx * ty) / (vax * vby - vay * vbx)
        valueB = (vax * ty - vay * tx) / (vax * vby - vay * vbx)

        # print(valueA, valueB)
        if valueA.is_integer() and valueB.is_integer():
            wins.append((valueA, valueB, 3 * valueA + valueB))

    sumTokens = sum(x[2] for x in wins)
    print(int(sumTokens))
    endTimepart1 = time.time()
    print("Part 1 took: ", endTimepart1 - start_time)
    print("Part 1 took in ms: ", (endTimepart1 - start_time) * 1000)

    alteredMachines = []
    for clawmachine in clawmachines:
        clawmachine = (
            clawmachine[0],
            clawmachine[1],
            (clawmachine[2][0] + 10000000000000, clawmachine[2][1] + 10000000000000),
        )
        alteredMachines.append(clawmachine)
    clawmachines = alteredMachines
    wins = []
    for clawmachine in clawmachines:
        (vax, vay), (vbx, vby), (tx, ty) = clawmachine
        # print(vax, vay, vbx, vby, tx, ty)

        valueA = (vby * tx - vbx * ty) / (vax * vby - vay * vbx)
        valueB = (vax * ty - vay * tx) / (vax * vby - vay * vbx)

        # print(valueA, valueB)
        if valueA.is_integer() and valueB.is_integer():
            wins.append((valueA, valueB, 3 * valueA + valueB))
    # print(wins)
    print(int(sum(x[2] for x in wins)))

    endtimeP2 = time.time()
    print("Part 2 took: ", endtimeP2 - endTimepart1)
    print("Part 2 took in ms: ", (endtimeP2 - endTimepart1) * 1000)


if __name__ == "__main__":
    main()
