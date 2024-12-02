import os
import time


def main():
    start_time = time.time()

    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/doorcard.txt"

    with open(os.path.join(script_dir, rel_path)) as f:
        lines = f.readlines()

    screen = {}

    for i in range(6):
        for j in range(50):
            screen[(i, j)] = "."

    instructions = []

    for line in lines:
        instr = line.strip().split(" ")
        if instr[0] == "rect":
            instructions.append(
                ("rect", None, int(instr[1].split("x")[0]), int(instr[1].split("x")[1]))
            )

        else:
            instructions.append(
                (instr[0], instr[1], int(instr[2].split("=")[1]), int(instr[4]))
            )
    print(instructions)
    print_screen(screen)
    print()

    for instr in instructions:
        screen = modify_screen(screen, instr)
        print_screen(screen)
        print()

    # sum all # in values
    print(sum(1 for v in screen.values() if v == "#"))


def modify_screen(screen, instr):
    if instr[0] == "rect":
        for i in range(instr[3]):
            for j in range(instr[2]):
                screen[(i, j)] = "#"
    else:
        if instr[1] == "row":
            temp_row = []
            shift = instr[3]
            for j in range(50):
                if screen[(instr[2], j)] == "#":
                    temp_row.append(((j + shift) % 50))
                    screen[(instr[2], j)] = "."
            for j in range(50):
                if j in temp_row:
                    screen[(instr[2], j)] = "#"
        else:
            temp_col = []
            shift = instr[3]
            for i in range(6):
                if screen[(i, instr[2])] == "#":
                    temp_col.append(((i + shift) % 6))
                    screen[(i, instr[2])] = "."
            for i in range(6):
                if i in temp_col:
                    screen[(i, instr[2])] = "#"
    return screen


def print_screen(screen):
    for i in range(6):
        for j in range(50):
            print(screen[(i, j)], end="")
        print()


if __name__ == "__main__":
    main()
