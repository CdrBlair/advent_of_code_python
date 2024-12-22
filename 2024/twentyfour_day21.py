import os
import time
from functools import lru_cache




def main():

    starttime = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/code.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    codes = []
    for line in lines:
        codes.append((line.strip(), int(line.strip()[:-1])))
    print(codes)
    lengths = []
    for code in codes:
        lengths.append((code, calculateLength(code[0], 3)))
    print(lengths)
    complexity = sum(x[0][1]*x[1] for x in lengths)
    print(complexity)
    endtimep1 = time.time()
    print("Part 1 took: ", endtimep1 - starttime)
    print("Part 1 took in ms: ", (endtimep1 - starttime) * 1000)

    lengths = []
    for code in codes:
        lengths.append((code, calculateLength(code[0], 26, True)))
    print(lengths)
    complexity = sum(x[0][1]*x[1] for x in lengths)
    print(complexity)

    endtimep2 = time.time()
    print("Part 2 took: ", endtimep2 - endtimep1)
    print("Part 2 took in ms: ", (endtimep2 - endtimep1) * 1000)


@lru_cache(maxsize=None)
def calculateLength(code, level, part2=False):
    length = 0
    if level == 0:
        return len(code)
    for i, c in enumerate(code):
        length += calculateLength(findPath(code[i-1], c, level, part2), level - 1, part2)
    return length

@lru_cache(maxsize=None)
def findPath(start, end, level, part2=False):

    keypad = {}
    keypad['7'] = (0, 0)
    keypad['8'] = (1, 0)
    keypad['9'] = (2, 0)
    keypad['4'] = (0, 1)
    keypad['5'] = (1, 1)
    keypad['6'] = (2, 1)
    keypad['1'] = (0, 2)
    keypad['2'] = (1, 2)
    keypad['3'] = (2, 2)
    keypad['0'] = (1, 3)
    keypad['A'] = (2, 3)
    keypad[' '] = (0,3)

 
    controlpad = {}
    controlpad['^'] = (1, 0)
    controlpad['A'] = (2,0)
    controlpad['<'] = (0, 1)
    controlpad['v'] = (1, 1)
    controlpad['>'] = (2, 1)
    controlpad[' '] = (0,0)
    if (level == 3 and not part2) or (level == 26 and part2):
        pad = keypad
    else:
        pad = controlpad

    x, y = pad[start]
    endx, endy = pad[end]
    diff = (endx - x, endy - y)
    #print(diff)
    if diff[0] > 0:
        horizontal = diff[0] * ">"
    else:
        horizontal = abs(diff[0]) * "<"
    if diff[1] > 0:
        vertical = diff[1] * "v"
    else:
        vertical = abs(diff[1]) * "^"

    #print(horizontal, vertical)
    
    badSpotX = pad[' '][0] - x
    badSpotY = pad[' '][1] - y
    verticalFirst = (diff[0]  > 0 or (badSpotY == 0 and badSpotX == diff[0])) and (badSpotX!=0 or diff[1]!=badSpotY)


    return (vertical + horizontal if verticalFirst else horizontal + vertical) + 'A'
    




         




if __name__ == "__main__":
    main()
