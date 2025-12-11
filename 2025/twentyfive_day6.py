# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day6.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    problems = []
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        firstLine = True

        for line in lines:
            line = line.strip()
            parts = " ".join(line.split()).split(" ")
            print(parts)
            if firstLine:
                problems.extend([[int(x)] for x in parts])
                firstLine = False
            else:

                if parts[0].isnumeric():
                    for i in range(len(parts)):
                        problems[i].append(int(parts[i]))
                else:
                    for i in range(len(parts)):
                        problems[i].append(parts[i])
    totalsum = 0
    for problem in problems:
        if problem[-1] == "+":
            totalsum += sum(problem[:-1])
        elif problem[-1] == "*":
            prod = 1
            for num in problem[:-1]:
                prod *= num
            totalsum += prod
    print(f"Total Sum: {totalsum}")

    endP1 = time.time()
    print("Part 1 Time: ", endP1 - start_time)
    print("Part 1 in ms: ", (endP1 - start_time) * 1000)

    y = 0
    inputAsGrid = {}
    for line in lines:
        x = 0
        # remove /n
        line = line.rstrip("\r\n")
        for c in line:
            inputAsGrid[(x, y)] = c
            x += 1
        y += 1
    # print(inputAsGrid)
    maxX = x
    maxY = y

    newtotal = 0
    subCalc = 0
    curMod = ""
    for i in range(maxX):
        number = 0
        for j in range(maxY - 1):
            if inputAsGrid[(i, j)] == " ":
                continue
            number = number * 10 + int(inputAsGrid[(i, j)])
        if number == 0:
            newtotal += subCalc
            continue
        if inputAsGrid[(i, maxY - 1)] not in "+*":
            if curMod == "+":
                subCalc += number
            elif curMod == "*":
                subCalc *= number
        else:
            subCalc = 0 if inputAsGrid[(i, maxY - 1)] == "+" else 1
            curMod = inputAsGrid[(i, maxY - 1)]
            if curMod == "+":
                subCalc += number
            elif curMod == "*":
                subCalc *= number

    newtotal += subCalc

    print("New Total: ", newtotal)


if __name__ == "__main__":
    main()
