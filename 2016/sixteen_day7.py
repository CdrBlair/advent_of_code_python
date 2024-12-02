import os
import time


def main():
    start_time = time.time()

    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/ips.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    ips = []

    for line in lines:
        outsides, hypernets = extract_strings(line.strip())

        ips.append((outsides, hypernets))

    tls_ips = []
    ssl_ips = []
    for ip in ips:
        if checkfortls(ip):
            tls_ips.append(ip)
        if checkforssl(ip):
            ssl_ips.append(ip)
    print(len(tls_ips))
    print(len(ssl_ips))

    end_timep1 = time.time()
    print("took in seconds", end_timep1 - start_time)
    print("took in ms", (end_timep1 - start_time) * 1000)


def findaba(part):
    listofabas = []
    for i, char in enumerate(part):
        if i + 2 < len(part):
            if char == part[i + 2] and char != part[i + 1]:
                listofabas.append(part[i : i + 3])
    return listofabas


def checkforssl(ip):
    outside, hypernets = ip
    abas = []
    for outside_part in outside:
        abas += findaba(outside_part)
    for aba in abas:
        bab = aba[1] + aba[0] + aba[1]
        for hypernet in hypernets:
            if bab in hypernet:
                return True
    return False


def extract_strings(s):
    inside_brackets = []
    outside_brackets = []
    temp = ""
    inside = False

    for char in s:
        if char == "[":
            if temp:
                outside_brackets.append(temp)
                temp = ""
            inside = True
        elif char == "]":
            if temp:
                inside_brackets.append(temp)
                temp = ""
            inside = False
        else:
            temp += char

    # Add the last accumulated string to the appropriate list
    if temp:
        if inside:
            inside_brackets.append(temp)
        else:
            outside_brackets.append(temp)

    return outside_brackets, inside_brackets


def checkforabba(part):
    for i, char in enumerate(part):
        if i + 3 < len(part):
            startab = part[i : i + 2]
            endab = part[i + 2 : i + 4]

            if startab == endab[::-1] and startab != endab:
                return True
    return False


def checkfortls(ip):
    outside, hypernets = ip
    for hypernet in hypernets:
        if checkforabba(hypernet):
            return False
    for outside_part in outside:
        if checkforabba(outside_part):
            return True

    return False


if __name__ == "__main__":
    main()
