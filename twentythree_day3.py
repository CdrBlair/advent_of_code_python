import operator
import os
import time
from functools import reduce
from re import T
from typing import List, Tuple

# definee dict for the engine schematic and max x and y
engine_schematic = {}
max_x = 0
max_y = 0
part_numbers_coords = {}


# Main method
def main():
    start_time = time.time()
    global max_x, max_y, engine_schematic, part_numbers_coords

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/engine_schematic.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "r")

    # Loop over lines in file and file the engine schematic
    coordinate = (0, 0)
    for line in file:
        line = line.strip("\n")
        for char in line:
            engine_schematic[coordinate] = char
            coordinate = (coordinate[0] + 1, coordinate[1])
        coordinate = (0, coordinate[1] + 1)

    # loop over engine schematic and find max x and y

    for key in engine_schematic:
        if key[0] > max_x:
            max_x = key[0]
        if key[1] > max_y:
            max_y = key[1]

    # loop over engine schematic and print it
    # for y in range(max_y + 1):
    #     print(y, end=" ")
    #     for x in range(max_x + 1):
    #         print(engine_schematic[(x, y)], end="")
    #     print()

    # loop over engine schematic and find part number (those adjacent to a symbol)
    part_numbers = []
    y = 0
    for y in range(max_y + 1):
        x = 0
        while x <= max_x:
            if engine_schematic[(x, y)].isdigit():
                number, coordinates_of_number, coordinate = extract_number((x, y))
                if check_adjacent(coordinates_of_number):
                    part_numbers.append(number)
                    part_numbers_coords[tuple(coordinates_of_number)] = number
                x = coordinate[0]
            x += 1

    # print(part_numbers)
    print("Sum of engine parts: ", sum(part_numbers))
    end_time = time.time()
    print("Time taken part 1: ", end_time - start_time)
    print("Time taken in ms part 1: ", (end_time - start_time) * 1000)

    # Part 2
    start_time_part_2 = time.time()
    # loop over engine schematic and find gears with exactly two part numbers adjacent
    gears_with_two_part_numbers = []
    y = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if engine_schematic[(x, y)] == "*":
                (
                    adjacent_to_two_part_numbers,
                    part_numbers,
                ) = check_adjacent_to_two_part_numbers((x, y))
                if adjacent_to_two_part_numbers:
                    gears_with_two_part_numbers.append(
                        (x, y, reduce(operator.mul, part_numbers))
                    )

    print("Sum of gear ratio", sum(t[2] for t in gears_with_two_part_numbers))
    end_time_part_2 = time.time()
    print("Time taken part 2: ", end_time_part_2 - start_time_part_2)
    print("Time taken in ms part 2: ", (end_time_part_2 - start_time_part_2) * 1000)
    print("Time taken total: ", end_time_part_2 - start_time)
    print("Time taken in ms total: ", (end_time_part_2 - start_time) * 1000)


# Method to check if gear adjacent to exactly two part numbers
def check_adjacent_to_two_part_numbers(
    coordinate: Tuple[int, int]
) -> (bool, Tuple[int, int]):
    global max_x, max_y, engine_schematic, part_numbers_coords
    adjacent_part_numbers = []
    adjacent_coordinates = []
    # at the right
    coordinate_right = (coordinate[0] + 1, coordinate[1])
    adjacent_coordinates.append(coordinate_right)
    # left
    coordinate_left = (coordinate[0] - 1, coordinate[1])
    adjacent_coordinates.append(coordinate_left)
    # below
    coordinate_below = (coordinate[0], coordinate[1] + 1)
    adjacent_coordinates.append(coordinate_below)
    # above
    coordinate_above = (coordinate[0], coordinate[1] - 1)
    adjacent_coordinates.append(coordinate_above)
    # top left
    coordinate_top_left = (coordinate[0] - 1, coordinate[1] - 1)
    adjacent_coordinates.append(coordinate_top_left)
    # top right
    coordinate_top_right = (coordinate[0] + 1, coordinate[1] - 1)
    adjacent_coordinates.append(coordinate_top_right)
    # bottom left
    coordinate_bottom_left = (coordinate[0] - 1, coordinate[1] + 1)
    adjacent_coordinates.append(coordinate_bottom_left)
    # bottom right
    coordinate_bottom_right = (coordinate[0] + 1, coordinate[1] + 1)
    adjacent_coordinates.append(coordinate_bottom_right)

    # iterate over part numbers an check if adjacent

    for coordinates, part_number in part_numbers_coords.items():
        for coordinate in coordinates:
            if coordinate in adjacent_coordinates:
                adjacent_part_numbers.append(part_number)
                break
        if len(adjacent_part_numbers) > 2:
            return False, None
    if len(adjacent_part_numbers) == 2:
        return True, tuple(adjacent_part_numbers)
    return False, None


