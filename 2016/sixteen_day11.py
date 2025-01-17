import os
import time


def main():
    start_time = time.time()
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/radioisotope_generators.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    floors = [[], [], [], []]
    elevator = 0

    for i, line in enumerate(lines):
        parts = line.strip().split(" a ")
        for part in parts[1:]:
            if "microchip" in part:
                floors[i].append(part.split("-compatible")[0] + "M")
            elif "generator" in part:
                floors[i].append(part.split(" ")[0] + "G")
    print(floors)

    def is_valid(floors):
        for floor in floors:
            gens = [item for item in floor if item.endswith("G")]
            chips = [item for item in floor if item.endswith("M")]
            if gens and any(chip[:-1] + "G" not in gens for chip in chips):
                return False
        return True

    def get_possible_moves(floors, elevator):
        items = floors[elevator]
        moves = []
        for i in range(len(items)):
            for j in range(i, len(items)):
                for direction in [-1, 1]:
                    new_elevator = elevator + direction
                    if 0 <= new_elevator < len(floors):
                        new_floors = [floor[:] for floor in floors]
                        new_floors[elevator].remove(items[i])
                        new_floors[new_elevator].append(items[i])
                        if i != j:
                            new_floors[elevator].remove(items[j])
                            new_floors[new_elevator].append(items[j])
                        if is_valid(new_floors):
                            moves.append((new_floors, new_elevator))
        return moves

    def bfs(floors, elevator):
        queue = [(floors, elevator, 0)]
        visited = set()
        while queue:
            current_floors, current_elevator, steps = queue.pop(0)
            if all(len(floor) == 0 for floor in current_floors[:-1]):
                return steps
            state = (
                tuple(tuple(sorted(floor)) for floor in current_floors),
                current_elevator,
            )
            if state in visited:
                continue
            visited.add(state)
            for new_floors, new_elevator in get_possible_moves(
                current_floors, current_elevator
            ):
                queue.append((new_floors, new_elevator, steps + 1))
        return -1

    print("Minimum steps:", bfs(floors, elevator))
    end_time = time.time()
    print("Time taken:", end_time - start_time)
    print("Time taken in ms:", (end_time - start_time) * 1000)


if __name__ == "__main__":
    main()
