from coding_game_algorithm.graph import Graph
from coding_game_algorithm.path_finding import shortest_path_dijkstra

def test_shortest_path_dijkstra():
    graph = Graph({
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J"
    },
    {
        ("A", "B", 85),
        ("A", "C", 217),
        ("A", "E", 173),
        ("B", "F", 80),
        ("C", "G", 186),
        ("C", "H", 103),
        ("D", "H", 183),
        ("E", "J", 502),
        ("F", "I", 250),
        ("H", "J", 167),
        ("I", "J", 84),
    })
    result_path = shortest_path_dijkstra(graph=graph, start_node_name="A", end_node_name="J")
    assert result_path == ["A", "C", "H", "J"]
    
