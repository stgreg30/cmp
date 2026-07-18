from dataclasses import dataclass, asdict


@dataclass
class GraphNode:
    id: int
    node_type: str
    label: str


@dataclass
class GraphEdge:
    source: int
    target: int
    relation: str


class GraphEngine:

    def build(self, memory_nodes):

        nodes = []
        edges = []

        previous = None

        for i, item in enumerate(memory_nodes):

            label = item.name if item.name else item.node_type

            node = GraphNode(
                id=i,
                node_type=item.node_type,
                label=label
            )

            nodes.append(node)

            if previous is not None:

                edges.append(
                    GraphEdge(
                        source=previous.id,
                        target=node.id,
                        relation="NEXT"
                    )
                )

            previous = node

        return {
            "nodes": [asdict(n) for n in nodes],
            "edges": [asdict(e) for e in edges]
        }