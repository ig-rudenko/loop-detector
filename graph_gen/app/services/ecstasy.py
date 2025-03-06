import requests


class UnauthorizedException(Exception):
    pass


class EcstasyAPI:

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {api_key}"})

    def get_device_interfaces(self, name_or_ip: str) -> list:
        resp = self.session.get(
            f"{self.url}/api/v1/devices/{name_or_ip}/interfaces?current_status=0&check_status=0&vlans=1"
        )
        if resp.status_code in [401, 403]:
            raise UnauthorizedException
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            return []
        return data.get("interfaces", [])

    def get_device_info(self, name_or_ip: str) -> dict:
        resp = self.session.get(f"{self.url}/api/v1/devices/{name_or_ip}/info")
        if resp.status_code in [401, 403]:
            raise UnauthorizedException
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            return {}
        return data

    def get_vlan_name(self, vid: int) -> str:
        resp = self.session.get(f"{self.url}/api/v1/tools/vlan-desc?vlan={vid}")
        if resp.status_code in [401, 403]:
            raise UnauthorizedException
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            return ""
        return data.get("name", "")
