from app.graph import Interface, Node, Graph
from app.interfaces import compare_interfaces
from app.services.ecstasy import EcstasyAPI
from app.services.elastic import ElasticAPI
from app.services.log_parser import get_unique_ips, process_logs, Record
from app.services.traceroute import find_next_device


class GraphLoopBuilder:

    def __init__(self, elastic_api: ElasticAPI, ecstasy_api: EcstasyAPI):
        self._devices_nodes = {}
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
        self._elastic_api = elastic_api
        self._ecstasy_api = ecstasy_api
        self._graph: Graph = Graph([], [])
        self._graph_depth = 0

    @property
    def graph(self):
        return self._graph

    @property
    def graph_depth(self):
        return self._graph_depth

    def build_graph(self, logs_data) -> None:
        """
        Генерирует граф из логов.
        """
        self.build_initial_devices(logs_data)
        self.create_initial_graph()
        self.increase_graph_depth()

    def increase_graph_depth(self) -> None:
        """
        Увеличивает глубину графа путем добавления связей и поиска новых устройств.
        """
        for node in list(self._graph.nodes.values()):
            find_next_device(node, self._graph, self._ecstasy_api)
        self._graph_depth += 1

    def build_initial_devices(self, logs_records: list[Record]) -> None:
        """
        Формирует список устройств из логов, которые будут добавлены в граф.
        Также находит их интерфейсы.
        """

        addresses = get_unique_ips(logs_records)
        for ip in addresses:
            device_info = self._ecstasy_api.get_device_info(ip)
            self._devices_nodes.setdefault(ip, {})
            self._devices_nodes[ip]["name"] = device_info["deviceName"]
            self._devices_nodes[ip]["interfaces"] = self._ecstasy_api.get_device_interfaces(ip)
            self._devices_nodes[ip].setdefault("ports", {})

        for ip, port, message, timestamp in process_logs(logs_records):
            self._devices_nodes[ip]["ports"].setdefault(port, {})
            self._devices_nodes[ip]["ports"][port].setdefault("messages", [])
            self._devices_nodes[ip]["ports"][port].setdefault("messages_count", 0)

            self._devices_nodes[ip]["ports"][port]["messages"].append(
                {"message": message, "timestamp": timestamp}
            )
            self._devices_nodes[ip]["ports"][port]["messages_count"] += 1

    def create_initial_graph(self) -> None:
        """
        Добавляет устройства в граф без формирования связей между ними.
        """
        initial_nodes = []

        for ip, node in self._devices_nodes.items():
            target_ports = []
            for port, port_data in node["ports"].items():
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

            initial_nodes.append(
                Node(
                    ip=ip,
                    name=node["name"],
                    interfaces=node["interfaces"],
                    target_ports=target_ports,
                    weight=1000,
                )
            )

        self._graph = Graph(nodes=initial_nodes, edges=[])
