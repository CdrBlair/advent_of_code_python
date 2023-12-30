import os
import sys
import time
from functools import cache


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/machineparts.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    rulesFinished = False
    workflows = {}
    parts = []
    for line in lines:
        line = line.strip()
        if line == "":
            rulesFinished = True
            continue

        if not rulesFinished:
            nameAndRest = line.split("{")
            name = nameAndRest[0]

            rules = []
            rest = nameAndRest[1].replace("}", "")

            ruleStrings = rest.split(",")
            for ruleString in ruleStrings:
                ruleString = ruleString.strip()

                if ruleString.__contains__("<") or ruleString.__contains__(">"):
                    if ruleString.__contains__("<"):
                        ruleString = ruleString.replace("<", ":")
                        ruleString = ruleString.split(":")
                        rule = (ruleString[0], "<", int(ruleString[1]), ruleString[2])
                    else:
                        ruleString = ruleString.replace(">", ":")
                        ruleString = ruleString.split(":")
                        rule = (ruleString[0], ">", int(ruleString[1]), ruleString[2])
                else:
                    rule = (None, None, None, ruleString)
                rules.append(rule)
            workflows[name] = tuple(rules)
        else:
            partCharacteristicsString = (
                line.replace("{", "").replace("}", "").split(",")
            )
            part = (
                int(partCharacteristicsString[0].split("=")[1]),
                int(partCharacteristicsString[1].split("=")[1]),
                int(partCharacteristicsString[2].split("=")[1]),
                int(partCharacteristicsString[3].split("=")[1]),
            )
            parts.append(part)

    # Evaluate all parts
    accepted = []
    rejected = []
    for part in parts:
        acceptedOrRejected = False
        currentWorkFlow = "in"
        while not acceptedOrRejected:
            wfResult = evaluateWorkflow(part, workflows[currentWorkFlow])
            if wfResult == "A":
                accepted.append(part)
                acceptedOrRejected = True
            elif wfResult == "R":
                rejected.append(part)
                acceptedOrRejected = True
            else:
                currentWorkFlow = wfResult

    print("Sum", sum(sum(t) for t in accepted))
    endTimePart1 = time.time()
    print("Part 1 finished in ", endTimePart1 - start_time, " seconds")
    print("Part 1 finished in ", (endTimePart1 - start_time) * 1000, " ms")
    startP2 = time.time()

    # Part 2
    # Starting values
    minX = 1
    maxX = 4000
    minM = 1
    maxM = 4000
    minA = 1
    maxA = 4000
    minS = 1
    maxS = 4000

    # Get all combinations
    Totalcombinations = getCombinations(
        minX, maxX, minM, maxM, minA, maxA, minS, maxS, workflows["in"], workflows
    )

    print("Combinations: ", Totalcombinations)

    endTimePart2 = time.time()
    print("Part 2 finished in ", endTimePart2 - startP2, " seconds")
    print("Part 2 finished in ", (endTimePart2 - startP2) * 1000, " ms")
    print("Total time: ", endTimePart2 - start_time)


