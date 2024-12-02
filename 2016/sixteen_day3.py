import os
import re
import time


def main():
    start_time = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/triangles.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    triangles = []

    for line in lines:

        numbers = re.split(r"\s+", line.strip())
        print(numbers)

        triangles.append(tuple(int(num) for num in numbers))

    # We filter the list of triangles
    # print(triangles)
    triangles = list(filter(isTriangle, triangles))

    print("number of true triangles is", len(triangles))
    end_time = time.time()
    print("took ", end_time - start_time)
    print("took in ms", (end_time - start_time) * 1000)

    triangles = []
    n = 0
    for i in range(0, len(lines), 3):
        # For each group of three lines, we split each line and create a tuple
        numbers = [re.split(r"\s+", line.strip()) for line in lines[i : i + 3]]
        triangles.append(tuple(int(num[0]) for num in numbers))
        triangles.append(tuple(int(num[1]) for num in numbers))
        triangles.append(tuple(int(num[2]) for num in numbers))

    print(triangles)

    # We filter the list of triangles
    triangles = list(filter(isTriangle, triangles))
    print("number of true triangles is", len(triangles))
    end_time = time.time()
    print("took ", end_time - start_time)
    print("took in ms", (end_time - start_time) * 1000)


# Function to check if a tuple represents a valid triangle
def isTriangle(possible_triangle: tuple) -> bool:
    # Check if the sum of the first two sides is greater than the third side
    if not possible_triangle[0] + possible_triangle[1] > possible_triangle[2]:
        return False
    # Check if the sum of the first and third sides is greater than the second side
    if not possible_triangle[0] + possible_triangle[2] > possible_triangle[1]:
        return False
    # Check if the sum of the second and third sides is greater than the first side
    if not possible_triangle[1] + possible_triangle[2] > possible_triangle[0]:
        return False

    # If all conditions are met, the tuple represents a valid triangle
    return True


if __name__ == "__main__":
    main()
