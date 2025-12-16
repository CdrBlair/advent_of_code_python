# Main method

import os
import time

from matplotlib.pyplot import grid


def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2025/day12.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    shapes = {}
    grids = {}
    gridid = 0
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
        readShapes = False
        nextShape = True
        for line in lines:
            line = line.strip()

            if line.__contains__("x"):
                readShapes = True

            if not readShapes:
                if nextShape:
                    line = line.removesuffix(":")
                    shape_id = int(line)
                    shapes[shape_id] = []
                    nextShape = False
                    shapeline = 0
                    continue
                elif line == "":
                    nextShape = True
                    continue
                else:
                    for i, c in enumerate(line):
                        if c == "#":
                            shapes[shape_id].append((shapeline, i))
                    shapeline += 1
            else:
                lineParts = line.split(":")
                gridsize = tuple(map(int, lineParts[0].strip().split("x")))
                griddata = [int(x) for x in lineParts[1].strip().split(" ")]
                grids[gridid] = (gridsize, griddata)
                gridid += 1
    # print("Shapes: ", shapes)
    # print("Grids: ", grids)

    # calculate shape size and add to existing dict
    for shape_id, shape_coords in shapes.items():
        area = len(shape_coords)
        shapes[shape_id] = (shape_coords, area)
    print("Shapes with area: ", shapes)
    print(len(grids), "grids to process")

    # check if grid is possible at all
    possiblegrids = {}
    for grid_id, (gridsize, griddata) in grids.items():
        grid_area = gridsize[0] * gridsize[1]
        area_shape_total = 0
        for i, cell in enumerate(griddata):
            area_shape_total += shapes[i][1] * cell
        if area_shape_total > grid_area:
            print("Grid ", grid_id, " not possible")
        else:
            possiblegrids[grid_id] = (gridsize, griddata)
    # Apparently all grids where there is enough space are possible... :D

    print(len(possiblegrids), "possible grids to process")
    endtime = time.time()
    print("Execution time: ", endtime - start_time, "seconds")
    print("Time in ms: ", (endtime - start_time) * 1000, "ms    ")


if __name__ == "__main__":
    main()
