import math
import os
import re
import time
from tokenize import String


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/races.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    times_string = re.sub(" +", " ", lines.pop(0).split(":")[1].strip())
    distances_string = re.sub(" +", " ", lines.pop(0).split(":")[1].strip())

    possible_wins = calculate_wins(times_string, distances_string, True)
    print("Multiply possible wins: ", math.prod(possible_wins))
    end_time_p1 = time.time()
    print("Time taken part 1: ", end_time_p1 - start_time)
    print("Time taken in ms part 1: ", (end_time_p1 - start_time) * 1000)
    possible_wins = calculate_wins(times_string, distances_string, False)
    print("Multiply possible wins: ", math.prod(possible_wins))
    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total in ms: ", (end_time_p2 - start_time) * 1000)


def calculate_wins(times: str, distance: str, part1: bool):
    races = []
    if part1:
        times_string = times.split(" ")
        distances_string = distance.split(" ")
    else:
        times_string = [re.sub(" +", "", times)]
        distances_string = [re.sub(" +", "", distance)]

    for i in range(len(times_string)):
        races.append((int(times_string[i].strip()), int(distances_string[i].strip())))

    max_time = max(num[0] for num in races)

    possible_wins = []
    for race in races:
        lower_min = 0.5 * (race[0] - math.sqrt(race[0] ** 2 - 4 * race[1]))
        lower_max = 0.5 * (race[0] + math.sqrt(race[0] ** 2 - 4 * race[1]))

        race_possible_wins = 0

        race_possible_wins = math.floor(lower_max) - math.floor(lower_min)
        possible_wins.append(race_possible_wins)
    return possible_wins


if __name__ == "__main__":
    main()
