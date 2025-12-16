# Main method


import os
import time
from collections import deque
from functools import lru_cache

devicesglobal = {}
count = 0


def main():
    global devicesglobal
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day11.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    devices = {}
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            parts = line.split(":")
            device_name = parts[0].strip()
            outputs = [x for x in parts[1].strip().split(" ")]

            devices[device_name] = outputs
    # print("Devices: ", devices)
    start_device = "you"
    end_device = "out"
    all_paths = findAllpaths(devices, start_device, end_device)
    # print(f"All paths from {start_device} to {end_device}:")
    # for path in all_paths:
    #     print(" -> ".join(path))
    print("Total paths found: ", len(all_paths))
    end_timeP1 = time.time()
    print("Part 1 took ", end_timeP1 - start_time, " seconds")
    print("Part 1 took in ms: ", (end_timeP1 - start_time) * 1000)

    devicesglobal = devices
    start = "svr"
    end = "fft"
    total_paths_count_svr_fft = count_paths(start, end, ignore_device="dac")
    # print(f"Total number of paths from {start} to {end}: {total_paths_count_svr_fft}")
    end = "dac"
    total_paths_count_svr_dac = count_paths(start, end, ignore_device="fft")
    # print(f"Total number of paths from {start} to {end}: {total_paths_count_svr_dac}")

    start = "fft"
    end = "dac"
    total_paths_count_fft_dac = count_paths(start, end, ignore_device=None)
    # print(f"Total number of paths from {start} to {end}: {total_paths_count_fft_dac}")

    start = "dac"
    end = "fft"
    total_paths_count_dac_fft = count_paths(start, end, ignore_device=None)
    # print(f"Total number of paths from {start} to {end}: {total_paths_count_dac_fft}")

    start = "dac"
    end = "out"
    total_paths_count_dac_out = count_paths(start, end, ignore_device=None)
    # print(f"Total number of paths from {start} to {end}: {total_paths_count_dac_out}")
    # print("cache info: ", count_paths.cache_info())
    # print("cache parameters: ", count_paths.cache_parameters())

    # total number of paths from svr to out over fft and dac knowing that there is no way from dac to fft
    total = (
        total_paths_count_svr_fft
        * total_paths_count_fft_dac
        * total_paths_count_dac_out
    )
    print("Total number of paths from svr to out: ", total)
    end_timeP2 = time.time()
    print("Part 2 took ", end_timeP2 - end_timeP1, " seconds")
    print("Part 2 took in ms: ", (end_timeP2 - end_timeP1) * 1000)


def findAllpaths(devices, start_device, end_device):
    # BFS to find all paths from start_device to end_device
    queue = deque([(start_device, [start_device])])
    all_paths = []
    while queue:
        (current_device, path) = queue.popleft()
        # print("Current device: ", current_device, " Path: ", path)
        for next_device in devices.get(current_device, []):
            if next_device in path:
                continue
            if next_device == end_device:
                all_paths.append(path + [next_device])
            else:
                queue.append((next_device, path + [next_device]))
    return all_paths


@lru_cache
def count_paths(current_device, end_device, ignore_device):
    devices = devicesglobal

    if current_device == end_device:
        return 1
    total_paths = 0
    for next_device in devices.get(current_device, []):
        if next_device == ignore_device:
            continue
        total_paths += count_paths(next_device, end_device, ignore_device)
        # print(total_paths)
    return total_paths


if __name__ == "__main__":
    main()
