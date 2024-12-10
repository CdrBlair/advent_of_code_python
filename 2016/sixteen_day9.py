import os
import time


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/compressed_file.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        line = file.readline().strip()

    i = 0
    newline = ""
    while i < len(line):
        if line[i] == "(":
            end = line.index(")", i)
            length, repeat = map(int, line[i + 1 : end].split("x"))
            i = end + 1
            newline += line[i : i + length] * repeat
            i += length
        else:
            newline += line[i]
            i += 1

    print(len(newline))
    endtimep1 = time.time()
    print("Part 1 time:", endtimep1 - start_time)
    print("Part 1 time in ms:", (endtimep1 - start_time) * 1000)

    print(decompress(line))
    print("Part 2 time:", time.time() - endtimep1)
    print("Part 2 time in ms:", (time.time() - endtimep1) * 1000)


def decompress(line):
    i = 0
    decompressedLength = 0
    while i < len(line):
        if line[i] == "(":
            end = line.index(")", i)
            length, repeat = map(int, line[i + 1 : end].split("x"))
            i = end + 1
            decompressedLength += decompress(line[i : i + length]) * repeat
            i += length
        else:
            decompressedLength += 1
            i += 1

    return decompressedLength


if __name__ == "__main__":
    main()
