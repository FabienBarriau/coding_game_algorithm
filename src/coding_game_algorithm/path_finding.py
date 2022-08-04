from coding_game_algorithm.graph import Graph, Path


def shortest_path_dijkstra(
    graph: Graph, start_node_name: str, end_node_name: str
) -> Path:
    temp = {start_node_name: 0}
    final_route = {}
    already_visited = set()
    actual_node = start_node_name

    while actual_node != end_node_name:
        already_visited.add(actual_node)
        for neighbor, weight in graph.neighbors(actual_node):
            new_weight = temp[actual_node] + weight
            neighbor_weight = temp.get(neighbor)
            if (neighbor_weight is None) or (neighbor_weight > new_weight):
                temp[neighbor] = new_weight
                final_route[neighbor] = actual_node
        temp_subset = {
            key: value for key, value in temp.items() if key not in already_visited
        }
        actual_node = min(temp_subset, key=temp_subset.get)

    path = [end_node_name]
    while path[-1] != start_node_name:
        path.append(final_route[path[-1]])

    path.reverse()

    return path
