import os
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/games.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "r")

    game_dict = {}

    max_allowed_balls = {"red": 12, "blue": 14, "green": 13}

    # Loop over lines in file
    for line in file:
        list_of_plays = []

        game_line = line.split(":")
        # play line
        play_line = game_line[1].split(";")
        for currentplay in play_line:
            play = {"red": 0, "blue": 0, "green": 0}
            list_of_balls = currentplay.split(",")
            for ball in list_of_balls:
                ball_split = ball.strip().split(" ")
                play[ball_split[1]] += int(ball_split[0])
            list_of_plays.append(play.copy())

        game_dict[game_line[0].split(" ")[1]] = list_of_plays.copy()

    sum_of_game_ids = 0

    for game, plays in game_dict.items():
        invalid = False
        for play in plays:
            for color, balls in play.items():
                if balls > max_allowed_balls[color]:
                    invalid = True
                    break
            if invalid:
                break
        if not invalid:
            sum_of_game_ids += int(game)

    print(sum_of_game_ids)

    # Find minimum needed balls
    overall_power = 0
    for game, plays in game_dict.items():
        power = 0
        minimum_balls = {"red": 0, "blue": 0, "green": 0}
        for play in plays:
            for color, balls in play.items():
                if balls > minimum_balls[color]:
                    minimum_balls[color] = balls
        power = minimum_balls["red"] * minimum_balls["blue"] * minimum_balls["green"]
        print("game", game, "power", power, "minimum_balls", minimum_balls)
        overall_power += power

        print("overall_power", overall_power)

    end_time = time.time()
    print("Time: ", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
