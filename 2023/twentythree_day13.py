import os
import time


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/rocks_and_ashes.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    blocks = []
    blocks.append([])
    for line in lines:
        if line.strip() == "":
            blocks.append([])
            continue
        blocks[-1].append(line.strip())

    # for block in blocks:
    #     for line in block:
    #         print(line)
    #     print()

    sumOfNotes = 0
    originaleReflectionLines = []
    for block in blocks:
        # first check horizontal
        reflectionLine = findReflections(block, -1)

        if reflectionLine > 0:
            originaleReflectionLines.append(("H", reflectionLine))
            sumOfNotes += 100 * reflectionLine
            continue
        # then check vertical
        # transpose
        blockTransposed = ["".join(x)[::-1] for x in zip(*block)]
        reflectionLine = findReflections(blockTransposed, -1)
        originaleReflectionLines.append(("V", reflectionLine))
        sumOfNotes += reflectionLine

    print("Sum of notes: ", sumOfNotes)
    endTimeP1 = time.time()
    print("Part one time: ", endTimeP1 - start_time)
    print("Part one time in ms: ", (endTimeP1 - start_time) * 1000)

    # Part two
    start_timeP2 = time.time()
    sumOfNotes = 0
    for block, original in zip(blocks, originaleReflectionLines):
        # iterate over all chars and change them
        foundReflection = False
        for i, line in enumerate(block):
            for j, char in enumerate(line):
                currentRow = block[i]
                if char == "#":
                    block[i] = line[:j] + "." + line[j + 1 :]
                else:
                    block[i] = line[:j] + "#" + line[j + 1 :]
                # first check horizontal
                if original[0] == "H":
                    originalLine = original[1]
                else:
                    originalLine = -1
                reflectionLine = findReflections(block, originalLine)

                if reflectionLine > 0:
                    sumOfNotes += 100 * reflectionLine
                    # for blockline in block:
                    #     print(blockline)
                    # print()
                    foundReflection = True
                    break
                # then check vertical
                # transpose
                blockTransposed = ["".join(x)[::-1] for x in zip(*block)]

                if original[0] == "V":
                    originalLine = original[1]
                else:
                    originalLine = -1
                reflectionLine = findReflections(blockTransposed, originalLine)
                if reflectionLine > 0:
                    sumOfNotes += reflectionLine
                    # for blockline in blockTransposed:
                    #     print(blockline)
                    # print()
                    # print("V", reflectionLine)
                    foundReflection = True
                    break
                block[i] = currentRow
            if foundReflection:
                break
        if not foundReflection:
            if original[0] == "H":
                sumOfNotes += 100 * original[1]
            else:
                sumOfNotes += original[1]

    print("Sum of notes P2: ", sumOfNotes)
    endTimeP2 = time.time()
    print("Part two time: ", endTimeP2 - start_timeP2)
    print("Part two time in ms: ", (endTimeP2 - start_timeP2) * 1000)
    print("Total time: ", endTimeP2 - start_time)
    print("Total time in ms: ", (endTimeP2 - start_time) * 1000)


def findReflections(block, original):
    maxLines = len(block)

    for i in range(1, maxLines):
        foundReflection = True
        distTotop = i
        distToBottom = maxLines - i
        if distTotop == distToBottom:
            aboveRange = range(i - 1, -1, -1)
            belowRange = range(i, maxLines)
        if distTotop > distToBottom:
            aboveRange = range(i - 1, i - distToBottom - 1, -1)
            belowRange = range(i, maxLines)
        if distTotop < distToBottom:
            aboveRange = range(i - 1, -1, -1)
            belowRange = range(i, i + distTotop)

        for j, k in zip(aboveRange, belowRange):
            if not block[j] == block[k]:
                foundReflection = False
                break
        if foundReflection:
            if not original == i:
                return i

    return 0


if __name__ == "__main__":
    main()
