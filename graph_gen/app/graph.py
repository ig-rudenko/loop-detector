from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict, Any


@dataclass
class Interface:
    name: str
    status: str
    desc: str
    vlans: list[int]
    messages: list[dict[str, str | datetime]] = field(default_factory=list)


@dataclass
class Node:
    ip: str
    name: str
    weight: int  # Вес данного узла
    interfaces: list  # Список интерфейсов данного узла
    target_ports: list[Interface]  # Список таргетных портов данного узла


@dataclass
class Edge:
    from_node: Node
    to_node: Node
    from_port: str
    to_port: str
    weight: int


class GraphData(TypedDict):
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]


class Graph:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self._nodes: dict[str, Node] = {node.name: node for node in nodes}  # Список всех узлов
        self._edges = edges  # Список всех ребер

        self._graph_multiplier = 1  # Множитель графа

    @property
    def nodes(self):
        return self._nodes

    def add_node(self, node: Node):
        self._nodes[node.name] = node

    def remove_node(self, name: str):
        del self._nodes[name]

    @property
    def edges(self):
        return self._edges

    def add_edge(self, edge: Edge):
        self._edges.append(edge)

    def build_graph(self) -> GraphData:
        nodes: dict[str, Any] = {}
        edges: dict[str, Any] = {}
        for edge in self._edges:
            edge_data = self._get_edge_properties(edge)
            edges[edge_data["id"]] = edge_data
        for node in self._nodes.values():
            node_data = self._get_node_properties(node)
            nodes[node_data["id"]] = node_data
        return {
            "nodes": list(nodes.values()),
            "edges": list(edges.values()),
        }

    def _get_node_properties(self, node: Node) -> dict[str, Any]:
        shape = "diamond" if node.weight > 800 else "dot"
        color = "#00f597" if node.weight > 800 else "#55b6ff"
        size = (node.weight * 2 / 100) if node.weight > 800 else node.weight
        size *= self._graph_multiplier

        if "ATS" in node.name:
            color = "#ff66f7"
            shape = "square"
            size *= 2

        return {
            "id": node.name,
            "label": node.name,
            "title": self._get_node_title(node),
            "shape": shape,
            "color": color,
            "size": size,
            "font": {"color": "black"},
        }

    @staticmethod
    def _get_node_title(node: Node) -> str:
        return f"{node.name} (<strong>{node.ip}</strong>)"

    def _get_edge_properties(self, edge: Edge) -> dict[str, Any]:
        messages: list[dict[str, str | datetime]] = []
        for port in edge.from_node.target_ports:
            if port.name == edge.from_port:
                messages.extend(port.messages)

        for message in messages:
            if isinstance(message["timestamp"], datetime):
                message["timestamp"] = message["timestamp"].isoformat()

        return {
            "id": edge.from_node.name + ":::" + edge.to_node.name,
            "from": edge.from_node.name,
            "to": edge.to_node.name,
            "value": len(messages) * self._graph_multiplier,
            "title": self._get_edge_title(edge, messages_count=len(messages)),
            "messages": messages,
        }

    def _get_edge_title(self, edge: Edge, *, messages_count) -> str:
        return f"{edge.from_port} -> {edge.to_port}<br>messages_count {messages_count}"
