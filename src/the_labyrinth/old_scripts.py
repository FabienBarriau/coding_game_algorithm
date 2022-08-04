import math
import random
import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]

inverse_direction_mapping = {
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
    "UP": "DOWN",
    "DOWN": "UP",
}


class AlreadySeen:
    def __init__(self):
        self.previous_intersection = None
        self.previous_direction_at_intersection = None
        self.already_visited_path_from_direction = dict()

    def update(self, actual_coord, node_degree, direction):
        if node_degree > 2:
            self.previous_intersection = actual_coord
            self.previous_direction_at_intersection = direction
        if node_degree == 1 & (self.previous_intersection is not None):
            if self.previous_intersection in self.already_visited_path_from_direction:
                self.already_visited_path_from_direction[
                    self.previous_intersection
                ].add(self.previous_direction_at_intersection)
            else:
                self.already_visited_path_from_direction[self.previous_intersection] = {
                    self.previous_direction_at_intersection
                }

    def __repr__(self):
        return str(
            {
                "inter": self.previous_intersection,
                "dir": self.previous_direction_at_intersection,
                "visited": self.already_visited_path_from_direction,
            }
        )


class Graph:
    def __init__(self, root):
        self.root = root
        self.edges = dict()

    def update(self, actual_coord, direction):
        next_coord = None
        print("agde", file=sys.stderr, flush=True)
        if direction == "RIGHT":
            next_coord = (actual_coord[0], actual_coord[1] + 1)
        if direction == "LEFT":
            next_coord = (actual_coord[0], actual_coord[1] - 1)
        if direction == "UP":
            next_coord = (actual_coord[0] - 1, actual_coord[1])
        if direction == "DOWN":
            next_coord = (actual_coord[0] + 1, actual_coord[1])

        if next_coord in self.edges:
            self.edges[next_coord].add((actual_coord, direction))
        else:
            self.edges[next_coord] = {(actual_coord, direction)}

    def compute_path_to_root(self, actual_coord):
        def loop(actual_node, path_to_root, already_visited):
            while True:
                if self.edges.get(actual_node) is None:
                    break
                for new_node, direction in self.edges[actual_node]:
                    if new_node in already_visited:
                        break
                    already_visited.add(new_node)
                    new_path = path_to_root + [direction]
                    if new_node == self.root:
                        return new_path
                    else:
                        return loop(new_node, new_path, already_visited)
                break

        return loop(actual_coord, [], set())


def scan_possible_directions(actual_coord, scan):
    y, x = actual_coord
    forbiden_direction = set()
    if scan[y][x + 1] == "#":
        forbiden_direction.add("RIGHT")
    if scan[y][x - 1] == "#":
        forbiden_direction.add("LEFT")
    if scan[y + 1][x] == "#":
        forbiden_direction.add("DOWN")
    if scan[y - 1][x] == "#":
        forbiden_direction.add("UP")

    return {"RIGHT", "LEFT", "UP", "DOWN"}.symmetric_difference(forbiden_direction)


def choose_direction(
    possible_directions, previous_direction, already_visited_directions
):
    print("possible_directions", file=sys.stderr, flush=True)
    print(possible_directions, file=sys.stderr, flush=True)
    print("previous_direction", file=sys.stderr, flush=True)
    print(previous_direction, file=sys.stderr, flush=True)
    print("already_visited_directions", file=sys.stderr, flush=True)
    print(already_visited_directions, file=sys.stderr, flush=True)
    direction = None
    inverse_previous_direction = inverse_direction_mapping.get(previous_direction)
    temp = possible_directions.copy()
    if len(temp) == 1:
        direction = temp.pop()
    if len(temp) == 2:
        if previous_direction is not None:
            temp.remove(inverse_previous_direction)
        direction = temp.pop()
    if len(temp) > 2:
        test = already_visited_directions.union({inverse_previous_direction})
        print("test", file=sys.stderr, flush=True)
        print(test, file=sys.stderr, flush=True)
        print("temp", file=sys.stderr, flush=True)
        print(temp, file=sys.stderr, flush=True)
        if temp == test:
            direction = inverse_previous_direction
        else:
            temp = temp.difference(test)
            direction = random.choice(list(temp))
    return direction


# game loop
in_exploration = True
path_to_command = []
direction = None
count = 0
already_seen = AlreadySeen()
while True:
    # kr: row where Rick is located.
    # kc: column where Rick is located.

    kr, kc = [int(i) for i in input().split()]
    actual_coord = (kr, kc)

    if count == 0:
        graph = Graph(actual_coord)
    count += 1

    scan = []
    scan_alt = ""
    for i in range(r):
        toto = input()
        scan.append(toto)
        scan_alt += toto + "\n"
        # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).

    print(scan_alt, file=sys.stderr, flush=True)

    print(actual_coord, file=sys.stderr, flush=True)

    on_command = scan[actual_coord[0]][actual_coord[1]] == "C"
    in_exploration = in_exploration & (not on_command)

    if on_command:
        print("on_comand", file=sys.stderr, flush=True)
        return_path_list = graph.compute_path_to_root(actual_coord)
        print("return_path_list", file=sys.stderr, flush=True)
        print(return_path_list, file=sys.stderr, flush=True)
        return_path = iter(return_path_list)

    if in_exploration:
        print("exploration", file=sys.stderr, flush=True)
        possible_directions = scan_possible_directions(actual_coord, scan)
        direction = choose_direction(
            possible_directions,
            direction,
            already_seen.already_visited_path_from_direction.get(actual_coord, set()),
        )
        already_seen.update(actual_coord, len(possible_directions), direction)
        graph.update(actual_coord, direction)
        print(already_seen, file=sys.stderr, flush=True)
    else:
        print("retour", file=sys.stderr, flush=True)
        direction = inverse_direction_mapping[next(return_path)]

    print(direction, file=sys.stderr, flush=True)
    print(direction)
