import re


def find_device_name(description: str) -> str:
    """
    Find the device name from the description.
    """
    match = re.search(r"SVSL-\S+?SW\d+|CE6\S+?ATS\d+", description)
    if match:
        return match.group(0)
    return ""
