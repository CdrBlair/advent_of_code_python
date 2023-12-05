import os
import time
from hmac import new


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/seed_maps.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    seed_line = lines.pop(0)
    seeds = [int(num) for num in seed_line.split(":")[1].strip().split(" ")]

    map_inst = {}
    current_map_name = ""

    lines.pop(0)
    for line in lines:
        if ":" in line:
            current_map_name = line.split(" ")[0].strip()
            map_inst[current_map_name] = []
        elif line.strip():
            current_mappings = tuple(int(num) for num in line.split(" "))
            map_inst[current_map_name].append(current_mappings)

    locations = []

    for seed in seeds:
        current_value = seed
        for map_name, mappings in map_inst.items():
            current_value = check_seed(current_value, mappings)

        location = current_value

        locations.append(location)

    min_location = min(locations)
    print("Min location: ", min_location)
    end_time_p1 = time.time()
    print("Time taken part 1: ", end_time_p1 - start_time)
    print("Time taken in ms part 1: ", (end_time_p1 - start_time) * 1000)

    seed_pairs = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds) - 1, 2)]

    location_range = []
    for pair in seed_pairs:
        current_range = pair
        current_ranges = []
        current_ranges.append(current_range)
        itermediate_ranges = []
        for map_name, mappings in map_inst.items():
            for current_range in current_ranges:
                itermediate_ranges.extend(convert_range(current_range, mappings))

            current_ranges = itermediate_ranges.copy()
            itermediate_ranges.clear()

        location_range.extend(current_ranges)

    min_location = min(num[0] for num in location_range)
    print("Min location part 2: ", min_location)

    end_time_p2 = time.time()
    print("Time taken part 2: ", end_time_p2 - end_time_p1)
    print("Time taken in ms part 2: ", (end_time_p2 - end_time_p1) * 1000)
    print("Time taken total: ", end_time_p2 - start_time)
    print("Time taken in ms total: ", (end_time_p2 - start_time) * 1000)


# Reverse Mapping
def reverse_mapping(input, mappings):
    for mapping in mappings:
        source = mapping[1]
        target = mapping[0]
        range_map = mapping[2]
        if target <= input <= target + range_map - 1:
            return source + input - target

    return input


# Check if seed is in any mappings, if yes return mapped number, else return seed
def check_seed(seed, mappings):
    for mapping in mappings:
        source = mapping[1]
        target = mapping[0]
        range_map = mapping[2]
        if source <= seed <= source + range_map - 1:
            return target + seed - source

    return seed


# Convert input range to new list of ranges according to mapping
def convert_range(range, mappings_input):
    mappings = mappings_input.copy()
    mappings.sort(key=lambda x: x[1])
    new_ranges = []
    within_ranges = []
    outside_ranges = []
    start_of_range = range[0]
    end_of_range = range[0] + range[1] - 1

    i = 0

    while start_of_range <= end_of_range and i < len(mappings):
        if mappings[i][1] <= start_of_range <= mappings[i][1] + mappings[i][2] - 1:
            if end_of_range <= mappings[i][1] + mappings[i][2] - 1:
                within_ranges.append(
                    (start_of_range, end_of_range - start_of_range + 1)
                )
                start_of_range = end_of_range + 1
            else:
                within_ranges.append(
                    (
                        start_of_range,
                        mappings[i][1] + mappings[i][2] - start_of_range + 1,
                    )
                )
                start_of_range = mappings[i][1] + mappings[i][2]
        elif i + 1 < len(mappings) and start_of_range < mappings[i + 1][1]:
            if end_of_range < mappings[i + 1][1]:
                outside_ranges.append(
                    (start_of_range, end_of_range - start_of_range + 1)
                )
                start_of_range = end_of_range + 1
            else:
                outside_ranges.append(
                    (start_of_range, mappings[i + 1][1] - start_of_range + 1)
                )
                start_of_range = mappings[i + 1][1]
        elif i + 1 == len(mappings):
            outside_ranges.append((start_of_range, end_of_range - start_of_range + 1))
            start_of_range = end_of_range + 1
        i += 1

    for within_range in within_ranges:
        new_ranges.append((check_seed(within_range[0], mappings), within_range[1]))

    if len(outside_ranges) > 0:
        new_ranges.extend(outside_ranges)

    return new_ranges


if __name__ == "__main__":
    main()
