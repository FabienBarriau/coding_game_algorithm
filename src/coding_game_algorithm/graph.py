from typing import Dict, List, Set, Tuple


class Graph:
    def __init__(
        self,
        nodes: Set[str],
        edges: Set[Tuple[str, str, float]],
        non_oriented: bool = True,
    ):
        nodes_in_edges: Set[str] = set()
        for edge in edges:
            nodes_in_edges.add(edge[0])
            nodes_in_edges.add(edge[1])
        if not nodes_in_edges.issubset(nodes):
            raise ValueError(
                f"Nodes in edges {nodes_in_edges} is not a subset of nodes {nodes}"
            )
        self.nodes = nodes
        self.edges_dict: Dict[str, Tuple[str, float]] = {}
        for start, to, weight in edges:
            if start not in self.edges_dict:
                self.edges_dict[start] = {(to, weight)}
            else:
                self.edges_dict[start].add((to, weight))
            if non_oriented:
                if to not in self.edges_dict:
                    self.edges_dict[to] = {(start, weight)}
                else:
                    self.edges_dict[to].add((start, weight))

    def neighbors(self, node_name: str) -> Tuple[str, float]:
        return self.edges_dict.get(node_name, set())


Path = List[str]
