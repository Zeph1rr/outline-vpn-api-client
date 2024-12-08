from sys import argv

import warnings
import json

from .client import OutlineClient

def main(client: OutlineClient, action: str):
    match(action):
        case "get_info":
            print(json.dumps(client.get_information(), ensure_ascii=False, indent=4))
        case "data_transfer":
            print(json.dumps(client.metrics.get_data_transfer(), ensure_ascii=False, indent=4))
        case _:
            raise NotImplementedError("Usage: python -m outline_vpn_api_client management_url get_info")

if __name__ == "__main__":
    if argv[1] == "-h" or argv[1] == '--help':
        print("Usage: python -m outline_vpn_api_client management_url get_info")
    client = OutlineClient(management_url=argv[1])
    action = argv[2]
    with warnings.catch_warnings(action="ignore"):
        main(client, action)