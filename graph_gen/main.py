import os

from app.api import API
from app.graph import Interface, Node, Graph
from app.interfaces import compare_interfaces
from app.loopd import get_loop_data, get_hits, get_unique_ips, process_logs
from app.services.traceroute import find_next_device

devices_nodes = {}
# devices_nodes = {
#     "ip": {
#         "interfaces": {},
#         "ports": {
#             "eth0": {
#                 "messages": [
#                     {"time": "2017-05-20T16:00:00Z", "message": ""},
#                 ],
#                 "description": "",
#                 "status": "",
#                 "vlan": "",
#             }
#         },
#     }
# }


if __name__ == "__main__":
    DEPTH = 2  # Глубина поиска узлов.

    load = get_loop_data("examples/loop-detected_17.05.2024.json")  # TODO: Заменить

    hits = get_hits(load)
    api = API(
        url=os.environ.get("ECSTASY_URL"),
        username=os.environ.get("ECSTASY_USERNAME"),
        password=os.environ.get("ECSTASY_PASSWORD"),
    )

    addresses = get_unique_ips(hits)
    for ip in addresses:
        device_info = api.get_device_info(ip)

        devices_nodes.setdefault(ip, {})
        devices_nodes[ip]["name"] = device_info["deviceName"]
        devices_nodes[ip]["interfaces"] = api.get_device_interfaces(ip)

    for ip, port, message, timestamp in process_logs(hits):
        devices_nodes[ip].setdefault("ports", {})
        devices_nodes[ip]["ports"].setdefault(port, {})
        devices_nodes[ip]["ports"][port].setdefault("messages", [])
        devices_nodes[ip]["ports"][port].setdefault("messages_count", 0)

        devices_nodes[ip]["ports"][port]["messages"].append({"message": message, "timestamp": timestamp})
        devices_nodes[ip]["ports"][port]["messages_count"] += 1

    # pprint(devices_nodes, depth=3)

    initial_nodes = []

    for ip, node in devices_nodes.items():
        target_ports = []
        for port, port_data in node["ports"].items():
            port_desc = ""
            for interface in node["interfaces"]:
                if compare_interfaces(port, interface["Interface"]):
                    target_ports.append(
                        Interface(
                            name=port,
                            status=interface["Status"],
                            desc=interface["Description"],
                            vlans=interface["VLAN's"],
                            messages=port_data["messages"],
                        )
                    )
                    break

        print(node["name"])
        initial_nodes.append(
            Node(
                ip=ip,
                name=node["name"],
                interfaces=node["interfaces"],
                target_ports=target_ports,
                weight=1000,
            )
        )

    graph = Graph(nodes=initial_nodes, edges=[])

    for i in range(DEPTH):
        for node in list(graph.nodes.values()):
            find_next_device(node, graph, api)

    graph_data = graph.build_graph()

    print(graph_data["nodes"])
    print(graph_data["edges"])
