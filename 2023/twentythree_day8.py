import math
import os
import time
from functools import reduce

from pyparsing import one_of


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/desertmap.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    directions = [char for char in lines.pop(0).strip()]

    lines.pop(0)

    nodes = {
        line.split("=")[0].strip(): (
            line.split("=")[1]
            .strip()
            .replace("(", "")
            .replace(")", "")
            .split(",")[0]
            .strip(),
            line.split("=")[1]
            .strip()
            .replace("(", "")
            .replace(")", "")
            .split(",")[1]
            .strip(),
        )
        for line in lines
    }

    steps = 0

    if "AAA" in nodes:
        steps = calc_route("AAA", nodes, directions)

    print("Steps: ", steps)
    end_time_p1 = time.time()
    print("Time taken part 1: ", end_time_p1 - start_time)
    print("Time taken in ms part 1: ", (end_time_p1 - start_time) * 1000)

    current_nodes = [node for node in nodes if node.endswith("A")]
    end_nodes = [node for node in nodes if node.endswith("Z")]

    list_of_steps = {}
    node_start_loop = {}
    for node in current_nodes:
        current_node = node
        list_of_steps[node] = []
        visited_nodes = set()
        visited_ends = set()
        visited_nodes_lengths = {}
        loop_start = 0
        loop_length = 0

        reached_end = False
        steps_p2 = 0
        while not reached_end:
            # Normalize index for length of directions
            i = steps_p2 % len(directions)
            direction = directions[i]

            if (current_node, i) in visited_nodes:
                list_of_steps[node].append((current_node, steps_p2))
                loop_start = visited_nodes_lengths[(current_node, i)]
                loop_length = steps_p2 - loop_start
                break

            visited_nodes.add((current_node, i))
            visited_nodes_lengths[(current_node, i)] = steps_p2

            if direction == "L":
                current_node = nodes[current_node][0]
            elif direction == "R":
                current_node = nodes[current_node][1]

            steps_p2 += 1

            if current_node in end_nodes and not current_node in visited_ends:
                list_of_steps[node].append((current_node, steps_p2))
                visited_ends.add(current_node)

        # find steps loop start to end
        steps_after_end = list_of_steps[node][1][1]
        reached_end = False
        current_node = list_of_steps[node][1][0]
        while not reached_end:
            # Normalize index for length of directions
            i = steps_after_end % len(directions)
            direction = directions[i]
            if direction == "L":
                current_node = nodes[current_node][0]
            elif direction == "R":
                current_node = nodes[current_node][1]

            steps_after_end += 1
            if current_node == list_of_steps[node][0][0]:
                if steps_after_end % len(directions) == list_of_steps[node][0][1] % len(
                    directions
                ):
                    list_of_steps[node].append(
                        (current_node, steps_after_end - list_of_steps[node][1][1])
                    )
                    loop_to_Z = steps_after_end - list_of_steps[node][1][1]
                    reached_end = True

        node_start_loop[node] = (loop_start, loop_length, loop_to_Z)

    # calculate minimum steps
    numbers = [list_of_steps[node][0][1] for node in list_of_steps]
    minimum_steps = reduce(lcm, numbers)

    print("Node start loop: ", node_start_loop)

    print("Minimum steps: ", minimum_steps)
    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total in ms: ", (end_time_p2 - start_time) * 1000)


def find_smallest_A(a, b, c, d, e, f, g, h, i, j, k, l, max_value):
    smallest_A = float("inf")
    for x in range(max_value):
        for y in range(max_value):
            for z in range(max_value):
                for x1 in range(max_value):
                    for y1 in range(max_value):
                        for z1 in range(max_value):
                            A = a + x * b
                            if A != c + y * d:
                                continue
                            if A != e + z * f:
                                continue
                            if A != g + x1 * h:
                                continue
                            if A != i + y1 * j:
                                continue
                            if A != k + z1 * l:
                                continue
                            if A < smallest_A:
                                smallest_A = A
                                return smallest_A
    return smallest_A


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def diophantine(a, b, c):
    gcd, x, y = extended_gcd(b, c)
    if a % gcd != 0:
        return None  # No solution
    else:
        x *= a // gcd
        y *= a // gcd
        return x, y


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

    # BruteForce
    # steps_p2 = 0
    # reached_end = False
    # current_nodes = [node for node in nodes if node.endswith("A")]
    # while not reached_end:
    #     # Normalize index for length of directions
    #     i = steps_p2 % len(directions)
    #     direction = directions[i]
    #     next_nodes = []
    #     for node in current_nodes:
    #         if direction == "L":
    #             next_nodes.append(nodes[node][0])
    #         elif direction == "R":
    #             next_nodes.append(nodes[node][1])

    #     current_nodes = next_nodes
    #     steps_p2 += 1

    #     if any(node.endswith("Z") for node in current_nodes):
    #         print("Current Nodes: ", current_nodes)
    #     if all(node.endswith("Z") for node in current_nodes):
    #         reached_end = True

    print("Steps: ", steps_p2)
    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total in ms: ", (end_time_p2 - start_time) * 1000)


# rout calc for one node
def calc_route(node, nodes, directions):
    steps = 0
    reached_end = False
    current_node = node
    while not reached_end:
        # Normalize index for length of directions
        i = steps % len(directions)
        direction = directions[i]
        if direction == "L":
            current_node = nodes[current_node][0]
        elif direction == "R":
            current_node = nodes[current_node][1]

        steps += 1
        if current_node == "ZZZ":
            reached_end = True
    return steps


if __name__ == "__main__":
    main()
