import os
import re
import time

cards = {}


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/cards.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "r")

    # Loop over lines in file
    for line in file:
        name_split = line.split(":")
        game_number = int(re.sub(" +", " ", name_split[0]).split(" ")[1])
        numbers_split = name_split[1].strip().split("|")

        winning_numbers = [
            int(num) for num in re.sub(" +", " ", numbers_split[0].strip()).split(" ")
        ]
        my_numbers = [
            int(num) for num in re.sub(" +", " ", numbers_split[1].strip()).split(" ")
        ]

        cards[game_number] = [(winning_numbers, my_numbers), 0, 1]

    # Iterate over all cards, calculate points and sum up
    sum_of_points = 0
    for game, numbers in cards.items():
        points, matches = find_points(numbers[0][0], numbers[0][1])
        sum_of_points += points
        cards[game][1] = matches

    print(sum_of_points)
    end_time = time.time()
    print("Time taken part 1: ", end_time - start_time)
    print("Time taken in ms part 1: ", (end_time - start_time) * 1000)

    start_time_part_2 = time.time()
    # iterate over all games and copie following ones depending on matches

    for game, numbers in cards.items():
        for matches in range(1, numbers[1] + 1):
            if game + matches in cards:
                cards[game + matches][2] += numbers[2]

    # iterate over games an sum up copies
    sum_of_cards = 0
    for game, numbers in cards.items():
        sum_of_cards += numbers[2]

    print(sum_of_cards)

    end_time_part_2 = time.time()
    print("Time taken part 2: ", end_time_part_2 - start_time_part_2)
    print("Time taken in ms part 2: ", (end_time_part_2 - start_time_part_2) * 1000)
    print("Time taken total: ", end_time_part_2 - start_time)
    print("Time taken in ms total: ", (end_time_part_2 - start_time) * 1000)


# Find how many points in this game and calculate points
from typing import Tuple


def find_points(winning_numbers, my_numbers) -> Tuple[int, int]:
    points = 0
    winning_set = set(winning_numbers)
    my_set = set(my_numbers)
    intersection = winning_set.intersection(my_set)
    matches = len(intersection)

    if matches > 0:
        points = 1 * (2 ** (matches - 1))

    return points, matches


if __name__ == "__main__":
    main()
