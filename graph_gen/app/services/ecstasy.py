from functools import wraps

import requests


class UnauthorizedException(Exception):
    pass


def auth_decorator(func):
    @wraps(func)
    def wrapper(self: "EcstasyAPI", *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except UnauthorizedException:
            self.login()
            return func(self, *args, **kwargs)

    return wrapper


class EcstasyAPI:

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self) -> None:
        resp = self.session.post(
            f"{self.url}/api/token",
            data={"username": self.username, "password": self.password},
        )
        if resp.status_code == 200:
            token = resp.json()["access"]
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    @auth_decorator
    def get_device_interfaces(self, name_or_ip: str) -> list:
        resp = self.session.get(
            f"{self.url}/device/api/{name_or_ip}/interfaces?current_status=0&check_status=0&vlans=1"
        )
        if resp.status_code in [401, 403]:
            raise UnauthorizedException
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            return []
        return data.get("interfaces", [])

    @auth_decorator
    def get_device_info(self, name_or_ip: str) -> dict:
        resp = self.session.get(f"{self.url}/device/api/{name_or_ip}/info")
        if resp.status_code in [401, 403]:
            raise UnauthorizedException
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            return {}
        return data

    @auth_decorator
    def get_vlan_name(self, vid: int) -> str:
        resp = self.session.get(f"{self.url}/tools/api/vlan-desc?vlan={vid}")
        if resp.status_code in [401, 403]:
            raise UnauthorizedException
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            return ""
        return data.get("name", "")
