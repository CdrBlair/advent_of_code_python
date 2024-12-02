import os
import time


def main():
    start_time = time.time()

    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/repeated_message.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    message = [""] * len(lines[0].strip())
    for line in lines:
        for i, char in enumerate(line.strip()):
            message[i] += char

    print("".join([max(set(char), key=char.count) for char in message]))

    end_timep1 = time.time()
    print("took in seconds", end_timep1 - start_time)
    print("took in ms", (end_timep1 - start_time) * 1000)

    print("".join([min(set(char), key=char.count) for char in message]))

    end_timep2 = time.time()
    print("took in seconds", end_timep2 - end_timep1)
    print("took in ms", (end_timep2 - end_timep1) * 1000)


if __name__ == "__main__":
    main()
