import os
import time


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2023/hail.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    positions = {}
    speeds = {}
    for i, line in enumerate(lines):
        line = line.strip()
        pos, speed = line.split("@")
        positions[i] = tuple(map(int, pos.split(",")))
        speeds[i] = tuple(map(int, speed.split(",")))

    # for key in positions:
    #     print(positions[key], speeds[key])

    minRange = 200000000000000
    maxRange = 400000000000000
    # minRange = 7
    # maxRange = 27
    intersects = []
    for key in positions:
        if key + 1 not in positions:
            continue
        for key2 in range(key + 1, len(positions)):
            x1 = positions[key][0]
            y1 = positions[key][1]
            x2 = positions[key2][0]
            y2 = positions[key2][1]

            vx1 = speeds[key][0]
            vy1 = speeds[key][1]
            vx2 = speeds[key2][0]
            vy2 = speeds[key2][1]

            # print(x1, y1, x2, y2, vx1, vy1, vx2, vy2)
            # Calculate t1
            if vx1 * vy2 - vx2 * vy1 != 0:
                t2 = (vy1 * (x2 - x1) + vx1 * (y1 - y2)) / ((vx1 * vy2) - (vx2 * vy1))
                t1 = (x2 + (vx2 * t2) - x1) / vx1

                # calculate intersect points
                ix1 = x1 + vx1 * t1
                iy1 = y1 + vy1 * t1
                ix2 = x2 + vx2 * t2
                iy2 = y2 + vy2 * t2

                # print(ix1, iy1)
                # print(ix2, iy2)

                # print(t1, t2)

                if (
                    minRange <= ix1 <= maxRange
                    and minRange <= iy1 <= maxRange
                    and t1 > 0
                    and t2 > 0
                ):
                    intersects.append((key, ix1, iy1))

    print(len(intersects))
    endtimeP1 = time.time()
    print("Part 1 took: ", endtimeP1 - start_time)
    print("Part 1 in ms: ", (endtimeP1 - start_time) * 1000)

    searchMin = -1000
    searchMax = 1000

    key = 0

    for vx0 in range(searchMin, searchMax + 1):
        for vy0 in range(searchMin, searchMax + 1):
            # print(x1, y1, x2, y2, vx1, vy1, vx2, vy2)
            # Calculate t1
            found = True

            for key2 in range(key + 1, len(positions)):
                x1 = positions[key][0]
                y1 = positions[key][1]
                x2 = positions[key2][0]
                y2 = positions[key2][1]

                vx1 = speeds[key][0]
                vy1 = speeds[key][1]
                vx2 = speeds[key2][0]
                vy2 = speeds[key2][1]
                vx1delta = vx1 - vx0
                vy1delta = vy1 - vy0
                vx2delta = vx2 - vx0
                vy2delta = vy2 - vy0

                if vx1delta * vy2delta - vx2delta * vy1delta != 0 and vx1delta != 0:
                    t2 = (vy1delta * (x2 - x1) + vx1delta * (y1 - y2)) / (
                        (vx1delta * vy2delta) - (vx2delta * vy1delta)
                    )
                    t1 = (x2 + (vx2delta * t2) - x1) / vx1delta
                    # calculate intersect points
                    ix1 = x1 + vx1delta * t1
                    iy1 = y1 + vy1delta * t1
                    ix2 = x2 + vx2delta * t2
                    iy2 = y2 + vy2delta * t2

                    if key2 == 1:
                        currentIntersectX = ix1
                        currentIntersectY = iy1
                        intersectingt1 = t1
                    else:
                        if ix1 != currentIntersectX or iy1 != currentIntersectY:
                            found = False
                            break
                elif vx1delta == 0:
                    found = False

            if found:
                x0 = ix1
                y0 = iy1

                break
        if found:
            break

    # print(x0, y0, vx0, vy0, intersectingt1)

    # now search for z
    # l0+vot = l1+v1t
    # z0 = z1 + vz1t - vz0t
    #
    key = 0
    intersectingTimeKey = (x0 - positions[key][0]) / (speeds[key][0] - vx0)
    for vxz in range(searchMin, searchMax + 1):
        # print(vxz)
        # z for key
        vz1delta = speeds[key][2] - vxz
        iz = positions[key][2] + vz1delta * intersectingTimeKey
        found = True
        for key2 in range(key + 1, len(positions)):
            # calculate intersecting time for key2 from x0 = x1 + vx1t- vx0t
            intersectingTimeKey2 = (x0 - positions[key2][0]) / (speeds[key2][0] - vx0)

            vz2delta = speeds[key2][2] - vxz
            # z for key2
            iz1 = positions[key2][2] + vz2delta * intersectingTimeKey2

            if iz != iz1:
                found = False
                break
        if found:
            z0 = iz

            break

    print(x0, y0, z0, vx0, vy0, vxz)
    print("Sum of coordinates: ", x0 + y0 + z0)
    print("Part 2 took: ", time.time() - endtimeP1)
    print("Part 2 in ms: ", (time.time() - endtimeP1) * 1000)
    print("Total time: ", time.time() - start_time)
    print("Total time in ms: ", (time.time() - start_time) * 1000)


if __name__ == "__main__":
    main()
