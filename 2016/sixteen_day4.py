import os
import re
import time
from collections import Counter


def main():
    start_time = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/rooms.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path) as f:
        lines = f.readlines()

    rooms = []

    for line in lines:
        line = line.strip()
        room = line.split("[")
        checksum = room[1].strip("]")
        room_segments_and_id = room[0].split("-")
        sector_id = room_segments_and_id[-1]
        room_segments = room_segments_and_id[:-1]
        room_name = "".join(room_segments)
        rooms.append((room_name, sector_id, checksum))

    total_sec_id = 0

    for room in rooms:
        if check_if_real_room(room):
            total_sec_id += int(room[1])
            if decrypt_room(room).__contains__("northpole"):
                print(room)

    print(total_sec_id)
    print("took", time.time() - start_time, "seconds")
    print("took in ms", (time.time() - start_time) * 1000, "milliseconds")


def decrypt_room(room):
    room_name, sector_id, checksum = room
    decrypted_name = ""
    for char in room_name:
        decrypted_name += shift_char(char, int(sector_id))
    return decrypted_name


def shift_char(char, shift):
    """Shifts a character forward through the alphabet, circulating when hitting 'z'.

    Args:
      char: The character to shift.
      shift: The number of positions to shift forward.

    Returns:
      The shifted character.
    """
    start = ord("a")
    shifted_ord = ord(char) + shift
    while shifted_ord > ord("z"):
        shifted_ord -= 26
    return chr(shifted_ord)


def check_if_real_room(room):
    room_name, sector_id, checksum = room
    char_counts = Counter(room_name)
    char_counts = char_counts.most_common()
    sorted_chars = sorted(char_counts, key=lambda item: (-item[1], item[0]))
    sorted_chars = sorted_chars[:5]
    concat_chars = "".join([item[0] for item in sorted_chars])
    # print(concat_chars)
    # print(checksum)
    # print(sorted_chars)

    return concat_chars == checksum


if __name__ == "__main__":
    main()
