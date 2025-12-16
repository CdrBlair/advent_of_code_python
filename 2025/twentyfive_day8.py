# Main method
import os
import time


def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day8.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        junctionBoxes = {}
        i = 0
        for line in lines:
            line = line.strip()
            parts = line.split(",")
            junctionBoxes[i] = (int(parts[0]), int(parts[1]), int(parts[2]))
            i += 1

    junctionBoxesPairs = []
    for i in range(len(junctionBoxes)):
        for j in range(i + 1, len(junctionBoxes)):
            if junctionBoxes[i] == junctionBoxes[j]:
                continue
            dist = calcDistance(junctionBoxes[i], junctionBoxes[j])
            junctionBoxesPairs.append((dist, i, j))

    # sort by distance
    junctionBoxesPairs.sort(key=lambda x: x[0])

    circuitConnections = []
    numberOfConnections = 1000
    count = 0
    for pair in junctionBoxesPairs:
        # print("Processing pair: ", pair)
        inOneCircuit = False
        dist, box1, box2 = pair
        for connection in circuitConnections:
            if box1 in connection and box2 in connection:
                inOneCircuit = True
                break
            elif box1 in connection or box2 in connection:
                for con2 in circuitConnections:
                    if con2 != connection and (box1 in con2 or box2 in con2):
                        connection.update(con2)
                        circuitConnections.remove(con2)
                        break
                    else:
                        if box1 in connection:
                            connection.add(box2)
                        else:
                            connection.add(box1)
                inOneCircuit = True
                break

        if inOneCircuit:
            # print(circuitConnections)
            count += 1
            if count >= numberOfConnections:
                break

            continue
        else:
            circuitConnections.append(set([box1, box2]))
        count += 1
        # print(circuitConnections)
        if count >= numberOfConnections:
            break

    # print("Number of circuits: ", len(circuitConnections))
    # print(circuitConnections)
    sizes = [len(circuit) for circuit in circuitConnections]
    # sort big to small
    sizes.sort(reverse=True)
    # print("Sizes of circuits: ", sizes)

    checksum = 1
    for size in sizes[:3]:
        checksum *= size
    print("Checksum (product of sizes of 3 largest circuits): ", checksum)

    endP1 = time.time()
    print("part 1:", endP1 - start_time)
    print("part 1 time in ms:", (endP1 - start_time) * 1000)

    circuitConnections = []
    for pair in junctionBoxesPairs:
        # print("Processing pair: ", pair)
        inOneCircuit = False
        dist, box1, box2 = pair
        for connection in circuitConnections:
            if box1 in connection and box2 in connection:
                inOneCircuit = True
                break
            elif box1 in connection or box2 in connection:
                for con2 in circuitConnections:
                    if con2 != connection and (box1 in con2 or box2 in con2):
                        connection.update(con2)
                        circuitConnections.remove(con2)
                        break
                    else:
                        if box1 in connection:
                            connection.add(box2)
                        else:
                            connection.add(box1)
                inOneCircuit = True
                break

        if inOneCircuit:
            # print(circuitConnections)
            if len(circuitConnections) == 1 and len(circuitConnections[0]) == len(
                junctionBoxes
            ):
                result = junctionBoxes[box1][0] * junctionBoxes[box2][0]
                # print(circuitConnections)
                # print(junctionBoxes)
                # print(result)
                break
            continue
        else:
            circuitConnections.append(set([box1, box2]))
        # print(circuitConnections)
        if len(circuitConnections) == 1 and len(circuitConnections[0]) == len(
            junctionBoxes
        ):
            result = box1[0] * box2[0]
            # print(circuitConnections)
            # print(junctionBoxes)
            # print(result)
            break

    print(result)
    endP2 = time.time()
    print("part 2:", endP2 - endP1)
    print("part 2 time in ms:", (endP2 - endP1) * 1000)


# Euclidean distance in 3D
def calcDistance(box1, box2):
    # print(box1, box2)
    dist = 0
    for i in range(3):
        dist += (box1[i] - box2[i]) ** 2
    return dist**0.5


if __name__ == "__main__":
    main()
