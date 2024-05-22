import re

from app.api import API
from app.graph import Node, Graph, Edge, Interface
from app.services.device import find_device_name


def find_target_ports(node: Node, graph: Graph, api: API) -> None:
    for interface in node.interfaces:
        next_device = find_device_name(interface["Description"])
        if next_device and re.search(r"SSW\d+$", next_device):
            node.target_ports.append(
                Interface(
                    name=interface["Interface"],
                    status=interface["Status"],
                    desc=interface["Description"],
                    vlans=interface["VLAN's"],
                )
            )


def get_back_port(node: Node, back_device_name: str, api: API) -> str:
    if not node.interfaces:
        node.interfaces = api.get_device_interfaces(node.name)

    for interface in node.interfaces:
        next_device = find_device_name(interface["Description"])
        if next_device == back_device_name:
            return interface["Interface"]
    return ""


def find_next_device(from_node: Node, graph: Graph, api: API):
    """
    Find the next device in the network.
    """

    for port in from_node.target_ports:
        next_device_name: str = find_device_name(port.desc)

        if next_device_name and graph.nodes.get(next_device_name):
            next_node = graph.nodes.get(next_device_name)
            back_port = get_back_port(next_node, from_node.name, api)

        elif next_device_name:
            next_device_info = api.get_device_info(next_device_name)
            next_node = Node(
                ip=next_device_info.get("deviceIP"),
                name=next_device_name,
                interfaces=api.get_device_interfaces(next_device_name),
                target_ports=[],
                weight=10,
            )
            find_target_ports(next_node, graph, api)
            back_port = get_back_port(next_node, from_node.name, api)
        else:
            next_node = Node(ip="", name=port.desc, interfaces=[], target_ports=[], weight=1)
            find_target_ports(next_node, graph, api)
            back_port = ""

        graph.add_node(next_node)
        graph.add_edge(
            Edge(from_node, next_node, from_port=port.name, to_port=back_port, weight=next_node.weight)
        )
