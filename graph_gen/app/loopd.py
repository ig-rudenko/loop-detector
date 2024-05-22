import json
import re
from datetime import datetime


def get_loop_data(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def get_hits(data: dict) -> list:
    return data["rawResponse"]["hits"]["hits"]


def get_unique_ips(records: list) -> list:
    return list({record["fields"]["host.ip"][0] for record in records})


def process_logs(records: list):
    for record in records:
        device_ip: str = record["fields"]["host.ip"][0]
        device_port = get_port(record)
        if device_port:
            timestamp = record["fields"]["@timestamp"][0]
            message = record["fields"]["event.original"][0]
            yield device_ip, device_port, message, datetime.fromisoformat(timestamp)


def get_port(record: dict) -> str:
    match = re.search(r"port (\S+) ", record["fields"]["event.original"][0])
    if match:
        return re.sub(r"[()]", "", match.group(1))
    return ""
