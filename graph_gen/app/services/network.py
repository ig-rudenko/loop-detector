from app.graph import Graph, Node
from pyvis.network import Network

multiplier = 1


def _add_node(node: Node, network: Network):
    shape = "diamond" if node.weight > 800 else "dot"
    color = "pink" if node.weight > 800 else "#55b6ff"
    size = (node.weight * 2 / 100) if node.weight > 800 else node.weight
    size *= multiplier

    if "ATS" in node.name:
        color = "#FF00FF"
        shape = "square"
        size *= 2

    network.add_node(
        node.name.lower(),  # Уникальный идентификатор
        label=node.name,
        title=f"{node.name} {node.ip}",
        shape=shape,
        color=color,
        size=size,
    )


def create_network(graph: Graph):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.barnes_hut()
    net.repulsion(node_distance=130, damping=0.89)

    for node in list(graph.nodes.values()):
        _add_node(node, net)

    for edge in graph.edges:
        messages_count = sum(map(lambda x: len(x.messages), edge.from_node.target_ports))
        net.add_edge(
            edge.from_node.name.lower(),  # Уникальный идентификатор узла
            edge.to_node.name.lower(),  # Уникальный идентификатор узла
            value=messages_count * multiplier,
            title=f"{edge.from_port} -> {edge.to_port}<br>messages_count {messages_count}",
        )

    return net


def show_network(net: Network):
    net.show("graph.html", notebook=False)
