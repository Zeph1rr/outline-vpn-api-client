import json
from outline_vpn_api_client import OutlineClient

def test_outline_client_str_print(client: OutlineClient):
    assert json.loads(str(client)) == client.get_information().model_dump()