def getCombinations(
    minX, maxX, minM, maxM, minA, maxA, minS, maxS, workflow, workflows
):
    combinations = 0
    for rule in workflow:
        if rule[0] == None:
            if rule[3] == "R":
                combinations += 0
            elif rule[3] == "A":
                combinations += (
                    (maxX - minX + 1)
                    * (maxM - minM + 1)
                    * (maxA - minA + 1)
                    * (maxS - minS + 1)
                )
            else:
                combinations += getCombinations(
                    minX,
                    maxX,
                    minM,
                    maxM,
                    minA,
                    maxA,
                    minS,
                    maxS,
                    workflows[rule[3]],
                    workflows,
                )
        if rule[0] == "x":
            if rule[1] == "<" and minX < rule[2]:
                if rule[3] == "R":
                    minX = rule[2]
                elif rule[3] == "A":
                    calculationValue = maxX if maxX < rule[2] - 1 else rule[2] - 1

                    combinations += (
                        (calculationValue - minX + 1)
                        * (maxM - minM + 1)
                        * (maxA - minA + 1)
                        * (maxS - minS + 1)
                    )
                    minX = rule[2]
                else:
                    calculationValue = rule[2] - 1
                    combinations += getCombinations(
                        minX,
                        calculationValue,
                        minM,
                        maxM,
                        minA,
                        maxA,
                        minS,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    minX = rule[2]
            elif rule[1] == ">" and maxX > rule[2]:
                if rule[3] == "R":
                    maxX = rule[2]
                elif rule[3] == "A":
                    calculationValue = minX if minX > rule[2] + 1 else rule[2] + 1

                    combinations += (
                        (maxX - calculationValue + 1)
                        * (maxM - minM + 1)
                        * (maxA - minA + 1)
                        * (maxS - minS + 1)
                    )
                    maxX = rule[2]
                else:
                    calculationValue = minX if minX > rule[2] + 1 else rule[2] + 1
                    combinations += getCombinations(
                        calculationValue,
                        maxX,
                        minM,
                        maxM,
                        minA,
                        maxA,
                        minS,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    maxX = rule[2]
        if rule[0] == "m":
            if rule[1] == "<" and minM < rule[2]:
                if rule[3] == "R":
                    minM = rule[2]
                elif rule[3] == "A":
                    calculationValue = maxM if maxM < rule[2] - 1 else rule[2] - 1

                    combinations += (
                        (maxX - minX + 1)
                        * (calculationValue - minM + 1)
                        * (maxA - minA + 1)
                        * (maxS - minS + 1)
                    )
                    minM = rule[2]
                else:
                    calculationValue = rule[2] - 1
                    combinations += getCombinations(
                        minX,
                        maxX,
                        minM,
                        calculationValue,
                        minA,
                        maxA,
                        minS,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    minM = rule[2]
            elif rule[1] == ">" and maxM > rule[2]:
                if rule[3] == "R":
                    maxM = rule[2]
                elif rule[3] == "A":
                    calculationValue = minM if minM > rule[2] + 1 else rule[2] + 1

                    combinations += (
                        (maxX - minX + 1)
                        * (maxM - calculationValue + 1)
                        * (maxA - minA + 1)
                        * (maxS - minS + 1)
                    )
                    maxM = rule[2]
                else:
                    calculationValue = minM if minM > rule[2] + 1 else rule[2] + 1
                    combinations += getCombinations(
                        minX,
                        maxX,
                        calculationValue,
                        maxM,
                        minA,
                        maxA,
                        minS,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    maxM = rule[2]
        if rule[0] == "a":
            if rule[1] == "<" and minA < rule[2]:
                if rule[3] == "R":
                    minA = rule[2]
                elif rule[3] == "A":
                    calculationValue = maxA if maxA < rule[2] - 1 else rule[2] - 1

                    combinations += (
                        (maxX - minX + 1)
                        * (maxM - minM + 1)
                        * (calculationValue - minA + 1)
                        * (maxS - minS + 1)
                    )
                    minA = rule[2]
                else:
                    calculationValue = maxA if maxA < rule[2] - 1 else rule[2] - 1
                    combinations += getCombinations(
                        minX,
                        maxX,
                        minM,
                        maxM,
                        minA,
                        calculationValue,
                        minS,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    minA = rule[2]
            elif rule[1] == ">" and maxA > rule[2]:
                if rule[3] == "R":
                    maxA = rule[2]
                elif rule[3] == "A":
                    calculationValue = minA if minA > rule[2] + 1 else rule[2] + 1

                    combinations += (
                        (maxX - minX + 1)
                        * (maxM - minM + 1)
                        * (maxA - calculationValue + 1)
                        * (maxS - minS + 1)
                    )
                    maxA = rule[2]
                else:
                    calculationValue = minA if minA > rule[2] + 1 else rule[2] + 1
                    combinations += getCombinations(
                        minX,
                        maxX,
                        minM,
                        maxM,
                        calculationValue,
                        maxA,
                        minS,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    maxA = rule[2]
        if rule[0] == "s":
            if rule[1] == "<" and minS < rule[2]:
                if rule[3] == "R":
                    minS = rule[2]
                elif rule[3] == "A":
                    calculationValue = maxS if maxS < rule[2] - 1 else rule[2] - 1

                    combinations += (
                        (maxX - minX + 1)
                        * (maxM - minM + 1)
                        * (maxA - minA + 1)
                        * (calculationValue - minS + 1)
                    )
                    minS = rule[2]
                else:
                    calculationValue = maxS if maxS < rule[2] - 1 else rule[2] - 1
                    combinations += getCombinations(
                        minX,
                        maxX,
                        minM,
                        maxM,
                        minA,
                        maxA,
                        minS,
                        calculationValue,
                        workflows[rule[3]],
                        workflows,
                    )
                    minS = rule[2]
            elif rule[1] == ">" and maxS > rule[2]:
                if rule[3] == "R":
                    maxS = rule[2]
                elif rule[3] == "A":
                    calculationValue = minS if minS > rule[2] + 1 else rule[2] + 1

                    combinations += (
                        (maxX - minX + 1)
                        * (maxM - minM + 1)
                        * (maxA - minA + 1)
                        * (maxS - calculationValue + 1)
                    )
                    maxS = rule[2]
                else:
                    calculationValue = minS if minS > rule[2] + 1 else rule[2] + 1
                    combinations += getCombinations(
                        minX,
                        maxX,
                        minM,
                        maxM,
                        minA,
                        maxA,
                        calculationValue,
                        maxS,
                        workflows[rule[3]],
                        workflows,
                    )
                    maxS = rule[2]
    return combinations


@cache
def evaluateWorkflow(part, workflow):
    charIndex = {"x": 0, "m": 1, "a": 2, "s": 3}
    for rule in workflow:
        if rule[0] == None:
            return rule[3]
        elif rule[1] == "<":
            if part[charIndex[rule[0]]] < int(rule[2]):
                return rule[3]
        elif rule[1] == ">":
            if part[charIndex[rule[0]]] > int(rule[2]):
                return rule[3]


if __name__ == "__main__":
    main()
