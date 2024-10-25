import json
import re
from datetime import datetime
from typing import TypedDict, Generator

import jq
from app.settings import settings

Host = TypedDict("Host", {"ip": str})
Record = TypedDict("Record", {"@timestamp": str, "message": str, "host": Host})


def get_loop_data_from_file(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def get_records(data: dict) -> list[Record]:
    result = []
    for row in data["hits"]["hits"]:
        device_ip = str(jq.first(settings.es_jq_device_ip, row["_source"]))
        message = str(jq.first(settings.es_jq_message, row["_source"]))
        record: Record = {
            "@timestamp": row["_source"]["@timestamp"],
            "message": message,
            "host": {"ip": device_ip},
        }
        result.append(record)

    return result


def get_unique_ips(records: list[Record]) -> list[str]:
    return list({record["host"]["ip"] for record in records})


def get_unique_vlans(records: list[Record]) -> dict[int, int]:
    """Returns a dict of unique VLANs and their counts"""
    result: dict[int, int] = {}
    for record in records:
        vlans: list[str] = re.findall(r"(?<=VLAN)\d{1,4}|(?<=v)\d{1,4}", record["message"], re.IGNORECASE)
        for vlan in vlans:
            try:
                vid = int(vlan)
            except ValueError:
                continue
            result.setdefault(vid, 0)
            result[vid] += 1
    return result


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
