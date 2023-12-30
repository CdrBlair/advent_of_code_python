import functools
import os
import time
from collections import Counter


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/camel_games.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    games = []
    for line in lines:
        games.append((line.split(" ")[0].strip(), int(line.split(" ")[1].strip()), 0))

    games = rank(games, True)

    games = sorted(games, key=functools.cmp_to_key(compare_games_p1))

    total_winnings = 0
    for i, game in enumerate(games):
        total_winnings += game[1] * (i + 1)

    print("Total winnings: ", total_winnings)
    end_time_p1 = time.time()
    print("Time taken part 1: ", end_time_p1 - start_time)
    print("Time taken in ms part 1: ", (end_time_p1 - start_time) * 1000)

    games = rank(games, False)

    games = sorted(games, key=functools.cmp_to_key(compare_games_p2))

    total_winnings = 0
    for i, game in enumerate(games):
        total_winnings += game[1] * (i + 1)

    print("Total winnings: ", total_winnings)
    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total in ms: ", (end_time_p2 - start_time) * 1000)


# AAAA8 AAA88 AA888 A8888


# comparotor for games based on hands
def compare_games_p1(game1, game2):
    ranks = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    if not game1[2] == game2[2]:
        return game1[2] - game2[2]

    for i, char in enumerate(game1[0]):
        if char == game2[0][i]:
            continue
        else:
            return ranks[char] - ranks[game2[0][i]]
    return 0


# comparotor for games based on hands
def compare_games_p2(game1, game2):
    ranks = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    if not game1[2] == game2[2]:
        return game1[2] - game2[2]

    for i, char in enumerate(game1[0]):
        if char == game2[0][i]:
            continue
        else:
            return ranks[char] - ranks[game2[0][i]]
    return 0


# define rank of
def rank(games, part1):
    games_with_ranks = []

    for game_original in games:
        len_set_of_cards = len(set(game_original[0]))
        card_counter = Counter(game_original[0])
        if "J" in game_original[0] and not len_set_of_cards == 1 and not part1:
            card_counter_copy = card_counter.copy()
            card_counter_copy.pop("J")
            top_card, top_count = card_counter_copy.most_common(1)[0]
            game = (
                game_original[0].replace("J", top_card),
                game_original[1],
                game_original[2],
            )

        else:
            game = game_original

        len_set_of_cards = len(set(game[0]))
        card_counter = Counter(game[0])

        if len(game[0]) == len_set_of_cards:
            game = (game[0], game[1], 0)
        elif len_set_of_cards == 1:
            game = (game[0], game[1], 6)

        if len_set_of_cards == 2:
            if 4 in card_counter.values():
                game = (game[0], game[1], 5)
            else:
                game = (game[0], game[1], 4)
        elif len_set_of_cards == 3:
            if 3 in card_counter.values():
                game = (game[0], game[1], 3)
            else:
                game = (game[0], game[1], 2)
        elif len_set_of_cards == 4:
            game = (game[0], game[1], 1)

        games_with_ranks.append((game_original[0], game_original[1], game[2]))
    return games_with_ranks


if __name__ == "__main__":
    main()
