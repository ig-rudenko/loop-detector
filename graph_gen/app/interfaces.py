import re


def interface_normal_view(interface) -> str:
    """
    Приводит имя интерфейса к виду принятому по умолчанию для коммутаторов

    Например:

    >>> interface_normal_view("Eth 0/1")
    'Ethernet 0/1'

    >>> interface_normal_view("GE1/0/12")
    'GigabitEthernet 1/0/12'

    >>> interface_normal_view("gi1")
    'GigabitEthernet 1'
    """

    interface_number = re.findall(r"(\d+([/\\]?\d*)*)", str(interface))
    if re.match(r"^[Ee]t", interface):
        return f"Ethernet {interface_number[0][0]}"
    if re.match(r"^[Ff]a", interface):
        return f"FastEthernet {interface_number[0][0]}"
    if re.match(r"^[Gg][ieE]", interface):
        return f"GigabitEthernet {interface_number[0][0]}"
    if re.match(r"^\d+", interface):
        return re.findall(r"^\d+", interface)[0]
    if re.match(r"^[Tt]e", interface):
        return f"TenGigabitEthernet {interface_number[0][0]}"

    return ""


def compare_interfaces(interface1: str, interface2: str) -> bool:
    """
    Сравнивает два интерфейса
    """
    interface1 = re.sub(r"\s", "", interface1).lower()
    interface2 = re.sub(r"\s", "", interface2).lower()

    if interface1 == interface2:
        return True

    interface1_normal = interface_normal_view(interface1)
    interface2_normal = interface_normal_view(interface2)

    if interface1 == interface2_normal:
        return True
    if interface1_normal == interface2:
        return True
    if interface1_normal == interface2_normal:
        return True
    return False
