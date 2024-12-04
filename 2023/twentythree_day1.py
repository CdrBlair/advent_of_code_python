import os
import time

from word2number import w2n


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/trebuchet.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    print(abs_file_path)
    file = open(abs_file_path, "r")

    sum = 0

    # Loop over lines in file
    for line in file:
        sum += sum_first_last(line)

    print(sum)
    end_time = time.time()
    print("Time: ", end_time - start_time, "seconds")


# method to sum up first and last digit in string
def sum_first_last(string):
    numbers_as_text_list = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    # Find first digit loop over string
    for i in range(len(string)):
        if string[i].isdigit():
            first = int(string[i])
            break
        # else:
        #     for number in numbers_as_text_list:
        #         if string[i : i + len(number)] == number:
        #             first = w2n.word_to_num(number)
        #             break
        #     # check if first is set
        #     try:
        #         first
        #     except NameError:
        #         # do nothing
        #         pass
        #     else:
        #         break

    # Find last digit loop over string
    for i in range(len(string) - 1, -1, -1):
        if string[i].isdigit():
            last = int(string[i])
            break
        # else:
        #     for number in numbers_as_text_list:
        #         if string[i : i + len(number)] == number:
        #             last = w2n.word_to_num(number)
        #             break
        #     # check if last is set
        #     try:
        #         last
        #     except NameError:
        #         # do nothing
        #         pass
        #     else:
        #         break

    return first * 10 + last


# Call main method
if __name__ == "__main__":
    main()
