# Main method

import os
import time
from collections import deque
from typing import List, Tuple

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day10.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        machines = []
        for line in lines:
            line = line.strip()
            linesplitted = line.split(" ")
            lights = linesplitted[0]
            buttons = []
            for i in range(1, len(linesplitted)):

                if linesplitted[i].startswith("("):
                    splittedButtopns = (
                        linesplitted[i].removeprefix("(").removesuffix(")").split(",")
                    )
                    buttonList = []
                    for button in splittedButtopns:
                        buttonList.append(int(button))
                    buttons.append(buttonList)
                else:
                    intermediate = linesplitted[i].removeprefix("{").removesuffix("}")
                    joltages = [int(x) for x in intermediate.split(",")]
            machines.append((lights, buttons, joltages))
    # print("Machines: ", machines)

    totalSum = 0
    for machine in machines:
        lights, buttons, joltages = machine
        lights = lights.removeprefix("[").removesuffix("]")
        # print("Solving machine with lights: ", lights)
        vectors = []
        for button in buttons:
            vector = tuple(1 if i in button else 0 for i in range(len(lights)))
            vectors.append(vector)
        target = tuple(1 if c == "#" else 0 for c in lights)
        # print("Vectors: ", vectors)
        # print("Target: ", target)
        result = find_min_combination(vectors, target)
        # if result is not None:
        #     print("Button presses for lights ", lights, ": ", result)
        # else:
        #     print("No solution found for lights ", lights)
        totalSum += sum(result) if result is not None else 0
    print("Total sum of button presses: ", totalSum)

    endP1 = time.time()
    print("Part 1 took ", endP1 - start_time, " seconds")
    print("Part 1 took in ms: ", (endP1 - start_time) * 1000)

    totalSumJoltage = 0
    for machine in machines:
        lights, buttons, joltages = machine

        # print("Solving machine with joltages: ", joltages)
        vectors = []
        for button in buttons:
            vector = tuple(1 if i in button else 0 for i in range(len(joltages)))
            vectors.append(vector)
        target = tuple(joltages)
        # print("Vectors: ", vectors)
        # print("Target: ", target)
        result = find_min_combinationJoltages_ILP(vectors, target)
        # if result is not None:
        #     print("Button presses for Joltages ", joltages, ": ", result)
        # else:
        #     print("No solution found for joltages ", joltages)
        # print(result)
        totalSumJoltage += sum(result) if result is not None else 0
        # print("Intermediate total joltage sum: ", totalSumJoltage)

    print("Total sum of button presses for joltage: ", totalSumJoltage)
    endTime = time.time()
    print("Part 2 took ", endTime - endP1, " seconds")
    print("Part 2 took in ms: ", (endTime - endP1) * 1000)


def find_min_combination(
    buttons: List[Tuple[int, ...]], targetLight: Tuple[int, ...]
) -> List[int]:
    """
    Find minimum combination of vectors that sum to target (mod 2).
    Returns list of counts for each vector.
    """
    n = len(buttons)
    dim = len(targetLight)

    # BFS: queue stores (current_state, coefficients)
    queue = deque([(tuple([0] * dim), [0] * n)])
    visited = {tuple([0] * dim): 0}  # state -> min steps to reach

    while queue:
        current, coefs = queue.popleft()

        if current == targetLight:
            return coefs

        current_sum = sum(coefs)

        # Try adding each vector
        for i in range(n):
            new_state = tuple((current[j] + buttons[i][j]) % 2 for j in range(dim))
            new_coefs = coefs.copy()
            new_coefs[i] += 1
            new_sum = current_sum + 1

            if new_state not in visited or visited[new_state] > new_sum:
                visited[new_state] = new_sum
                queue.append((new_state, new_coefs))

    return None  # No solution found


def find_min_combinationJoltages_ILP(
    buttons: List[Tuple[int, ...]], targetJoltage: Tuple[int, ...]
) -> List[int]:
    """
    Solve as Integer Linear Program: minimize sum(x) subject to Ax = target
    """
    n = len(buttons)
    dim = len(targetJoltage)

    # Coefficient matrix: each column is a button vector
    A = np.array(buttons).T
    b = np.array(targetJoltage)

    # Objective: minimize sum of all button presses
    c = np.ones(n)

    constraints = LinearConstraint(A, b, b)
    bounds = Bounds(0, np.inf)

    res = milp(c, constraints=constraints, bounds=bounds, integrality=np.ones(n))

    # Verify the solution
    verification = A @ res.x

    # Check if solution is actually correct
    is_correct = np.allclose(verification, b, atol=1e-6)
    # print(f"Solution is correct: {is_correct}")
    # print sum with and without rounding
    # if any(res.x[i] != round(res.x[i]) for i in range(len(res.x))):
    #     print(f"Sum of solution (rounded): {np.sum(np.round(res.x))}")
    #     print(f"Sum of solution (unrounded): {np.sum(res.x)}")
    #     for i in range(len(res.x)):
    #         print(f"Button {i}: {res.x[i]}")
    if res.success and is_correct:
        # round results to nearest integer other wise 0.999... is a problem...
        return [int(np.round(x)) for x in res.x]

    print("ILP failed or incorrect, falling back to A*")
    return None


if __name__ == "__main__":
    main()
