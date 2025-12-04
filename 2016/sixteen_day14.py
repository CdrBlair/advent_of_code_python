import hashlib
import re
import time
from functools import lru_cache


def main():
    start_time = time.time()

    salt = "ihaygndm"
    hashes = []
    index = 0
    keys = set()
    while len(keys) < 64:
        if index >= len(hashes):
            hash = hashlib.md5((salt + str(index)).encode()).hexdigest()
            hashes.append(hash)
        else:
            hash = hashes[index]

        # Check for triplet
        triplet = re.search(r"(.)\1\1", hash)
        if triplet:
            for j in range(index + 1, index + 1001):
                if j >= len(hashes):
                    next_hash = hashlib.md5((salt + str(j)).encode()).hexdigest()
                    hashes.append(next_hash)
                else:
                    next_hash = hashes[j]
                if re.search(r"(" + triplet.group(1) + r")\1\1\1\1", next_hash):
                    keys.add(index)
                    break
        index += 1
    print("Part 1: ", index - 1)
    endP1 = time.time()
    print("Time Part 1: ", endP1 - start_time)
    print("Time P1 in ms: ", (endP1 - start_time) * 1000)

    salt = "ihaygndm"
    hashes = []
    index = 0
    keys = set()
    while len(keys) < 64:
        if index >= len(hashes):
            hash = hashlib.md5((salt + str(index)).encode()).hexdigest()
            hash = hashstreching(hash)
            hashes.append(hash)
        else:
            hash = hashes[index]

        # Check for triplet
        triplet = re.search(r"(.)\1\1", hash)
        if triplet:
            for j in range(index + 1, index + 1001):
                if j >= len(hashes):
                    next_hash = hashlib.md5((salt + str(j)).encode()).hexdigest()
                    next_hash = hashstreching(next_hash)
                    hashes.append(next_hash)
                else:
                    next_hash = hashes[j]
                if re.search(r"(" + triplet.group(1) + r")\1\1\1\1", next_hash):
                    keys.add(index)
                    break
        index += 1

    print("Part 2: ", index - 1)
    endP2 = time.time()
    print("Time Part 2: ", endP2 - endP1)
    print("Time P2 in ms: ", (endP2 - endP1) * 1000)


def hashstreching(hash):
    for _ in range(2016):
        hash = hashlib.md5(hash.encode()).hexdigest()
    return hash


if __name__ == "__main__":
    main()
