import os
import time


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/storage.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        storeagedensity = file.readline().strip()
    # print(storeagedensity)

    totalMemLength = sum([int(x) for x in storeagedensity])
    # print(totalMemLength)

    memory = [None] * totalMemLength
    currentLoc = 0  # current location in memory
    curFileID = 0
    freeSpace = []
    fileList = []
    for i, entry in enumerate(storeagedensity):
        if i % 2 == 0:
            fileList.append((currentLoc, currentLoc + int(entry)))
            for j in range(currentLoc, currentLoc + int(entry)):
                memory[j] = str(curFileID)

            curFileID += 1
        else:
            freeSpace.append((currentLoc, currentLoc + int(entry)))
            for j in range(currentLoc, currentLoc + int(entry)):
                memory[j] = "."
        currentLoc += int(entry)

    # print(memory)
    memPart2 = memory.copy()
    preCursor = 0
    postCursor = totalMemLength - 1

    while preCursor < postCursor:
        # print(preCursor, postCursor)
        temp = memory[postCursor]
        if memory[preCursor] == ".":
            memory[preCursor] = temp
            memory[postCursor] = "."
            preCursor += 1
            while memory[postCursor] == ".":
                postCursor -= 1
        else:
            preCursor += 1

    # print(memory)
    total = 0
    for i in range(postCursor + 1):

        total += int(memory[i]) * i
    print(total)

    endTime = time.time()
    print("Time part 1: ", endTime - start_time)
    print("Time part 1 in ms: ", (endTime - start_time) * 1000)
    newFree = None
    # print(memPart2)
    # print(freeSpace)
    for file in fileList[::-1]:
        # print(memPart2)
        # print(file)
        size = file[1] - file[0]
        fileID = memPart2[file[0]]
        for i, free in enumerate(freeSpace):
            if free[1] - free[0] >= size and free[0] < file[0]:
                for j in range(file[0], file[1]):
                    memPart2[j] = "."
                for k in range(free[0], free[0] + size):
                    memPart2[k] = fileID
                newFree = (free[0] + size, free[1])
                freeSpace[i] = newFree
                break

        # print(freeSpace)

    # print(memPart2)
    total = 0
    for i, mem in enumerate(memPart2):
        # print(i, mem, total)
        if not mem == ".":
            total += int(mem) * i
        # print(total)

    print(total)
    endTimeP2 = time.time()
    print("Time part 2: ", endTimeP2 - endTime)
    print("Time part 2 in ms: ", (endTimeP2 - endTime) * 1000)


if __name__ == "__main__":
    main()