# Method to check for adjacent symbols
def check_adjacent(coordinates: List[Tuple[int, int]]) -> bool:
    global max_x, max_y, engine_schematic
    for coordinate in coordinates:
        # at the right
        if (
            (coordinate[0] + 1, coordinate[1]) in engine_schematic
            and not engine_schematic[(coordinate[0] + 1, coordinate[1])].isdigit()
            and not engine_schematic[(coordinate[0] + 1, coordinate[1])] == "."
        ):
            return True
        # left
        if (
            (coordinate[0] - 1, coordinate[1]) in engine_schematic
            and not engine_schematic[(coordinate[0] - 1, coordinate[1])].isdigit()
            and not engine_schematic[(coordinate[0] - 1, coordinate[1])] == "."
        ):
            return True
        # below
        if (
            (coordinate[0], coordinate[1] + 1) in engine_schematic
            and not engine_schematic[(coordinate[0], coordinate[1] + 1)].isdigit()
            and not engine_schematic[(coordinate[0], coordinate[1] + 1)] == "."
        ):
            return True
        # above
        if (
            (coordinate[0], coordinate[1] - 1) in engine_schematic
            and not engine_schematic[(coordinate[0], coordinate[1] - 1)].isdigit()
            and not engine_schematic[(coordinate[0], coordinate[1] - 1)] == "."
        ):
            return True
        # top left
        if (
            (coordinate[0] - 1, coordinate[1] - 1) in engine_schematic
            and not engine_schematic[(coordinate[0] - 1, coordinate[1] - 1)].isdigit()
            and not engine_schematic[(coordinate[0] - 1, coordinate[1] - 1)] == "."
        ):
            return True
        # top right
        if (
            (coordinate[0] + 1, coordinate[1] - 1) in engine_schematic
            and not engine_schematic[(coordinate[0] + 1, coordinate[1] - 1)].isdigit()
            and not engine_schematic[(coordinate[0] + 1, coordinate[1] - 1)] == "."
        ):
            return True
        # bottom left
        if (
            (coordinate[0] - 1, coordinate[1] + 1) in engine_schematic
            and not engine_schematic[(coordinate[0] - 1, coordinate[1] + 1)].isdigit()
            and not engine_schematic[(coordinate[0] - 1, coordinate[1] + 1)] == "."
        ):
            return True
        # bottom right
        if (
            (coordinate[0] + 1, coordinate[1] + 1) in engine_schematic
            and not engine_schematic[(coordinate[0] + 1, coordinate[1] + 1)].isdigit()
            and not engine_schematic[(coordinate[0] + 1, coordinate[1] + 1)] == "."
        ):
            return True
    return False


# Method to fine number starting at given coordinate
def extract_number(coordinate: Tuple[int, int]) -> (int, List, Tuple[int, int]):
    global max_x, max_y, engine_schematic
    number = ""
    coordinates_of_number = []
    while coordinate[0] <= max_x and engine_schematic[coordinate].isdigit():
        number += engine_schematic[coordinate]
        coordinates_of_number.append(coordinate)
        coordinate = (coordinate[0] + 1, coordinate[1])
    return int(number), coordinates_of_number, (coordinate[0] - 1, coordinate[1])


if __name__ == "__main__":
    main()
