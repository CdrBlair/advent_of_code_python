import os
import time


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/oasis.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    oasises = []
    for i, line in enumerate(lines):
        oasises.append([[]])
        oasises[i][0].extend([int(num) for num in line.strip().split(" ")])

    for oasis in oasises:
        oasis.extend(calc_deep_sequence(oasis[-1]))
        oasis[0].append(oasis[1][-1] + oasis[0][-1])
        oasis[0].insert(0, oasis[0][0] - oasis[1][0])

    sum_of_predictions_p1 = sum([oasis[0][-1] for oasis in oasises])
    sum_of_predictions_p2 = sum([oasis[0][0] for oasis in oasises])
    print("Part 1: ", sum_of_predictions_p1)
    print("Part 2: ", sum_of_predictions_p2)
    end_time_p1 = time.time()
    print("Time taken part 1+2: ", end_time_p1 - start_time)
    print("Time taken in ms part 1+2: ", (end_time_p1 - start_time) * 1000)


def calc_deep_sequence(start_sequence):
    next_sequences = []
    next_sequence = []
    for i, num in enumerate(start_sequence):
        if i + 1 < len(start_sequence):
            next_sequence.append(start_sequence[i + 1] - num)
    next_sequences.append(next_sequence)

    if all([num == 0 for num in next_sequence]):
        next_sequences[-1].append(0)
        next_sequences[-1].insert(0, 0)
        return next_sequences
    else:
        next_sequences.extend(calc_deep_sequence(next_sequences[-1]))
        next_sequences[0].append(next_sequences[1][-1] + next_sequences[0][-1])
        next_sequences[0].insert(0, next_sequences[0][0] - next_sequences[1][0])
        return next_sequences


if __name__ == "__main__":
    main()
