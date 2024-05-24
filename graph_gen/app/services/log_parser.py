import json
import re
from datetime import datetime
from typing import TypedDict, Generator

Host = TypedDict("Host", {"ip": str})
Record = TypedDict("Record", {"@timestamp": str, "message": str, "host": Host}


def get_loop_data_from_file(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def get_records(data: dict) -> list[Record]:
    return [r["_source"] for r in data["hits"]["hits"]]


def get_unique_ips(records: list[Record]) -> list[str]:
    return list({record["host"]["ip"] for record in records})


def process_logs(
    records: list[Record],
) -> Generator[tuple[str, str, str, datetime], None, None]:
    for record in records:
        device_ip: str = record["host"]["ip"]
        device_port = get_port(record)
        if device_port:
            timestamp = record["@timestamp"]
            message = record["message"]
            yield device_ip, device_port, message, datetime.fromisoformat(timestamp)


def get_port(record: Record) -> str:
    match = re.search(r"port (\S+) ", record["message"])
    if match:
        return re.sub(r"[()]", "", match.group(1))
    return ""
