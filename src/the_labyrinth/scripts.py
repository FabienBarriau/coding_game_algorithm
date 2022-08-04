import random
import sys
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

################################################### FUNCS ###################################################

Row = int
Col = int
Scan = List[str]


class Direction(str, Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"


INVERSE_DIRECTION: Dict[Direction, Direction] = {
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,
    Direction.DOWN: Direction.UP,
    Direction.UP: Direction.DOWN,
}


class ExploratoryGraph:
    def __init__(
        self,
        start_node: Tuple[Row, Col],
        init_scan: Optional[Scan]=None,
        edges: Optional[
            Dict[Tuple[Row, Col], Set[Tuple[Tuple[Row, Col], Direction]]]
        ] = None,
    ):
        self.start_node = start_node
        self.edges: Dict[Tuple[Row, Col], Set[Tuple[Tuple[Row, Col], Direction]]] = {}
        if edges is None:
            if scan is None:
                raise ValueError("No scan provided")
            self.update_graph_with_scan(
                init_scan,
                range(start_node[0] - 2, start_node[0] + 3),
                range(start_node[1] - 2, start_node[1] + 3),
            )
        else:
            self.edges = edges

    @property
    def nodes(self) -> Set[Tuple[Row, Col]]:
        return set(self.edges.keys())

    def update_graph(self, actual_node: Tuple[Row, Col], previous_direction: Direction, scan: Scan):
        row_range, col_range = ranges_from_direction(actual_node=actual_node, direction=previous_direction)
        self.update_graph_with_scan(
            scan=scan, row_range=row_range, col_range=col_range
        )

    def update_graph_with_scan(self, scan: Scan, row_range: range, col_range: range):
        new_nodes: Set[Tuple[Row, Col]] = set()
        for row in row_range:
            for col in col_range:
                if scan[row][col] in {".", "T", "C"}:
                    new_nodes.add((row, col))
                    if (row, col) not in self.nodes:
                        self.nodes.add((row, col))
                        self.edges[(row, col)] = set()

        for row, col in new_nodes:
            if (row, col + 1) in self.nodes:
                self.edges[(row, col)].add(((row, col + 1), Direction.RIGHT))
            if (row, col - 1) in self.nodes:
                self.edges[(row, col)].add(((row, col - 1), Direction.LEFT))
            if (row + 1, col) in self.nodes:
                self.edges[(row, col)].add(((row + 1, col), Direction.DOWN))
            if (row - 1, col) in self.nodes:
                self.edges[(row, col)].add(((row - 1, col), Direction.UP))

    def compute_path_to_start_node(self, from_node: Tuple[Row, Col]):
        def loop(actual_node, path_to_root, already_visited):
            while True:
                if self.edges.get(actual_node) is None:
                    break
                for new_node, direction in self.edges[actual_node]:
                    if new_node in already_visited:
                        continue
                    already_visited.add(new_node)
                    new_path = path_to_root + [direction]
                    if new_node == self.start_node:
                        return new_path
                    else:
                        return loop(new_node, new_path, already_visited)
                break

        return loop(from_node, [], {from_node})

    def __repr__(self):
        return str(
            {
                "nodes": self.nodes,
                "edges": self.edges,
            }
        )


def ranges_from_direction(
    actual_node: Tuple[Row, Col], direction: Direction
) -> Tuple[range, range]:
    if direction == Direction.RIGHT:
        row_range, col_range = range(actual_node[0] - 2, actual_node[0] + 3), range(
            actual_node[1] + 1, actual_node[1] + 3
        )
    if direction == Direction.LEFT:
        row_range, col_range = range(actual_node[0] - 2, actual_node[0] + 3), range(
            actual_node[1] - 2, actual_node[1]
        )
    if direction == Direction.DOWN:
        row_range, col_range = range(actual_node[0] + 1, actual_node[0] + 3), range(
            actual_node[1] - 2, actual_node[1] + 3
        )
    if direction == Direction.UP:
        row_range, col_range = range(actual_node[0] - 2, actual_node[0]), range(
            actual_node[1] - 2, actual_node[1] + 3
        )
    return row_range, col_range


def choose_direction(
    actual_node: Tuple[Row, Col], previous_direction: Direction, graph: ExploratoryGraph
) -> Tuple[Direction, Dict]:
    inverse_previous_direction = INVERSE_DIRECTION[previous_direction]
    possible_directions = {neighbor[1] for neighbor in graph.edges[actual_node]}
    debug_reason = {"possible_directions": str(possible_directions)}
    if len(possible_directions) == 1:
        direction = possible_directions.pop()
        debug_reason["reason"] = "BLOCKED"
    if len(possible_directions) == 2:
        if previous_direction is not None:
            possible_directions.remove(inverse_previous_direction)
        direction = possible_directions.pop()
        debug_reason["reason"] = "IN TUNNEL"
    if len(possible_directions) > 2:
        possible_directions.remove(inverse_previous_direction)
        if previous_direction in possible_directions:
            direction = previous_direction
            debug_reason["reason"] = "COURS FOREST"
        else:
            direction = random.choice(list(possible_directions))
            debug_reason["reason"] = "RANDOM CHOICE"
    return direction, debug_reason


def get_init_input() -> Tuple[int, int, int]:
    """
    Returns:
        Tuple[int, int, int]: number of rows, number of columns, number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
    """
    return tuple([int(i) for i in input().split()])


def get_actual_position_and_scan(row_nbr: int) -> Tuple[Tuple[Row, Col], Scan]:
    actual_position = tuple([int(i) for i in input().split()])
    scan = []
    for _ in range(row_nbr):
        scan.append(input())
    return actual_position, scan


################################################### SCRIPTS ###################################################

row_nbr, cols_nbr, alarm_duration = get_init_input()

in_exploration = True
direction: Direction = Direction.UP
graph: Optional[ExploratoryGraph] = None
for i in range(200):
    actual_position, scan = get_actual_position_and_scan(row_nbr)
    if graph is None:
        graph = ExploratoryGraph(start_node=actual_position, init_scan=scan)
    else:
        graph.update_graph(actual_node=actual_position, previous_direction=direction, scan=scan)

    on_command = scan[actual_position[0]][actual_position[1]] == "C"
    in_exploration = in_exploration & (not on_command)

    if on_command:
        print("on command", file=sys.stderr, flush=True)
        return_path_list = graph.compute_path_to_start_node(actual_position)
        print(return_path_list, file=sys.stderr, flush=True)
        return_path = iter(return_path_list)

    if in_exploration:
        print("exploration", file=sys.stderr, flush=True)
        direction, debug_reason = choose_direction(
            actual_node=actual_position, previous_direction=direction, graph=graph
        )
        print(f"choose direction debug: {debug_reason}", file=sys.stderr, flush=True)
    else:
        print("return", file=sys.stderr, flush=True)
        direction = next(return_path)

    print(direction, file=sys.stderr, flush=True)
    print(direction.value)
