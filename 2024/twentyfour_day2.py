import os
import time


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/nuclearreports.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    reports = []
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            report = line.split(" ")
            report = [int(x) for x in report]
            reports.append(report)
    sumSafereports = 0
    unsafeReports = []
    for report in reports:
        if isReporSafe(report):
            sumSafereports += 1
        else:
            unsafeReports.append(report)

    print(sumSafereports)
    endtime = time.time()
    print("Time part 1: ", endtime - start_time)
    print("Time part 1 in ms: ", (endtime - start_time) * 1000)

    nowSafe = 0
    for unsafe in unsafeReports:
        # remove 1 level at a time
        for i in range(len(unsafe)):
            if isReporSafe(unsafe[:i] + unsafe[i + 1 :]):
                nowSafe += 1
                break
    print(nowSafe + sumSafereports)
    print("Time part 2: ", time.time() - endtime)
    print("Time part 2 in ms: ", (time.time() - endtime) * 1000)


def isReporSafe(report):
    diffs = [report[i] - report[i + 1] for i in range(len(report) - 1)]
    if all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs):
        return all(abs(diff) < 4 for diff in diffs)
    return False

    return False


if __name__ == "__main__":
    main()
