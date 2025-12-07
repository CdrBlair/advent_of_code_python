import time


def main():

    starttime = time.time()

    state = "10011111011011001"
    diskSize = 35651584

    while len(state) < diskSize:
        state = dragoncurve(state)

    # print(state)
    print(len(state))
    if len(state) > diskSize:
        state = state[:diskSize]
    # print(state)
    print(len(state))

    checksum = calcchecksum(state)

    print("Final checksum: ", checksum)
    endTime = time.time()
    print("Time taken: ", endTime - starttime)
    print("Time taken in ms: ", (endTime - starttime) * 1000)


def calcchecksum(state):
    checksum = state

    while len(checksum) % 2 == 0 or len(checksum) == len(state):
        parts = []
        for i in range(0, len(checksum), 2):
            pair = checksum[i : i + 2]
            if pair[0] == pair[1]:
                parts.append("1")
            else:
                parts.append("0")

        checksum = "".join(parts)
        # print(checksum)
    return checksum


def dragoncurve(state):
    trans = str.maketrans("01", "10")
    b = state[::-1].translate(trans)
    return state + "0" + b


if __name__ == "__main__":
    main()
